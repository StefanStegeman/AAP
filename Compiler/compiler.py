from Compiler.context import Context
from Compiler.function import Function
from Compiler.number import Number
from copy import copy
from functools import reduce, partial
from Interpreter.nodes import *
from itertools import chain
from operator import is_not, add

def Compile(filename, functionAssignNode, node):
    instructions = [".cpu cortex-m0\n", ".text\n", ".align 2\n", f".global {functionAssignNode.token.value}\n\n", f'{functionAssignNode.token.value}:\n', set()]
    context = Context()

    instructions = VisitNode(node, context, instructions)[1]

    registers = ["R4", "R5", "R6", "R7", "R8"]
    try:
        highestRegisterIndex = registers.index(max(instructions[5]))
        usedRegisters = registers[0:highestRegisterIndex + 1]
    except ValueError:
        usedRegisters = []                         
    usedRegisters = ', '.join(usedRegisters)
    if len(usedRegisters) > 0:
        registersToPop = f"\tPOP \t{{ {usedRegisters}, PC }}"
        registersToPush = f"\tPUSH \t{{ {usedRegisters}, LR }}\n"
    else:
        registersToPop = f"\tPOP \t{{ PC }}"
        registersToPush = f"\tPUSH \t{{ LR }}\n"
    instructions.append(registersToPop)
    instructions[5] = registersToPush

    with open(filename, "w") as file:
        instructions = map(lambda x:x, instructions)
        file.writelines(instructions)

def VisitNode(node, context, instructions):
    """ VisitNode 
    Parameters:
        node (Node)       :
        context (Context) :
    Returns:

    """
    method = globals()[f'Visit{type(node).__name__}']
    try:
        return method(node, context, instructions)
    except Exception as exception:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(exception).__name__, exception.args)
        print(message)

def VisitNumberNode(node: NumberNode, context: Context, instructions):
    """ VisitNumberNode 
    Parameters:
        node (NumberNode) :
        context (Context) :
    Returns:
        number (Number)   : A new instance of the Number class.
    """
    register = context.registers.pop(0)
    instructions[5].add(register)
    instructions.append(f"\tMOVS\t{register}, #{node.token.value}\n")
    return Number(node.token.value, context, register), instructions

def VisitReturnNode(node: ReturnNode, context: Context, instructions):
    """ VisitReturnNode 
    Parameters:
        node (ReturnNode) :
        context (Context) :
    Returns:
        
    """
    if node.node:
        result, instructions = VisitNode(node.node, context, instructions)
        instructions.append("END:\n")
        if result.register != "R0":
            instructions.append(f"\tMOVS\tR0, {result.register}\n")
        return result, instructions

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context, instructions):
    """ VisitBinaryOperationNode 
    Parameters:
        node (BinaryOperationNode) :
        context (Context)          :
    Returns:
        
    """
    left, instructions = VisitNode(node.left, context, instructions)
    right, instructions = VisitNode(node.right, context, instructions)
    method = getattr(left, f'{type(node.operator).__name__}')
    try:
        return method(right, context, instructions)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def VisitVariableAssignNode(node: VariableAssignNode, context: Context, instructions):
    """ VisitVariableAssignNode 
    Parameters:
        node (VariableAssignNode) :
        context (Context)         :
    Returns:
        
    """
    name = node.token.value
    value, instructions = VisitNode(node.node, context, instructions)
    context.symbolDictionary.SetValue(name, value)
    return value, instructions

def VisitVariableAccessNode(node: VariableAccessNode, context: Context, instructions):
    """ VisitVariableAccessNode 
    Parameters:
        node (VariableAccessNode) :
        context (Context)         :
    Returns:
        
    """
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        raise Exception(f"No value found for '{name}'..")
    return value, instructions

def VisitListNode(node: ListNode, context: Context, instructions):
    """ VisitListNode 
    Parameters:
        node (ListNode)   :
        context (Context) :
    Returns:
        
    """
    returnNodes = map(lambda element: ReturnNode == type(element), node.elements)
    returns = reduce(add, returnNodes, 0)
    print(returns)
    def VisitElement(element):
        if not returns:
            return VisitNode(element, context, instructions)
        if type(element) == ReturnNode:
            return VisitNode(element, context, instructions)
        VisitNode(element, context, instructions)

    elements = []
    elements = list(chain(*map(lambda node: [*elements, VisitElement(node)], node.elements)))
    elements = list(filter(partial(is_not, None), elements))
    if len(elements) == 1:
        return elements[0], instructions
    return elements, instructions

def VisitIfNode(node: IfNode, context: Context, instructions):
    """ VisitIfNode 
    Parameters:
        node (IfNode)     :
        context (Context) :
    Returns:
        
    """
    condition, expression = node.case
    registers = copy(context.registers)
    value, instructions = VisitNode(condition, context, instructions)
    value = value
    instructions.append(f"\tCMP \t{value.register}, #1\n")
    afterIf = context.labels.pop(0)
    afterElse = context.labels.pop(0)
    instructions.append(f"\tBNE \t{afterIf}\n")
    resultRegister = context.registers[0]
    instructions[5].add(resultRegister)
    result, instructions = VisitNode(expression, context, instructions)
    remainingRegisters = context.registers
    instructions.append(f"\tB   \t{afterElse}\n")
    instructions.append(f"{afterIf}:\n")
    context.registers = registers
    if node.elseCase:
        instructions = VisitNode(node.elseCase, context, instructions)
        if type(node.elseCase) == FunctionCallNode:
            instructions.append(f"\tMOVS\t{resultRegister}, R0\n")
    instructions.append(f"{afterElse}:\n")
    context.registers = min(context.registers, remainingRegisters)
    return result, instructions


def VisitWhileNode(node: WhileNode, context: Context, instructions):
    """ VisitWhileNode 
    Parameters:
        node (WhileNode)  :
        context (Context) :
    Returns:
        
    """
    instructions.append("LOOP:\n")
    condition, instructions = VisitNode(node.condition, context, instructions)
    instructions = VisitNode(node.body, context, instructions)
    instructions.append(f"\tCMP \t{condition.register}, #1\n")
    instructions.append(f"\tBEQ \tLOOP\n")
    return instructions

def VisitFunctionAssignNode(node: FunctionAssignNode, context: Context, instructions):
    """ VisitFunctionAssignNode 
    Parameters:
        node (FunctionAssignNode) :
        context (Context)         :
    Returns:
        
    """
    function = Function(node.token.value, node.arguments, node.body, context) 
    if node.token:
        context.symbolDictionary.SetValue(node.token.value, function)
    arguments = list(map(lambda _: Number(0, context, context.registers.pop(0)), node.arguments))
    body, context = function.Compile(arguments, context)
    return VisitNode(body, context, instructions)

def VisitFunctionCallNode(node: FunctionCallNode, context: Context, instructions):
    """ VisitFunctionCallNode 
    Parameters:
        node (FunctionCallNode) :
        context (Context)       :
    Returns:
        
    """
    arguments = [] 
    arguments, instructions = list(chain(*map(lambda node: [*arguments, VisitNode(node, context, instructions)], node.arguments)))
    instructions.append(f"\tBL  \t{node.node.token.value}\n")
    return instructions