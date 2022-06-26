from ast import NotEq
from tokens import *
from typing import Union

class NumberNode:
    """ Store a Number value in this Node."""
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Assign the token which contains the number value. 
        
        Parameters:
            token (Int, Float) : The toen which contains the number value.
        """
        self.token = token
    
    def __str__(self):
        """ Represent token as string. """
        return f'{self.token}'

class VariableAccessNode:
    def __init__(self, token: Union[Int, Float]) -> None:
        self.token = token

class BinaryOperationNode:
    """ Store the nodes and operator token needed for a binary operation in this Node. """
    def __init__(self, left: Union[VariableAccessNode, NumberNode], operator: 'OperatorTokens', right: Union[VariableAccessNode, NumberNode]) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.operator}, {self.right})'

class VariableAssignNode:
    def __init__(self, token: Identifier, node: Union[VariableAccessNode, NumberNode]) -> None:
        self.token = token
        self.node = node


class IfNode:
    def __init__(self, cases, elseCase) -> None:
        self.cases = cases
        self.elseCase = elseCase
        
class WhileNode:
    def __init__(self, condition: VariableAccessNode, body) -> None:
        self.condition = condition
        self.body = body

class FunctionAssignNode:
    def __init__(self, token, arguments, body):
        self.token = token
        self.arguments = arguments
        self.body = body

class FunctionCallNode:
    def __init__(self, node, arguments):
        self.node = node
        self.arguments = arguments

class ListNode:
    def __init__(self, elements) -> None:
        self.elements = elements

class ReturnNode:
    def __init__(self, node) -> None:
        self.node = node

OperatorTokens = Union[Plus, Minus, Divide, Multiply, Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals, And, Or]