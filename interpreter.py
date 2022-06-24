from nodes import *
from number import Number
from tokens import *

def VisitNode(node, context):
    method = globals()[f'Visit{type(node).__name__}']
    return method(node, context)

def VisitNumberNode(node, context):
    return Number(node.token.value, context)

def VisitBinaryOperationNode(node, context):
    left = VisitNode(node.left, context)
    right = VisitNode(node.right, context)

    method = getattr(left, f'{type(node.operator).__name__}')
    try:
        return method(right)
    except:
        raise Exception("No method found..")
