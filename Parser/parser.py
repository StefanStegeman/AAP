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
            raise Exception(f"Expected Identifier..")
        name = tokens[index]
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != Assign: 
            raise Exception(f"Expected '{Assign.value}'..")
        index = IncrementIndex(tokens, index)
        expression, index = Expression(tokens, index)
        return VariableAssignNode(name, expression), index

    return BinaryOperation(Comparision, (And, Or), tokens, index)

def IfB(tokens, index):
    return IfCases(Elif, tokens, index)

def IfC(tokens, index):
    elseCase = None
    if type(tokens[index]) == Else:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) == NewLine:
            index = IncrementIndex(tokens, index)
            statements, index = Statements(tokens, index)
            elseCase = statements

            if type(tokens[index]) == End:
                index = IncrementIndex(tokens, index)
            else:
                print(f"Expected {End.value} token..")
                raise Exception(f"Expected {End.value} Token..")
        else:
            expression, index = Statement(tokens, index)
            elseCase = expression
    return elseCase, index

def IfBORC(tokens, index):
    cases, elseCase = [], None
    if type(tokens[index]) == Elif:
        allCases, index = IfB(tokens, index)
        cases, elseCase = allCases
    else:
        elseCase, index = IfC(tokens, index)
    return (cases, elseCase), index

def IfCases(token, tokens, index):
    cases = []
    elseCase = None
    if not type(tokens[index]) == token:
        print(f"Expected {token.value} token..")
        raise Exception(f"Expected {token.value} token..")
    index = IncrementIndex(tokens, index)
    condition, index = Expression(tokens, index)

    if not type(tokens[index]) == Then:
        print(f"Expected {Then.value} token..")
        raise Exception(f"Expected {Then.value} token..")

    index = IncrementIndex(tokens, index)

    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        statements, index = Statements(tokens, index)
        cases.append((condition, statements)) 

        if type(tokens[index]) == End:
            index = IncrementIndex(tokens, index)
        else:
            allCases, index = IfBORC(tokens, index)
            newCases, elseCase = allCases
            cases.extend(newCases)
    else:
        expression, index = Statement(tokens, index)
        # expression, index = Expression(tokens, index)
        cases.append((condition, expression))
        allCases, index = IfBORC(tokens, index)
        newCases, elseCase = allCases
        cases.extend(newCases)
    return (cases, elseCase), index

def IfStatement(tokens, index):
    allCases, index = IfCases(If, tokens, index - 1)
    cases, elseCase = allCases
    return IfNode(cases, elseCase), index

def WhileLoop(tokens, index):
    condition, index = Expression(tokens, index)
    if type(tokens[index]) != Then:
        print(f"Expected {Then.value} token..")
        raise Exception("Expected Then token..")
    index = IncrementIndex(tokens, index)
    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        body, index = Statements(tokens, index)
        if not type(tokens[index]) == End:
            print(f"Expected {End.value} token..")
            raise Exception(f"Expected {End.value} Token..")
        index = IncrementIndex(tokens, index)
        # return WhileNode(condition, body, True), index
        return WhileNode(condition, body), index

    print("Before: \t",tokens[index])
    index = IncrementIndex(tokens, index) # Is Deze nodig?
    print("After: \t", tokens[index])
    body, index = Statement(tokens, index)
    # body, index = Expression(tokens, index)
    return WhileNode(condition, body), index

def FunctionDefenition(tokens, index):
    if type(tokens[index]) == Identifier:
        token = tokens[index] 
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != LPar:
            raise Exception(f"Expected '{LPar.value}'..")
    else:
        token = None       
        if type(tokens[index]) != LPar:
            raise Exception(f"Expected Identifier or '{LPar.value}'..")
    
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
                raise Exception(f"Expected Identifier..")

        if type(tokens[index]) != RPar:
            print(f"Expected {RPar.value} token..")
            raise Exception("Expected RPar token..")
    else:
        if type(tokens[index]) != RPar:
            print(f"Expected {RPar.value} token..")
            raise Exception("Expected RPar token..")

    index = IncrementIndex(tokens, index)   
    if type(tokens[index]) == Arrow:
        index = IncrementIndex(tokens, index)
        body, index = Expression(tokens, index)
        return FunctionAssignNode(token, arguments, body), index     
    if type(tokens[index]) != NewLine:
        raise Exception(f"Expected {Arrow.value} or Newline after the assignment of '{FunctionAssignNode.value}' '{token}'..")
    index = IncrementIndex(tokens, index)
    body, index = Statements(tokens, index)
    # body, index = Expression(tokens, index)
    if type(tokens[index]) != End:
        raise Exception(f"Expected {End.value} Token..")
    index = IncrementIndex(tokens, index)
    return FunctionAssignNode(token, arguments, body), index  

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
                print("Expected RPar token..")
                raise Exception("Expected RPar token..")
            index = IncrementIndex(tokens, index)
        return FunctionCallNode(factor, arguments), index
    return factor, index

def List(tokens, index):
    elements = []
    if type(tokens[index]) == ListClose:
        index = IncrementIndex(tokens, index)
    else:
        expression, index = Expression(tokens, index)
        elements.append(expression)

        while type(tokens[index]) == Comma:
            index = IncrementIndex(tokens, index)
            expression, index = Expression(tokens, index)
            elements.append(expression)

        if type(tokens[index]) != ListClose:
            print(f"Expected {ListClose.value} token..")
            raise Exception("Expected ListClose token..")
        index = IncrementIndex(tokens, index)
    return ListNode(elements), index

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
    elif type(token) == Return:
        expression, index = Expression(tokens, index)
        return ReturnNode(expression), index
    elif type(token) == ListOpen:
        list, index = List(tokens, index)
        return list, index

def Try(oldIndex, expression):
    if expression[0] == None:
        return expression[0], oldIndex
    return expression

def Statement(tokens, index):
    if type(tokens[index]) == Return:
        index = IncrementIndex(tokens, index)
        expression, index = Try(index, Expression(tokens, index)) 
        return ReturnNode(expression), index
    return Expression(tokens, index)

def Statements(tokens, index):
    statements = []
    while type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
    
    statement, index = Statement(tokens, index)
    statements.append(statement)

    moreStatements = True
    while moreStatements:
        newLine = 0
        while type(tokens[index]) == NewLine:
            index = IncrementIndex(tokens, index)
            newLine += 1
        if newLine == 0:
            moreStatements = False
        if not moreStatements: break

        statement, index = Try(index, Statement(tokens, index))
        if not statement:
            moreStatements = False
            continue
        statements.append(statement)
    return ListNode(statements), index

def Term(tokens, index):
    return BinaryOperation(Factor, (Multiply, Divide), tokens, index)

def Parse(tokens, index):
    print(tokens)
    statements, index = Statements(tokens, index)
    if type(tokens[index]) == EOF:
        return statements