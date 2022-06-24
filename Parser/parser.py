from tokens import *
from nodes import *

def IncrementIndex(tokens, index):
    return index + 1 if index < len(tokens) - 1 else index

def Parse(tokens, index):
    return Expression(tokens, index)[0]

def Factor( tokens, index):
    token = tokens[index]
    if type(token) in (Int, Float):
        index = IncrementIndex(tokens, index)
        return NumberNode(token), index
    elif type(token) == LPar:
        index = IncrementIndex(tokens, index)
        expression = Expression(tokens, index)
        if tokens[index] == RPar:
            index = IncrementIndex(tokens, index)
            return expression

def Term(tokens, index):
    return BinaryOperation(Factor, (Multiply, Divide), tokens, index)

def Expression(tokens, index):
    return BinaryOperation(Term, (Plus, Minus), tokens, index)

def BinaryOperation(f, acceptedTokens, tokens, index):
    left, index = f(tokens, index)
    while type(tokens[index]) in acceptedTokens:
        operator = tokens[index]
        index = IncrementIndex(tokens, index)
        right, index = f(tokens, index)
        left = BinaryOperationNode(left, operator, right)
    return left, index