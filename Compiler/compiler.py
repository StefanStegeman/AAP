from Compiler.context import Context
from Compiler.function import Function
from Compiler.number import Number
from copy import copy
from functools import reduce, partial
from Interpreter.nodes import *
from itertools import chain
from operator import is_not, add
import traceback

class Compiler():
    def __init__(self, FunctionDefenitionNode: FunctionDefenitionNode) -> None:
        """ Initialize the instructions and context. 
        Haskell:
            Init :: FunctionDefenitionNode -> None
        Parameters:
            FunctionDefenitionNode (FunctionDefenitionNode): The function defenition node to write the name in the assembler file. """
        self.instructions = [".cpu cortex-m0\n", ".text\n", ".align 2\n", f".global {FunctionDefenitionNode.token.value}\n\n", f'{FunctionDefenitionNode.token.value}:\n', set()]
        self.context = Context()
        
    def Compile(self, ast: ListNode, output: str) -> None:
        """ Compile the Abstract Syntax Tree and write it to a file. 
        Haskell:
            Compile :: ListNode -> String -> None
        Parameters:
            ast (ListNode): The AST which will be compiled.
            output (str): The name of the file where the assembler instructions will be written to.
        """
        self.VisitNode(ast, self.context)

        registers = ["R4", "R5", "R6", "R7", "R8"]
        try:
            index: int = registers.index(max(self.instructions[5]))
            usedRegisters: str = registers[0:index + 1]
        except:
            usedRegisters = []

        usedRegisters: str = ', '.join(usedRegisters)
        if len(usedRegisters) > 0:
            popRegisters = f"\tPOP \t{{ {usedRegisters}, PC }}"
            pushRegisters = f"\tPUSH \t{{ {usedRegisters}, LR }}\n"
        else:
            popRegisters = f"\tPOP \t{{ PC }}"
            pushRegisters = f"\tPUSH \t{{ LR }}\n"
        self.instructions.append(popRegisters)
        self.instructions[5] = pushRegisters

        with open(output, "w") as file:
            self.instructions = map(lambda instruction:instruction, self.instructions)
            file.writelines(self.instructions)

    def VisitNode(self, node: 'AllNodes', context: Context = None) -> Union[FunctionCallNode, List[Number], Number]:
        """ Visit the passed Node's function and compile this.
        Every node has a Visit{node} function which is responsible for compiling that node.
        Haskell:
            VisitNode :: Node -> Context -> FunctionCallnode | [Number] | Number
        Parameters:
            node (Node): The node which will be compiled.
            context (Context): The current existing context.
        Returns:
            number (Number): The result of the AST.
        """
        def VisitNumberNode(node: NumberNode, context: Context) -> Number:
            """ Compile a NumberNode. 
            Haskell:
                VisitNumberNode :: NumberNode -> Context -> Number
            Parameters:
                node (NumberNode): The NumberNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the NumberNode.
            """
            register = context.registers.pop(0)
            self.instructions[5].add(register)
            self.instructions.append(f"\tMOVS\t{register}, #{node.token.value}\n")
            return Number(node.token.value, context, register)

        def VisitReturnNode(node: ReturnNode, context: Context) -> Number:
            """ Compile a ReturnNode. 
            Haskell:
                VisitReturnNode :: ReturnNode -> Context -> Number
            Parameters:
                node (ReturnNode): The ReturnNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the ReturnNode.
            """
            if node.node:
                result = self.VisitNode(node.node, context)
                self.instructions.append("END:\n")
                if result.register != "R0":
                    self.instructions.append(f"\tMOVS\tR0, {result.register}\n")
                return result
        
        def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context) -> Number:
            """ Compile a BinaryOperation. 
            Haskell:
                VisitBinaryOperationNode :: BinaryOperationNode -> Context -> Number
            Parameters:
                node (BinaryOperationNode): The BinaryOperationNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the BinaryOperationNode.
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
                print(traceback.format_exc())

        def VisitVariableAssignNode(node: VariableAssignNode, context: Context) -> Number:
            """ Compile a VariableAssignNode. 
            Haskell:
                VisitVariableAssignNode :: VariableAssignNode -> Context -> Number
            Parameters:
                node (VariableAssignNode): The VariableAssignNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the VariableAssignNode.
            """
            name = node.token.value
            value = self.VisitNode(node.node, context)
            context.symbolDictionary.SetValue(name, value)
            return value

        def VisitVariableAccessNode(node: VariableAccessNode, context: Context) -> Number:
            """ Compile a VariableAccessNode. 
            Haskell:
                VisitVariableAccessNode :: VariableAccessNode -> Context -> Number
            Parameters:
                node (VariableAccessNode): The VariableAccessNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the VariableAccessNode.
            """
            name = node.token.value
            value = context.symbolDictionary.GetValue(name)
            if not value:
                raise Exception(f"No value found for '{name}'..")
            return value

        def VisitListNode(node: ListNode, context: Context) -> Number:
            """ Compile a ListNode. 
            Haskell:
                VisitListNode :: ListNode -> Context -> Number
            Parameters:
                node (ListNode): The ListNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the ListNode.
            """
            returnNodes = map(lambda element: ReturnNode == type(element), node.elements)
            returns = reduce(add, returnNodes, 0)
            print(returns)
            def VisitElement(element: 'AllNodes') -> Number:
                """ Visit element of list.
                Haskell:
                    VisitElement :: Node -> Number
                Parameters: 
                    element (Node): An element from the ListNode which will be interpreted.
                Returns:
                    number (Number): The result of interpreting the node.
                """
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

        def VisitIfNode(node: IfNode, context: Context) -> Number:
            """ Compile a IfNode. 
            Haskell:
                VisitIfNode :: IfNode -> Context -> Number
            Parameters:
                node (IfNode): The IfNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                number (Number): The result of compiling the IfNode.
            """
            condition, expression = node.case
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

        def VisitWhileNode(node: WhileNode, context: Context) -> None:
            """ Compile a WhileNode. 
            Haskell:
                VisitWhileNode :: WhileNode -> Context -> None
            Parameters:
                node (WhileNode): The WhileNode which will be compiled.
                context (Context): The current existing context.
            """
            self.instructions.append("LOOP:\n")
            condition = self.VisitNode(node.condition, context)
            self.VisitNode(node.body, context)
            self.instructions.append(f"\tCMP \t{condition.register}, #1\n")
            self.instructions.append(f"\tBEQ \tLOOP\n")

        def VisitFunctionDefenitionNode(node: FunctionDefenitionNode, context: Context) -> Function:
            """ Compile a FunctionDefenitionNode.
            Haskell:
                VisitFunctionDefenitionNode :: FunctionDefenitionNode -> Context -> Function
            Parameters:
                node (FunctionDefenitionNode): The FunctionDefenitionNode which will be compiled.
                context (Context): The current existing context.
            Returns:
                function (Function): The result of compiling the FunctionDefenitionNode.
            """
            function = Function(node.token.value, node.arguments, node.body, context) 
            if node.token:
                context.symbolDictionary.SetValue(node.token.value, function)
            arguments = list(map(lambda _: Number(0, context, context.registers.pop(0)), node.arguments))
            body, context = function.Compile(arguments, context)
            return self.VisitNode(body, context)

        def VisitFunctionCallNode(node: FunctionCallNode, context: Context) -> None:
            """ Compile a FunctionCallNode. 
            Haskell:
                VisitFunctionCallNode :: FunctionCallNode -> Context -> None
            Parameters:
                node (FunctionCallNode): The FunctionCallNode which will be compiled.
                context (Context): The current existing context.
            """
            arguments = [] 
            arguments = list(chain(*map(lambda node: [*arguments, self.VisitNode(node, context)], node.arguments)))
            self.instructions.append(f"\tBL  \t{node.node.token.value}\n")
            return self.instructions
        
        methodName: str = f'Visit{type(node).__name__}'
        method = locals()[methodName]
        return method(node, context)

AllNodes = Union[NumberNode, VariableAccessNode, BinaryOperationNode, VariableAccessNode, VariableAssignNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ListNode, ReturnNode]
