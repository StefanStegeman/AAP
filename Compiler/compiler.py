from copy import copy
from itertools import chain
from functools import reduce, partial
from operator import is_not, add
from Interpreter.nodes import *
from Compiler.context import Context
from Compiler.function import Function
from Compiler.number import Number

class Compiler:
    def __init__(self, filenameOutput: str, functionAssignNode: FunctionAssignNode) -> None:
        self.filenameOutput = filenameOutput

        self.context = Context()
        self.instructions = [".cpu cortex-m0\n", ".text\n", ".align 2\n", f".global {functionAssignNode.token.value}\n\n", f'{functionAssignNode.token.value}:\n', set()]

    def __del__(self) -> None:
        registers = ["R4", "R5", "R6", "R7", "R8"]
        try:
            highestRegisterIndex = registers.index(max(self.instructions[5]))
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
        self.instructions.append(registersToPop)
        self.instructions[5] = registersToPush

        with open(self.filenameOutput, "w") as file:
            self.instructions = map(lambda x:x, self.instructions)
            file.writelines(self.instructions)

    def VisitNode(self, node, context = None):
        """ VisitNode 
        Parameters:
            node (Node)       :
            context (Context) :
        Returns:

        """
        if context == None:
            context = self.context

        def VisitNumberNode(node: NumberNode, context: Context):
            """ VisitNumberNode 
            Parameters:
                node (NumberNode) :
                context (Context) :
            Returns:
                number (Number)   : A new instance of the Number class.
            """
            register = context.registers.pop(0)
            self.instructions[5].add(register)
            self.instructions.append(f"\tMOVS\t{register}, #{node.token.value}\n")
            return Number(node.token.value, context, register)

        def VisitReturnNode(node: ReturnNode, context: Context):
            """ VisitReturnNode 
            Parameters:
                node (ReturnNode) :
                context (Context) :
            Returns:
                
            """
            if node.node:
                result = self.VisitNode(node.node, context)
                self.instructions.append("END:\n")
                if result.register != "R0":
                    self.instructions.append(f"\tMOVS\tR0, {result.register}\n")
                return result

        def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context):
            """ VisitBinaryOperationNode 
            Parameters:
                node (BinaryOperationNode) :
                context (Context)          :
            Returns:
                
            """
            left = self.VisitNode(node.left, context)
            right = self.VisitNode(node.right, context)
            method = getattr(left, f'{type(node.operator).__name__}')
            try:
                return method(right, context, self.instructions)
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

        def VisitVariableAssignNode(node: VariableAssignNode, context: Context):
            """ VisitVariableAssignNode 
            Parameters:
                node (VariableAssignNode) :
                context (Context)         :
            Returns:
                
            """
            name = node.token.value
            value = self.VisitNode(node.node, context)
            context.symbolDictionary.SetValue(name, value)
            return value

        def VisitVariableAccessNode(node: VariableAccessNode, context: Context):
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
            return value

        def VisitListNode(node: ListNode, context: Context):
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
                    return self.VisitNode(element, context)
                if type(element) == ReturnNode:
                    return self.VisitNode(element, context)
                self.VisitNode(element, context)

            elements = []
            elements = list(chain(*map(lambda node: [*elements, VisitElement(node)], node.elements)))
            elements = list(filter(partial(is_not, None), elements))
            if len(elements) == 1:
                return elements[0]
            return elements

        def VisitIfNode(node: IfNode, context: Context):
            """ VisitIfNode 
            Parameters:
                node (IfNode)     :
                context (Context) :
            Returns:
                
            """
            condition, expression = node.cases[0]
            registers = copy(context.registers)
            value = self.VisitNode(condition, context)
            value = value
            self.instructions.append(f"\tCMP \t{value.register}, #1\n")
            afterIf = context.labels.pop(0)
            afterElse = context.labels.pop(0)
            self.instructions.append(f"\tBNE \t{afterIf}\n")
            resultRegister = context.registers[0]
            self.instructions[5].add(resultRegister)
            result = self.VisitNode(expression, context)
            remainingRegisters = context.registers
            self.instructions.append(f"\tB   \t{afterElse}\n")
            self.instructions.append(f"{afterIf}:\n")
            context.registers = registers
            if node.elseCase:
                self.VisitNode(node.elseCase, context)
                if type(node.elseCase) == FunctionCallNode:
                    self.instructions.append(f"\tMOVS\t{resultRegister}, R0\n")
            self.instructions.append(f"{afterElse}:\n")
            context.registers = min(context.registers, remainingRegisters)
            return result


        def VisitWhileNode(node: WhileNode, context: Context):
            """ VisitWhileNode 
            Parameters:
                node (WhileNode)  :
                context (Context) :
            Returns:
                
            """
            self.instructions.append("LOOP:\n")
            condition = self.VisitNode(node.condition, context)
            self.VisitNode(node.body, context)
            self.instructions.append(f"\tCMP \t{condition.register}, #1\n")
            self.instructions.append(f"\tBEQ \tLOOP\n")

        def VisitFunctionAssignNode(node: FunctionAssignNode, context: Context):
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
            return self.VisitNode(body, context)

        def VisitFunctionCallNode(node: FunctionCallNode, context: Context):
            """ VisitFunctionCallNode 
            Parameters:
                node (FunctionCallNode) :
                context (Context)       :
            Returns:
                
            """
            arguments = [] 
            arguments = list(chain(*map(lambda node: [*arguments, self.VisitNode(node, context)], node.arguments)))
            self.instructions.append(f"\tBL  \t{node.node.token.value}\n")

        method = locals()[f'Visit{type(node).__name__}']
        try:
            return method(node, context)
        except Exception as exception:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exception).__name__, exception.args)
            print(message)