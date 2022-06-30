from Interpreter.tokens import *
from typing import Union, List

class NumberNode:
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Initialize the NumberNode. 
        Parameters:
            token (Int, Float): The token which contains the number value.
        """
        self.token = token
    
    def __str__(self) -> str:
        """ Represent NumberNode as string. """
        return f'{self.token}'

class VariableAccessNode:
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Initialize the VariableAccessNode. 
        Parameters:
            token (Int, Float): The token which is being stored.
        """
        self.token = token

    def __str__(self) -> str:
        """ Represent VariableAccessNode as string. """
        return f'{self.token}'

class BinaryOperationNode:
    def __init__(self, left: 'Node', operator: 'OperatorTokens', right: 'Node') -> None:
        """ Initialize the BinaryOperationNode. 
        Parameters:
            left (VariableAccessNode, NumberNode): The left node for the binary operation.
            operator (OperatorTokens): The operator node for the binary operation.
            right (VariableAccessNode, NumberNode): The right node for the binary operation.
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        """ Represent BinaryOperationNode as string. """
        return f'({self.token}, {self.operator}, {self.right})'

class VariableAssignNode:
    def __init__(self, token: Identifier, node: Union[VariableAccessNode, NumberNode]) -> None:
        """ Initialize the VariableAssignNode. 
        Parameters:
            token (Identifier):
            node (VariableAccessNode, NumberNode):
        """
        self.token = token
        self.node = node

    def __str__(self) -> str:
        """ Represent VariableAssignNode as string. """
        return f'({self.token}, {self.node})'

class ListNode:
    def __init__(self, elements: List[VariableAccessNode]) -> None:
        """ Initialize the ListNode. 
        Parameters:
            elements (Lst):
        """
        self.elements = elements

    def __str__(self) -> str:
        """ Represent ListNode as string. """
        return f'{self.elements}'

class IfNode:
    def __init__(self, case, elseCase: ListNode) -> None:
        """ Initialize the IfNode. 
        Parameters:
            case (Lst): The case which contains a condition and the expression.
            elseCase (): An expression which will be executed.
        """
        self.case = case
        self.elseCase = elseCase

    def __str__(self) -> str:
        """ Represent IfNode as string. """
        return f'({self.case}, {self.elseCase})'
        
class WhileNode:
    def __init__(self, condition: VariableAccessNode, body) -> None:
        """ Initialize the WhileNode. 
        Parameters:
            condition (VariableAccessNode):
            body ():
        """
        self.condition = condition
        self.body = body

    def __str__(self) -> str:
        """ Represent WhileNode as string. """
        return f'({self.condition}, {self.body})'

class FunctionDefenitionNode:
    def __init__(self, token, arguments, body):
        """ Initialize the FunctionDefenitionNode. 
        Parameters:
            token (Token):
            arguments ():
            body ():
        """
        self.token = token
        self.arguments = arguments
        self.body = body

    def __str__(self) -> str:
        """ Represent FunctionDefenitionNode as string. """
        return f'({self.token}, {self.arguments}, {self.body})'

class FunctionCallNode:
    def __init__(self, node: VariableAccessNode, arguments: List[VariableAccessNode]):
        """ Initialize the FunctionCallNode. 
        Parameters:
            node (VariableAccessNode): The function which will be called.
            arguments (List[VariableAccessNode]): The arguments for the function call.
        """
        self.node = node
        self.arguments = arguments

    def __str__(self) -> str:
        """ Represent FunctionCallNode as string. """
        return f'({self.node}, {self.arguments})'

class ReturnNode:
    def __init__(self, node: 'Node') -> None:
        """ Initialize the ReturnNode. 
        Parameters:
            node (Node): The node which will be called on returning.
        """
        self.node = node

    def __str__(self) -> str:
        """ Represent ReturnNode as string. """
        return f'{self.node}'

OperatorTokens = Union[Plus, Minus, Divide, Multiply, Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals, And, Or]
Node = Union[NumberNode, VariableAccessNode, BinaryOperationNode, VariableAssignNode, ListNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ReturnNode]