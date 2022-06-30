from Interpreter.nodes import *
from Interpreter.number import Number
from Interpreter.tokens import *
from Interpreter.nodes import *
from Interpreter.context import Context, SymbolDictionary
from typing import Callable
from itertools import chain
from functools import reduce, partial
from operator import add, is_not

class Function:
    """ Function class which makes it easier to execute a function."""
    def __init__(self, name, arguments, body, context) -> None:
        """ Initialize the function class. 
        Parameters:
            name (str)        : The name of the function. 
            arguments (Lst)   : The arguments for the function.
            body (Node)       : The body of the function in the form of a Node.
            context (context) : The context for the function.
        """
        self.name = name
        self.arguments = arguments
        self.body = body
        self.context = context

    def Execute(self, arguments):
        """ Execute the function's body. 
        
        Parameters:
            arguments (Lst) : The arguments passed into the function.
        """
        context = Context(self.context)
        context.symbolDictionary = SymbolDictionary(self.context.symbolDictionary)
        if len(arguments) > len(self.arguments):
            raise Exception(f"Too many arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")
        elif len(arguments) < len(self.arguments):
            raise Exception(f"Too little arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")

        def SetArguments(index, localContext):
            if index < len(arguments):
                name = self.arguments[index]
                value = arguments[index]
                value.context = localContext
                localContext.symbolDictionary.SetValue(name.value, value)
                return SetArguments(index + 1, localContext) 
            return localContext
        context = SetArguments(0, context)
        return VisitNode(self.body, context)

def VisitNode(node: 'AllNodes', context: Context):
    """ VisitNode 
    Parameters:
        node (Node)       :
        context (Context) :
    Returns:

    """
    method = globals()[f'Visit{type(node).__name__}']
    try:
        return method(node, context)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def VisitNumberNode(node: NumberNode, context: Context):
    """ VisitNumberNode 
    Parameters:
        node (NumberNode) :
        context (Context) :
    Returns:
        number (Number)   : A new instance of the Number class.
    """
    return Number(node.token.value, context)

def VisitReturnNode(node: ReturnNode, context: Context):
    """ VisitReturnNode 
    Parameters:
        node (ReturnNode) :
        context (Context) :
    Returns:
        
    """
    if node.node:
        return VisitNode(node.node, context)

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context):
    """ VisitBinaryOperationNode 
    Parameters:
        node (BinaryOperationNode) :
        context (Context)          :
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

def VisitVariableAssignNode(node: VariableAssignNode, context: Context):
    """ VisitVariableAssignNode 
    Parameters:
        node (VariableAssignNode) :
        context (Context)         :
    Returns:
        
    """
    name = node.token.value
    value = VisitNode(node.node, context)
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

    def VisitElement(element):
        if not returns:
            return VisitNode(element, context)
        if type(element) == ReturnNode:
            return VisitNode(element, context)
        VisitNode(element, context)

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
    condition, expression = node.cases
    value = VisitNode(condition, context)
    if value.IsTrue():
        return VisitNode(expression, context) 
    if node.elseCase:
        expression = node.elseCase
        return VisitNode(expression, context)
    return Number.null

def VisitWhileNode(node: WhileNode, context: Context, elements: List = []):
    """ VisitWhileNode 
    Parameters:
        node (WhileNode)  :
        context (Context) :
    Returns:
        
    """
    condition = VisitNode(node.condition, context)
    if condition.IsTrue():
        elements.append(VisitNode(node.body, context))
        return VisitWhileNode(node, context, elements)
    return

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
    return function

def VisitFunctionCallNode(node: FunctionCallNode, context: Context):
    """ VisitFunctionCallNode 
    Parameters:
        node (FunctionCallNode) :
        context (Context)       :
    Returns:
        
    """
    arguments = [] 
    function = VisitNode(node.node, context)
    arguments = list(chain(*map(lambda node: [*arguments, VisitNode(node, context)], node.arguments)))
    return function.Execute(arguments)

AllNodes = [NumberNode, VariableAccessNode, BinaryOperationNode, VariableAccessNode, VariableAssignNode, IfNode, WhileNode, FunctionAssignNode, FunctionCallNode, ListNode, ReturnNode]