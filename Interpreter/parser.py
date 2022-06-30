from typing import Callable, Tuple, Union, TypeVar
from Interpreter.tokens import *
from Interpreter.nodes import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def SkipUntil(f: Callable):
    def SkipDecorator(token, tokens, index, *args):
        if type(tokens[index]) == token:
            index = IncrementIndex(tokens, index)
            index, args = f(token, tokens, index, *args)
            return SkipDecorator(token, tokens, index, args)
        return index, args[0]
    return SkipDecorator

def IncrementIndex(tokens: List[Token], index: int) -> int:
    """ Increment the index value when it's not out of bounds.
    Parameters:
        tokens (Lst) : List with the tokens which will be parsed.
        index (int)  : The index which will be used throughout the parse process.

    Returns:
        index (int)  : The incremented index.
    """
    return index + 1 if index < len(tokens) - 1 else index

def BinaryOperation(f: Callable[[A, B], C], acceptedTokens: List[Token], tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Create BinaryOperationNode.
    Parameters:
        f (Callable)         : Callable which is used to get the left and right nodes for.
        acceptedTokens (Lst) : List with all the accepted tokens.
        tokens (Lst)         : List with the tokens which will be parsed.
        index (int)          : The index which will be used throughout the parse process.               

    Returns:
        node (Node)          : The node which has been created.
        index (int)          : The incremented index.  
    """
    left, index = f(tokens, index)

    def func(lhs, i):
        if type(tokens[i]) in acceptedTokens:
            operator = tokens[i]
            i = IncrementIndex(tokens, i)
            right, i = f(tokens, i)
            lhs = BinaryOperationNode(lhs, operator, right)
            return func(lhs, i)
        else:
            return lhs, i
    return func(left, index)

def Arithmic(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Arithmic expression.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    
    Returns:
        Node (Node) : The result of the BinaryOperation function call.
        index (int) : The incremented index.
    """
    return BinaryOperation(Term, (Plus, Minus), tokens, index)

def Comparison(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Comparison expression.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    
    Returns:
        Node (Node) : The result of the BinaryOperation function call.
        index (int) : The incremented index.
    """
    return BinaryOperation(Arithmic, (Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals), tokens, index)

def Expression(tokens: List[Token], index: int) -> Tuple['Node', int]:
    """ Expression
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    
    Returns:
        Node (VariableAssignNode) : The VariableAssignNode.
        index (int)               : The incremented index.
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
    return BinaryOperation(Comparison, (And, Or), tokens, index)

def ElseStatement(tokens: List[Token], index: int) -> Tuple[ListNode, int]:
    """ ElseStatement.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        elseCase (ListNode) : The else case.
        index (int)         : The incremented index.
    """
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

def IfStatement(tokens: List[Token], index: int):
    """ IfCases.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        
        index (int)     : The incremented index.
    """
    cases = None
    elseCase = None
    if not type(tokens[index]) == If:
        print(f"Expected {If.value} token..")
        raise Exception(f"Expected {If.value} token..")
    index = IncrementIndex(tokens, index)
    condition, index = Expression(tokens, index)

    if not type(tokens[index]) == Then:
        raise Exception(f"Expected {Then.value} token..")

    index = IncrementIndex(tokens, index)

    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        statements, index = Statements(tokens, index)
        cases = (condition, statements)

        if type(tokens[index]) == EndIf:
            index = IncrementIndex(tokens, index)
        else:
            elseCase, index = ElseStatement(tokens, index)
    else:
        expression, index = Statement(tokens, index)
        cases = (condition, expression)
        elseCase, index = ElseStatement(tokens, index)
    return IfNode(cases, elseCase), index
    # cases = []
    # elseCase = None
    # if not type(tokens[index]) == If:
    #     print(f"Expected {If.value} token..")
    #     raise Exception(f"Expected {If.value} token..")
    # index = IncrementIndex(tokens, index)
    # condition, index = Expression(tokens, index)

    # if not type(tokens[index]) == Then:
    #     raise Exception(f"Expected {Then.value} token..")

    # index = IncrementIndex(tokens, index)

    # if type(tokens[index]) == NewLine:
    #     index = IncrementIndex(tokens, index)
    #     statements, index = Statements(tokens, index)
    #     cases.append((condition, statements)) 

    #     if type(tokens[index]) == EndIf:
    #         index = IncrementIndex(tokens, index)
    #     else:
    #         elseCase, index = ElseStatement(tokens, index)
    # else:
    #     expression, index = Statement(tokens, index)
    #     cases.append((condition, expression))
    #     elseCase, index = ElseStatement(tokens, index)
    # return IfNode(cases, elseCase), index

# def IfStatement(tokens: List[Token], index: int) -> Tuple[IfNode, int]:
#     """ IfStatement.
#     Parameters:
#         tokens (Lst)   : List with the tokens which will be parsed.
#         index (int)    : The index which will be used throughout the parse process.
#     Returns
#         node (IfNode)  : The resulting IfNode.
#         index (int)     : The incremented index.
#     """
#     return If(If, tokens, index - 1)

def WhileLoop(tokens: List[Token], index: int) -> Tuple[WhileNode, int]:
    """ While loop.
    Parameters:
        tokens (Lst)     : List with the tokens which will be parsed.
        index (int)      : The index which will be used throughout the parse process.
    Returns
        node (WhileNode) : The resulting WhileNode
        index (int)     : The incremented index.
    """
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

def FunctionDefenition(tokens: List[Token], index: int) -> Tuple[FunctionAssignNode, int]:
    """ Function defenition.
    Parameters:
        tokens (Lst)              : List with the tokens which will be parsed.
        index (int)               : The index which will be used throughout the parse process.
    Returns
        node (FunctionAssignNode) : The resulting FunctionAssignNode.
        index (int)               : The incremented index.
    """
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

        def SetParameters(tokenList, i):
            if type(tokenList[i]) == Comma:
                i = IncrementIndex(tokenList, i)
                if type(tokenList[i]) == Identifier:
                    arguments.append(tokenList[i])
                    i = IncrementIndex(tokenList, i)
                else:
                    raise Exception(f"Expected Identifier..")
                return SetParameters(tokenList, i)
            return i
            
        index = SetParameters(tokens, index)  

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

def CallFunction(tokens: List[Token], index: int) -> Tuple[Union[NumberNode, VariableAccessNode, IfNode, WhileNode, FunctionCallNode, ReturnNode], int]:
    """ Call function.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        
        index (int)     : The incremented index.
    """
    factor, index = Factor(tokens, index)
    if type(tokens[index]) == LPar:
        index = IncrementIndex(tokens, index)
        arguments = []
        if type(tokens[index]) == RPar:
            index = IncrementIndex(tokens, index)
        else:
            expression, index = Expression(tokens, index)
            arguments.append(expression)

            def SetArguments(tokenList, i, args):
                if type(tokens[i]) == Comma:
                    i = IncrementIndex(tokenList, i)
                    expr, i = Expression(tokenList, i)
                    args.append(expr)
                    return SetArguments(tokenList, i, args)
                return i
            index = SetArguments(tokens, index, arguments)
            if type(tokens[index]) != RPar:
                print("Expected RPar token..")
                raise Exception("Expected RPar token..")
            index = IncrementIndex(tokens, index)
        return FunctionCallNode(factor, arguments), index
    return factor, index

def Factor(tokens: List[Token], index: int) -> Tuple[Union[NumberNode, VariableAccessNode, IfNode, WhileNode, FunctionCallNode, ReturnNode], int]:
    """ Factor.
    Parameters:
        tokens (Lst)    : List with the tokens which will be parsed.
        index (int)     : The index which will be used throughout the parse process.
    Returns
        
        index (int)     : The incremented index.
    """
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
        return IfStatement(tokens, index - 1)
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
    """ Try.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        
    """
    if expression[0] == None:
        return expression[0], oldIndex
    return expression

def Statement(tokens: List[Token], index: int):
    """ Statement.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        
    """
    if type(tokens[index]) == Return:
        index = IncrementIndex(tokens, index)
        expression, index = Try(index, Expression(tokens, index)) 
        return ReturnNode(expression), index
    return Expression(tokens, index)

def Statements(tokens: List[Token], index: int) -> Tuple[ListNode, int]:
    """ Statements.
    Parameters:
        tokens (Lst)    : List with the tokens which will be parsed.
        index (int)     : The index which will be used throughout the parse process.
    Returns
        node (ListNode) : The resulting ListNode.
        index (int)     : The incremented index.
    """
    statements = []
    
    def func(tokenList, i):
        if type(tokenList[i]) == NewLine:
            i = IncrementIndex(tokenList, i)
            return func(tokenList, i)
        return i
    
    index = func(tokens, index)
    statement, index = Statement(tokens, index)
    statements.append(statement)

    @SkipUntil
    def SkipNewLines(token, tokens, index, skipped):
        skipped += 1
        return index, skipped

    def GetStatements(tokenList, i):
        newLine = 0
        i, newLine = SkipNewLines(NewLine, tokens, i, newLine)   
        if newLine == 0:
            return i
        statement, i = Try(i, Statement(tokens, i))
        if not statement:
            return i
        statements.append(statement)
        return GetStatements(tokenList, i)

    index = GetStatements(tokens, index)
    return ListNode(statements), index

def Term(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Term.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        
    """
    return BinaryOperation(Factor, (Multiply, Divide), tokens, index)

def Parse(tokens: List[Token], index: int) -> ListNode:
    """ Parse the tokens and create an AST.
    Parameters:
        tokens (Lst)   : List with the tokens which will be parsed.
        index (int)    : The index which will be used throughout the parse process.
    Returns
        AST (ListNode) : The AST which resulted out of the passed tokens.
    """
    statements, index = Statements(tokens, index)
    if type(tokens[index]) == EOF:
        return statements

Node = Union[NumberNode, VariableAccessNode, BinaryOperationNode, VariableAssignNode, ListNode, IfNode, WhileNode, FunctionAssignNode, FunctionCallNode, ReturnNode]