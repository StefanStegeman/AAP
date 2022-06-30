from Compiler.context import Context
from Compiler.function import Function
from Compiler.number import Number
from copy import copy
from functools import reduce, partial
from Interpreter.nodes import *
from itertools import chain
from operator import is_not, add
from typing import List, Tuple

def Compile(filename: str, FunctionDefenitionNode: FunctionDefenitionNode, ast: ListNode) -> None:
    """ Compile the given function and write it to a file. 
    Haskell:
        Compile :: String -> FunctionDefenitionNode -> ListNode -> None
    Parameters:
        filename (str): The name of the file where the output will be written to.
        FunctionDefenitionNode (FunctionDefenitionNode): The function which will be compiled.
        ast (ListNode): The node where the compilation starts.
    """
    instructions = [".cpu cortex-m0\n", ".text\n", ".align 2\n", f".global {FunctionDefenitionNode.token.value}\n\n", f'{FunctionDefenitionNode.token.value}:\n', set()]
    registers = ["R4", "R5", "R6", "R7", "R8"]
    context = Context()
    instructions = VisitNode(ast, context, instructions)[1]

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

def VisitNode(node: 'AllNodes', context: Context, instructions: List[Union[str, set]]) -> Union[FunctionCallNode, List[Number], Number]:
    """ Visit the passed Node's function and compile this.
    Every node has a Visit{node} function which is responsible for compiling that node.
    Haskell:
        VisitNode :: Node -> Context -> [String & Set] -> FunctionCallnode | [Number] | Number
    Parameters:
        node (Node): The node which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of the AST.
    """
    method = globals()[f'Visit{type(node).__name__}']
    try:
        return method(node, context, instructions)
    except Exception as exception:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(exception).__name__, exception.args)
        print(message)

def VisitNumberNode(node: NumberNode, context: Context, instructions: List[Union[str, set]]) -> Tuple[Number, List[Union[str, set]]]:
    """ Compile a NumberNode. 
    Haskell:
        VisitNumberNode :: NumberNode -> Context -> [String & Set] -> Tuple
    Parameters:
        node (NumberNode): The NumberNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the NumberNode.
        instructions (Lst): The updated list of assembler instructions.
    """
    register = context.registers.pop(0)
    instructions[5].add(register)
    instructions.append(f"\tMOVS\t{register}, #{node.token.value}\n")
    return Number(node.token.value, context, register), instructions

def VisitReturnNode(node: ReturnNode, context: Context, instructions: List[Union[str, set]]) -> Union[Tuple[Number, List[Union[str, set]]], List[Union[str, set]]]:
    """ Compile a ReturnNode. 
    Haskell:
        VisitReturnNode :: ReturnNode -> Context -> [String & Set] -> Tuple | [String & Set]
    Parameters:
        node (ReturnNode): The ReturnNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the ReturnNode.
        instructions (Lst): The updated list of assembler instructions.
    """
    if node.node:
        result, instructions = VisitNode(node.node, context, instructions)
        instructions.append("END:\n")
        if result.register != "R0":
            instructions.append(f"\tMOVS\tR0, {result.register}\n")
        return result, instructions

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context, instructions: List[Union[str, set]]) -> Tuple[Number, List[Union[str, set]]]:
    """ Compile a BinaryOperation. 
    Haskell:
        VisitBinaryOperationNode :: BinaryOperationNode -> Context -> [String & Set] -> Tuple
    Parameters:
        node (BinaryOperationNode): The BinaryOperationNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the BinaryOperationNode.
        instructions (Lst): The updated list of assembler instructions.
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

def VisitVariableAssignNode(node: VariableAssignNode, context: Context, instructions: List[Union[str, set]]) -> Tuple[Number, List[Union[str, set]]]:
    """ Compile a VariableAssignNode. 
    Haskell:
        VisitVariableAssignNode :: VariableAssignNode -> Context -> [String && Set] -> Tuple
    Parameters:
        node (VariableAssignNode): The VariableAssignNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the VariableAssignNode.
        instructions (Lst): The updated list of assembler instructions.
    """
    name = node.token.value
    value, instructions = VisitNode(node.node, context, instructions)
    context.symbolDictionary.SetValue(name, value)
    return value, instructions

def VisitVariableAccessNode(node: VariableAccessNode, context: Context, instructions: List[Union[str, set]]) -> Tuple[Number, List[Union[str, set]]]:
    """ Compile a VariableAccessNode. 
    Haskell:
        VisitVariableAccessNode :: VariableAccessNode -> Context -> [String && Set] -> Tuple
    Parameters:
        node (VariableAccessNode): The VariableAccessNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the VariableAccessNode.
        instructions (Lst): The updated list of assembler instructions.
    """
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        raise Exception(f"No value found for '{name}'..")
    return value, instructions

def VisitListNode(node: ListNode, context: Context, instructions: List[Union[str, set]]) -> Union[Tuple[Number, List[Union[str, set]]], List[Union[str, set]]]:
    """ Compile a ListNode. 
    Haskell:
        VisitListNode :: ListNode -> Context -> [String && Set] -> Tuple | [String & Set]
    Parameters:
        node (ListNode): The ListNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the ListNode.
        instructions (Lst): The updated list of assembler instructions.
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

def VisitIfNode(node: IfNode, context: Context, instructions: List[Union[str, set]]) -> Union[Tuple[Number, List[Union[str, set]]], List[Union[str, set]]]:
    """ Compile a IfNode. 
    Haskell:
        VisitIfNode :: IfNode -> Context -> [String && Set] -> Tuple | [String & Set]
    Parameters:
        node (IfNode): The IfNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        number (Number): The result of compiling the IfNode.
        instructions (Lst): The updated list of assembler instructions.
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


def VisitWhileNode(node: WhileNode, context: Context, instructions: List[Union[str, set]]) -> List[Union[str, set]]:
    """ Compile a WhileNode. 
    Haskell:
        VisitWhileNode :: WhileNode -> Context -> [String && Set] -> [String & Set]
    Parameters:
        node (WhileNode): The WhileNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        instructions (Lst): The updated list of assembler instructions.
    """
    instructions.append("LOOP:\n")
    condition, instructions = VisitNode(node.condition, context, instructions)
    instructions = VisitNode(node.body, context, instructions)
    instructions.append(f"\tCMP \t{condition.register}, #1\n")
    instructions.append(f"\tBEQ \tLOOP\n")
    return instructions

def VisitFunctionDefenitionNode(node: FunctionDefenitionNode, context: Context, instructions: List[Union[str, set]]) -> Tuple[Function, List[Union[str, set]]]:
    """ Compile a FunctionDefenitionNode.
    Haskell:
        VisitFunctionDefenitionNode :: FunctionDefenitionNode -> Context -> [String && Set] ->  Tuple
    Parameters:
        node (FunctionDefenitionNode): The FunctionDefenitionNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        function (Function): The result of compiling the FunctionDefenitionNode.
        instructions (Lst): The updated list of assembler instructions.
    """
    function = Function(node.token.value, node.arguments, node.body, context) 
    if node.token:
        context.symbolDictionary.SetValue(node.token.value, function)
    arguments = list(map(lambda _: Number(0, context, context.registers.pop(0)), node.arguments))
    body, context = function.Compile(arguments, context)
    return VisitNode(body, context, instructions)

def VisitFunctionCallNode(node: FunctionCallNode, context: Context, instructions: List[Union[str, set]]) -> List[Union[str, set]]:
    """ Compile a FunctionCallNode. 
    Haskell:
        VisitFunctionCallNode :: FunctionCallNode -> Context -> [String && Set] -> [String & Set]
    Parameters:
        node (FunctionCallNode): The FunctionCallNode which will be compiled.
        context (Context): The current existing context.
        instructions (Lst): The list containing the assembler instructions.
    Returns:
        instructions (Lst): The updated list of assembler instructions.
    """
    arguments = [] 
    arguments, instructions = list(chain(*map(lambda node: [*arguments, VisitNode(node, context, instructions)], node.arguments)))
    instructions.append(f"\tBL  \t{node.node.token.value}\n")
    return instructions

AllNodes = [NumberNode, VariableAccessNode, BinaryOperationNode, VariableAccessNode, VariableAssignNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ListNode, ReturnNode]