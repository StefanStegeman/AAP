from Parser.parser import WhileLoop
from nodes import *
from number import Number
from tokens import *
from context import Context

def VisitNode(node, context: Context):
    method = globals()[f'Visit{type(node).__name__}']
    return method(node, context)

def VisitNumberNode(node: NumberNode, context: Context):
    return Number(node.token.value, context)

def VisitBinaryOperationNode(node: BinaryOperationNode, context: Context):
    left = VisitNode(node.left, context)
    right = VisitNode(node.right, context)

    method = getattr(left, f'{type(node.operator).__name__}')
    try:
        return method(right)
    except:
        raise Exception("No method found..")

def VisitVariableAssignNode(node: VariableAssignNode, context: Context):
    name = node.token.value
    value = VisitNode(node.node, context)
    context.symbolDictionary.SetValue(name, value)
    return value

def VisitVariableAccessNode(node: VariableAccessNode, context: Context):
    name = node.token.value
    value = context.symbolDictionary.GetValue(name)
    if not value:
        Exception("No value found..")
    return value

def VisitIfNode(node: IfNode, context: Context):
    for condition, expression in node.cases:
        value = VisitNode(condition, context)
        if value.IsTrue():
            return VisitNode(expression, context) 
    if node.elseCase:
        return VisitNode(node.elseCase, context)
            
def VisitWhileNode(node: WhileNode, context: Context):
    while True:
        condition = VisitNode(node.condition, context)
        if not condition.IsTrue(): break
        VisitNode(node.body, context)