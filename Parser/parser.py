from mysqlx import Expr
from tokens import *
from nodes import *

def IncrementIndex(tokens, index):
    return index + 1 if index < len(tokens) - 1 else index

def BinaryOperation(f, acceptedTokens, tokens, index):
    left, index = f(tokens, index)
    while type(tokens[index]) in acceptedTokens:
        operator = tokens[index]
        index = IncrementIndex(tokens, index)
        right, index = f(tokens, index)
        left = BinaryOperationNode(left, operator, right)
    return left, index

def Arithmic(tokens, index):
    return BinaryOperation(Term, (Plus, Minus), tokens, index)

def Comparision(tokens, index):
    return BinaryOperation(Arithmic, (Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals), tokens, index)

def Expression(tokens, index):
    if type(tokens[index]) == Variable:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != Identifier: 
            raise Exception("Expected Identifier Token")
        name = tokens[index]
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != Assign: 
            raise Exception("Expected Assign Token")
        index = IncrementIndex(tokens, index)
        expression, index = Expression(tokens, index)
        return VariableAssignNode(name, expression), index

    return BinaryOperation(Comparision, (And, Or), tokens, index)

def IfStatement(tokens, index):
    cases = []
    elseCase = None
    condition, index = Expression(tokens, index)
    if type(tokens[index]) != Then:
        raise Exception("Expected Then token..")
    index = IncrementIndex(tokens, index)
    expression, index = Expression(tokens, index)
    cases.append((condition, expression))

    while type(tokens[index]) == Elif:
        index = IncrementIndex(tokens, index)
        condition, index = Expression(tokens, index)
        if type(tokens[index]) != Then:
            raise Exception("Expected Then token..")
        index = IncrementIndex(tokens, index)
        expression, index = Expression(tokens, index)
        cases.append((condition, expression))    

    if type(tokens[index]) == Else:
        index = IncrementIndex(tokens, index)
        elseCase, index = Expression(tokens, index)
    return IfNode(cases, elseCase), index

def WhileLoop(tokens, index):
    condition, index = Expression(tokens, index)
    if type(tokens[index]) != Then:
        raise Exception("Expected Then token..")
    index = IncrementIndex(tokens, index)
    body, index = Expression(tokens, index)
    return WhileNode(condition, body), index

def FunctionDefenition(tokens, index):
    if type(tokens[index]) == Identifier:
        token = tokens[index] 
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != LPar:
            raise Exception("Expected Param token..")
    else:
        token = None       
    if type(tokens[index]) != LPar:
        raise Exception("Expected Identifier or LPar token..")
    
    index = IncrementIndex(tokens, index)
    arguments = []
    if type(tokens[index]) == Identifier:
        arguments.append(tokens[index]) 
        index = IncrementIndex(tokens, index)

        while type(tokens[index]) == Comma:
            index = IncrementIndex(tokens, index)
            if type(tokens[index]) == Identifier:
                arguments.append(tokens[index])
                index = IncrementIndex(tokens, index)
            else:
                raise Exception("Expected Identifier token..")

        if type(tokens[index]) != RPar:
            raise Exception("Expected RPar token..")
    else:
        if type(tokens[index]) != RPar:
            raise Exception("Expected RPar token..")

    index = IncrementIndex(tokens, index)   
    if type(tokens[index]) != Arrow:
        raise Exception("Expected Arrow token..")

    index = IncrementIndex(tokens, index)
    expression, index = Expression(tokens, index)
    return FunctionAssignNode(token, arguments, expression), index     

def CallFunction(tokens, index):
    factor, index = Factor(tokens, index)
    if type(tokens[index]) == LPar:
        index = IncrementIndex(tokens, index)
        arguments = []

        if type(tokens[index]) == RPar:
            index = IncrementIndex(tokens, index)
        else:
            expression, index = Expression(tokens, index)
            arguments.append(expression)

            while type(tokens[index]) == Comma:
                index = IncrementIndex(tokens, index)
                expression, index = Expression(tokens, index)
                arguments.append(expression)

            if type(tokens[index]) != RPar:
                raise Exception("Expected RPar token..")
            index = IncrementIndex(tokens, index)
        return FunctionCallNode(factor, arguments), index
    return factor, index

def Factor(tokens, index):
    token = tokens[index]
    index = IncrementIndex(tokens, index)
    if type(token) in (Int, Float):
        return NumberNode(token), index
    elif type(token) == Identifier:
        return VariableAccessNode(token), index
    elif type(token) == LPar:
        expression, index = Expression(tokens, index)
        if type(tokens[index]) == RPar:
            return expression, IncrementIndex(tokens, index)
    elif type(token) == If:
        return IfStatement(tokens, index)
    elif type(token) == While:
        return WhileLoop(tokens, index)
    elif type(token) == FunctionDef:
        return FunctionDefenition(tokens, index)
    elif type(token) == Run:
        return CallFunction(tokens, index)

def Term(tokens, index):
    return BinaryOperation(Factor, (Multiply, Divide), tokens, index)

def Parse(tokens, index):
    return Expression(tokens, index)[0]