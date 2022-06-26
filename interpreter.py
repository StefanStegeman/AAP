from nodes import *
from number import Number
from tokens import *
from context import Context, SymbolDictionary
from copy import deepcopy

class List:
    def __init__(self, elements, context = None) -> None:
        self.elements = elements
        self.context = context

    def Plus(self, other):
        lst = deepcopy(self)
        lst.elements.append(other)
        return lst

    def Minus(self, other):
        if isinstance(other, Number):
            lst = deepcopy(self)
            for item in lst.elements:
                if item.value == other.value:
                    lst.elements.remove(item)
                return lst
        else:
            raise Exception(f"Element needs to be a number..")

    def __repr__(self) -> str:
        return f'[{", ".join([str(x) for x in self.elements])}]'

class Function:
    def __init__(self, name, arguments, body, context) -> None:
        self.name = name
        self.arguments = arguments
        self.body = body
        self.context = context
        # self.context = Context(self.context)
        # self.context.symbolDictionary = SymbolDictionary(self.context.parent.symbolDictionary)

    def Execute(self, arguments):
        context = Context(self.context)
        if self.context.parent:
            context.symbolDictionary = SymbolDictionary(self.context.parent.symbolDictionary)
        else:
            context.symbolDictionary = SymbolDictionary(self.context.symbolDictionary)
        if len(arguments) > len(self.arguments):
            raise Exception(f"Too many arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")
        elif len(arguments) < len(self.arguments):
            raise Exception(f"Too little arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")
        
        for i in range(len(arguments)):
            name = self.arguments[i]
            value = arguments[i]
            value.context = context
            context.symbolDictionary.SetValue(name.value, value)
            
        return VisitNode(self.body, context)

def VisitNode(node, context: Context):
    method = globals()[f'Visit{type(node).__name__}']
    try:
        return method(node, context)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def VisitListNode(node: ListNode, context: Context):
    elements = []
    for element in node.elements:
        elements.append(VisitNode(element, context))
    return List(elements, context)

def VisitNumberNode(node: NumberNode, context: Context):
    return Number(node.token.value, context)

def VisitReturnNode(node: ReturnNode, context: Context):
    if node.node:
        return VisitNode(node.node, context)
    else:
        return Number.null

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context):
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
    name = node.token.value
    value = VisitNode(node.node, context)
    context.symbolDictionary.SetValue(name, value)
    return value

def VisitVariableAccessNode(node: VariableAccessNode, context: Context):
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        raise Exception(f"No value found for '{name}'..")
    return value

def VisitIfNode(node: IfNode, context: Context):
    for condition, expression in node.cases:
        value = VisitNode(condition, context)
        if value.IsTrue():
            return VisitNode(expression, context) 
    if node.elseCase:
        expression = node.elseCase
        return VisitNode(expression, context)
    return Number.null
            
def VisitWhileNode(node: WhileNode, context: Context):
    elements = []
    while True:
        condition = VisitNode(node.condition, context)
        if not condition.IsTrue(): break
        elements.append(VisitNode(node.body, context))
    return List(elements, context)

def VisitFunctionAssignNode(node: FunctionAssignNode, context: Context):
    arguments = [name for name in node.arguments]
    function = Function(node.token.value, arguments, node.body, context) 
    if node.token:
        context.symbolDictionary.SetValue(node.token.value, function)
    return function

def VisitFunctionCallNode(node: FunctionCallNode, context: Context):
    arguments = []
    function = VisitNode(node.node, context) #Copy nodig?
    for argument in node.arguments:
        arguments.append(VisitNode(argument, context))
    return function.Execute(arguments)