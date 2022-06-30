from Interpreter.tokens import *
from typing import Union, List

class NumberNode:
    """ This class stores the value of a NumberNode."""
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
    """ This class stores the value of a VariableAccesNode. """
    def __init__(self, token: Union[Int, Float]) -> None:
        """ Initialize the VariableAccessNode. 
        Parameters:
            token (Int, Float): The token which is being stored.
        """
        self.token = token

    def __str__(self) -> str:
        """ Represent VariableAccessNode as string. """
        return f'{self.token}'

    def __repr__(self) -> str:
        """ Represent VariableAccessNode as string. """
        return f"{self.token}"

class BinaryOperationNode:
    """ This class stores the value of a BinaryOperationNode. """
    def __init__(self, left: Union[VariableAccessNode, NumberNode], operator: 'OperatorTokens', right: Union[VariableAccessNode, NumberNode]) -> None:
        """ Initialize the BinaryOperationNode. 
        Parameters:
            left (VariableAccessNode, NumberNode):
            operator (OperatorTokens):
            right (VariableAccessNode, NumberNode):
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        """ Represent BinaryOperationNode as string. """
        return f'({self.token}, {self.operator}, {self.right})'

    def __repr__(self):
        """ Represent BinaryOperationNode as string. """
        return f'({self.left}, {self.operator}, {self.right})'

class VariableAssignNode:
    """ This class stores the value of a VariableAssignNode. """
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
    """ This class stores the value of a ListNode. """
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
    """ This class stores the value of an IfNode. """
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
    """ This class stores the value of a WhileNode. """
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

class FunctionAssignNode:
    """ This class stores the value of a FunctionAssignNode. """
    def __init__(self, token, arguments, body):
        """ Initialize the FunctionAssignNode. 
        Parameters:
            token (Token):
            arguments ():
            body ():
        """
        self.token = token
        self.arguments = arguments
        self.body = body

    def __str__(self) -> str:
        """ Represent FunctionAssignNode as string. """
        return f'({self.token}, {self.arguments}, {self.body})'

class FunctionCallNode:
    """ This class stores the value of a FunctionCallNode. """
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
    """ This class stores the value of a ReturnNode. """
    def __init__(self, node) -> None:
        """ Initialize the ReturnNode. 
        Parameters:
            node () :
        """
        self.node = node

    def __str__(self) -> str:
        """ Represent ReturnNode as string. """
        return f'{self.node}'

OperatorTokens = Union[Plus, Minus, Divide, Multiply, Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals, And, Or]