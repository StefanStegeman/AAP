from ast import Num
from Interpreter.function import Function
from Interpreter.nodes import *
from Interpreter.number import Number
from Interpreter.tokens import *
from Interpreter.context import Context, SymbolDictionary
from typing import Optional
from itertools import chain
from functools import reduce, partial
from operator import add, is_not

def VisitNode(node: 'AllNodes', context: Context) -> 'Number':
    """ Visit the passed Node's function.
    Every node has a 'Visit' + node function which is responsible for interpreting that node. 
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
    """ Interpret a NumberNode 
    Parameters:
        node (NumberNode): The NumberNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        number (Number): The result of interpreting the NumberNode.
    """
    return Number(node.token.value, context)

def VisitReturnNode(node: ReturnNode, context: Context) -> Optional[Number]:
    """ Interpret a ReturnNode 
    Parameters:
        node (ReturnNode): The ReturnNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    if node.node:
        return VisitNode(node.node, context)

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context) -> Number:
    """ Interpret a BinaryOperationNode 
    Parameters:
        node (BinaryOperationNode): The BinaryOperationNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
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
    """ Interpret a VariableAssignNode 
    Parameters:
        node (VariableAssignNode): The VariableAssignNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    name = node.token.value
    value = VisitNode(node.node, context)
    context.symbolDictionary.SetValue(name, value)
    return value

def VisitVariableAccessNode(node: VariableAccessNode, context: Context) -> Number:
    """ Interpret a VariableAccessNode 
    Parameters:
        node (VariableAccessNode): The VariableAccessNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        raise Exception(f"No value found for '{name}'..")
    return value

def VisitListNode(node: ListNode, context: Context) -> Union[List[Number], Number]:
    """ Interpret a ListNode 
    Parameters:
        node (ListNode): The ListNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    returnNodes = map(lambda element: ReturnNode == type(element), node.elements)
    returns = reduce(add, returnNodes, 0)

    def VisitElement(element) -> Number:
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
    """ Interpret an IfNode 
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
    """ Interpret a WhileNode 
    Parameters:
        node (WhileNode): The WhileNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    condition = VisitNode(node.condition, context)
    if condition.IsTrue():
        elements.append(VisitNode(node.body, context))
        return VisitWhileNode(node, context, elements)
    return

def VisitFunctionDefenitionNode(node: FunctionDefenitionNode, context: Context) -> Function:
    """ Interpret a FunctionDefenitionNode 
    Parameters:
        node (FunctionDefenitionNode): The FunctionDefenitionNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    function = Function(node.token.value, node.arguments, node.body, context) 
    if node.token:
        context.symbolDictionary.SetValue(node.token.value, function)
    return function

def VisitFunctionCallNode(node: FunctionCallNode, context: Context) -> Number:
    """ Interpret a FunctionCallNode 
    Parameters:
        node (FunctionCallNode): The FunctionCallNode which will be interpreted.
        context (Context): The current existing context.
    Returns:
        
    """
    arguments = [] 
    function = VisitNode(node.node, context)
    arguments = list(chain(*map(lambda node: [*arguments, VisitNode(node, context)], node.arguments)))
    return function.Execute(arguments)

AllNodes = [NumberNode, VariableAccessNode, BinaryOperationNode, VariableAccessNode, VariableAssignNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ListNode, ReturnNode]