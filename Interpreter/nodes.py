from Interpreter.tokens import *
from typing import Union, List

class NumberNode:
    """ This class stores the value of a Number."""
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Initialize the NumberNode. 
        Parameters:
            token (Int, Float) : The toen which contains the number value.
        """
        self.token = token
    
    def __str__(self) -> str:
        """ Represent token as string. """
        return f'{self.token}'

class VariableAccessNode:
    """ """
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Initialize the VariableAccessNode. 
        Parameters:
            token (Int, Float) : The token which is being stored.
        """
        self.token = token

class BinaryOperationNode:
    """ Store the nodes and operator token needed for a binary operation in this Node. """
    def __init__(self, left: Union[VariableAccessNode, NumberNode], operator: 'OperatorTokens', right: Union[VariableAccessNode, NumberNode]) -> None:
        """ Initialize the BinaryOperationNode. 
        Parameters:
            left (VariableAccessNode, NumberNode) :
            operator (OperatorTokens)             :
            right (VariableAccessNode, NumberNode) :
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.operator}, {self.right})'

class VariableAssignNode:
    def __init__(self, token: Identifier, node: Union[VariableAccessNode, NumberNode]) -> None:
        """ Initialize the VariableAssignNode. 
        Parameters:
            token (Identifier) :
            node (VariableAccessNode, NumberNode) :
        """
        self.token = token
        self.node = node

class ListNode:
    def __init__(self, elements: List[VariableAccessNode]) -> None:
        """ Initialize the ListNode. 
        Parameters:
            elements () :
        """
        self.elements = elements

class IfNode:
    def __init__(self, cases, elseCase: ListNode) -> None:
        """ Initialize the IfNode. 
        Parameters:
            cases (Lst) :
            elseCase () :
        """
        self.cases = cases
        self.elseCase = elseCase
        
class WhileNode:
    def __init__(self, condition: VariableAccessNode, body) -> None:
        """ Initialize the WhileNode. 
        Parameters:
            condition (VariableAccessNode) :
            body () :
        """
        self.condition = condition
        self.body = body

class FunctionAssignNode:
    def __init__(self, token, arguments, body):
        """ Initialize the FunctionAssignNode. 
        Parameters:
            token () :
            arguments () :
            body () :
        """
        self.token = token
        self.arguments = arguments
        self.body = body

class FunctionCallNode:
    def __init__(self, node: VariableAccessNode, arguments: List[VariableAccessNode]):
        """ Initialize the FunctionCallNode. 
        Parameters:
            node () :
            arguments () :
        """
        self.node = node
        self.arguments = arguments

class ReturnNode:
    def __init__(self, node) -> None:
        """ Initialize the ReturnNode. 
        Parameters:
            node () :
        """
        self.node = node

OperatorTokens = Union[Plus, Minus, Divide, Multiply, Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals, And, Or]