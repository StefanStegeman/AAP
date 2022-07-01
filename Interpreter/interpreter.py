from Interpreter.function import Function
from Interpreter.nodes import *
from Interpreter.number import Number
from Interpreter.tokens import *
from Interpreter.context import Context
from typing import Optional
from itertools import chain
from functools import reduce, partial
from operator import add, is_not

def VisitNode(node: 'AllNodes', context: Context) -> Number:
    """ Visit the passed Node's function and interpret this.
    Every node has a Visit{node} function which is responsible for interpreting that node. 
    Haskell notation:
        VisitNode :: Node -> Context -> Number
    Parameters:
        node (Node): The node which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of the AST.
    """
    method = globals()[f'Visit{type(node).__name__}']
    try:
        return method(node, context)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def VisitNumberNode(node: NumberNode, context: Context) -> Number:
    """ Interpret a NumberNode. 
    Haskell notation:
        VisitNumberNode :: NumberNode -> Context -> Number
    Parameters:
        node (NumberNode): The NumberNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the NumberNode.
    """
    return Number(node.token.value, context)

def VisitReturnNode(node: ReturnNode, context: Context) -> Optional[Number]:
    """ Interpret a ReturnNode. 
    Haskell notation:
        VisitReturnNode :: ReturnNode -> Context -> Number | None
    Parameters:
        node (ReturnNode): The ReturnNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the ReturnNode.
        None will be returned if there is no node to return.
    """
    if node.node:
        return VisitNode(node.node, context)

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context) -> Number:
    """ Interpret a BinaryOperationNode. 
    Haskell notation:
        VisitBinaryOperationNode :: BinaryOperationNode -> Context -> Number
    Parameters:
        node (BinaryOperationNode): The BinaryOperationNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the BinaryOperationNode.
    """
    left = VisitNode(node.left, context)
    right = VisitNode(node.right, context)
    method = getattr(left, f'{type(node.operator).__name__}')
    try:
        return method(right)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def VisitVariableAssignNode(node: VariableAssignNode, context: Context) -> Number:
    """ Interpret a VariableAssignNode.
    Haskell notation:
        VisitVariableAssignNode :: VariableAssignNode -> Context -> Number 
    Parameters:
        node (VariableAssignNode): The VariableAssignNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the VariableAssignNode.
    """
    name = node.token.value
    value = VisitNode(node.node, context)
    context.symbolDictionary.SetValue(name, value)
    return value

def VisitVariableAccessNode(node: VariableAccessNode, context: Context) -> Number:
    """ Interpret a VariableAccessNode. 
    Haskell notation:
        VisitVariableAccessNode :: VariableAccessNode -> Context -> Number
    Parameters:
        node (VariableAccessNode): The VariableAccessNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the VariableAccessNode.
    """
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        raise Exception(f"No value found for '{name}'..")
    return value

def VisitListNode(node: ListNode, context: Context) -> Union[List[Number], Number]:
    """ Interpret a ListNode. 
    Haskell notation:
        VisitListNode :: ListNode -> Context -> Number | [Number]
    Parameters:
        node (ListNode): The ListNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the VariableAssignNode.
        numbers (Lst): A list filled with the results of interpreted nodes.
    """
    returnNodes = map(lambda element: ReturnNode == type(element), node.elements)
    returns = reduce(add, returnNodes, 0)

    def VisitElement(element: 'AllNodes') -> Number:
        """ Visit element of list.
        Haskell notation:
            VisitElement :: Node -> Number
        Parameters: 
            element (Node): An element from the ListNode which will be interpreted.
        Returns:
            number (Number): The result of interpreting the node.
        """
        if not returns:
            return VisitNode(element, context)
        if type(element) == ReturnNode:
            return VisitNode(element, context)
        VisitNode(element, context)

    elements = []
    elements = list(chain(*map(lambda node: [*elements, VisitElement(node)], node.elements)))
    elements = list(filter(partial(is_not, None), elements))
    if len(elements) != 1:
        return elements
    return elements[0]

def VisitIfNode(node: IfNode, context: Context) -> Optional[Number]:
    """ Interpret an IfNode. 
    Haskell notation:
        VisitIfNode :: IfNode -> Context -> Number | None
    Parameters:
        node (IfNode): The IfNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    condition, expression = node.case
    value = VisitNode(condition, context)
    if value.IsTrue():
        return VisitNode(expression, context) 
    if node.elseCase:
        expression = node.elseCase
        return VisitNode(expression, context)
    return

def VisitWhileNode(node: WhileNode, context: Context, elements: List = []) -> None:
    """ Interpret a WhileNode. 
    Haskell notation:
        VisitWhileNode :: WhileNode -> Context -> None
    Parameters:
        node (WhileNode): The WhileNode which will be interpreted.
        context (Context): The current existing context.
    """
    condition = VisitNode(node.condition, context)
    if condition.IsTrue():
        elements.append(VisitNode(node.body, context))
        return VisitWhileNode(node, context, elements)
    return

def VisitFunctionDefenitionNode(node: FunctionDefenitionNode, context: Context) -> Function:
    """ Interpret a FunctionDefenitionNode. 
    Haskell notation:
        VisitFunctionDefenitionNode :: FunctionDefenitionNode -> Context -> Function
    Parameters:
        node (FunctionDefenitionNode): The FunctionDefenitionNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the FunctionDefenitionNode.
        None will be returned if there is no node to return.
    """
    function = Function(node.token.value, node.arguments, node.body, context) 
    if node.token:
        context.symbolDictionary.SetValue(node.token.value, function)
    return function

def VisitFunctionCallNode(node: FunctionCallNode, context: Context) -> Number:
    """ Interpret a FunctionCallNode. 
    Haskell notation:
        VisitFunctionCallNode :: FunctionCallNode -> Context -> Number
    Parameters:
        node (FunctionCallNode): The FunctionCallNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the FunctionDefenitionNode.
    """
    arguments = [] 
    function = VisitNode(node.node, context)
    arguments = list(chain(*map(lambda node: [*arguments, VisitNode(node, context)], node.arguments)))
    return function.Execute(arguments)

AllNodes = Union[NumberNode, VariableAccessNode, BinaryOperationNode, VariableAccessNode, VariableAssignNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ListNode, ReturnNode]