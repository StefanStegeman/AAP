from tokens import *
from nodes import *

def IncrementIndex(tokens, index):
    """ Increment the index value when it's not out of bounds.
    
    Parameters:
        tokens (Lst) : List with all the tokens.
        index  (int) : The index.

    Returns:
        index (int)  : The incremented index.
    """
    return index + 1 if index < len(tokens) - 1 else index

def BinaryOperation(f, acceptedTokens, tokens, index):
    """ Create BinaryOperationNode.
    
    Parameters:
        f (Callable)         : Callable which is used to get the left and right nodes for.
        acceptedTokens (Lst) : List with all the accepted tokens.
        tokens (Lst)         : List with all the tokens.
        index (int)          : The index.

    Returns:
        node (BinaryOperationNode) : The BinaryOperation node which has been created.
        index (int)                : The index.  
    """
    left, index = f(tokens, index)

    while type(tokens[index]) in acceptedTokens:
        operator = tokens[index]
        index = IncrementIndex(tokens, index)
        right, index = f(tokens, index)
        left = BinaryOperationNode(left, operator, right)
    return left, index

def Arithmic(tokens, index):
    """ Arithmic expression.
    
    Parameters:
        tokens (List) : The list with all the tokens.
        index (int)   : The index.
    
    Returns:
        Node (Node) : The result of the BinaryOperation function call.
        index (int) : The index.
    """
    return BinaryOperation(Term, (Plus, Minus), tokens, index)

def Comparision(tokens, index):
    """ Comparison expression.
    
    Parameters:
        tokens (List) : The list with all the tokens.
        index (int)   : The index.
    
    Returns:
        Node (Node) : The result of the BinaryOperation function call.
        index (int) : The index.
    """
    return BinaryOperation(Arithmic, (Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals), tokens, index)

def Expression(tokens, index):
    """ Expression
    
    Parameters:
        tokens (List) : The list with all the tokens.
        index (int)   : The index.
    
    Returns:
        Node (VariableAssignNode) : The VariableAssignNode.
        index (int)               : The index.
    """
    if type(tokens[index]) == Variable:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != Identifier: 
            raise Exception(f"Expected Identifier token..")
        name = tokens[index]
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) != Assign: 
            raise Exception(f"Expected '{Assign.value}' token..")
        index = IncrementIndex(tokens, index)
        expression, index = Expression(tokens, index)
        return VariableAssignNode(name, expression), index
    return BinaryOperation(Comparision, (And, Or), tokens, index)

def IfC(tokens, index):
    elseCase = None
    if type(tokens[index]) == Else:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) == NewLine:
            index = IncrementIndex(tokens, index)
            statements, index = Statements(tokens, index)
            elseCase = statements

            if type(tokens[index]) == EndIf:
                index = IncrementIndex(tokens, index)
            else:
                print(f"Expected {EndIf.value} token..")
                raise Exception(f"Expected {EndIf.value} Token..")
        else:
            expression, index = Statement(tokens, index)
            elseCase = expression
    return elseCase, index

def IfBORC(tokens, index):
    cases, elseCase = [], None
    if type(tokens[index]) == Elif:
        allCases, index = IfCases(Elif, tokens, index)
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

        if type(tokens[index]) == EndIf:
            index = IncrementIndex(tokens, index)
        else:
            allCases, index = IfBORC(tokens, index)
            newCases, elseCase = allCases
            cases.extend(newCases)
    else:
        expression, index = Statement(tokens, index)
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
        raise Exception(f"Expected {Then.value} token..")
    index = IncrementIndex(tokens, index)
    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        body, index = Statements(tokens, index)
        if not type(tokens[index]) == EndWhile:
            raise Exception(f"Expected {EndWhile.value} Token..")
        index = IncrementIndex(tokens, index)
        return WhileNode(condition, body), index

    body, index = Statement(tokens, index)
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
    if type(tokens[index]) != EndFunction:
        raise Exception(f"Expected {EndFunction.value} Token..")
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
    statements, index = Statements(tokens, index)
    if type(tokens[index]) == EOF:
        return statements