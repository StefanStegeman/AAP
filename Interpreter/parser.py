from typing import Callable, Tuple, Union, TypeVar
from functools import wraps
from Interpreter.tokens import *
from Interpreter.nodes import *

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def SkipDecorator(f: Callable[[Token, List[Token], int, Tuple], Tuple[int, A]]) -> Callable[[Token, List[Token], int, Tuple], Tuple[int, A]]:
    """ This is a decorator which allows the user to skip a certain token. 
    Haskell notation:
        SkipDecorator :: Callable -> Callable
    """
    @wraps(f)
    def SkipWrapper(token: Token, tokens: List[Token], index: int, *args: Tuple[int, A]) -> Union[int, A]:
        """ The wrapper function of the decorator.
        Haskell notation:
            SkipWrapper :: Token -> [Token] -> Integer -> Tuple -> Integer | A
        Parameters:
            token (Token): The token which will be skipped. 
            tokens (Lst): The list with all tokens.
            index (int): The current index.
        Returns:
            arg (A): The passed argument.
            index (int): The index which will be used throughout the parse process.
        """
        if type(tokens[index]) == token:
            index = IncrementIndex(tokens, index)
            index, args = f(token, tokens, index, *args)
            return SkipWrapper(token, tokens, index, args)
        return index, args[0]
    return SkipWrapper

def GetArguments(tokens: List[Token], index: int, arguments: List['Node']) -> Tuple[int, List['Node']]:
    """ Get the arguments for a function.
    This function retrieves all arguments from the tokenlist which belong to a function.
    Haskell notation:
        GetArguments :: [Token] -> Integer -> [Node] -> Tuple        
    Parameters:
        tokens (Lst): List with all the tokens which will be parsed. 
        index (int): The index which will be used throughout the parse process. 
        arguments (Lst): A list which will contain all arguments.
    Returns 
        index (int): The index which will be used throughout the parse process. 
        arguments (Lst): The list with all arguments.
    """
    if type(tokens[index]) == Comma:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) in (Int, Float, Identifier):
            argument, index = Expression(tokens, index)
            arguments.append(argument)
        else:
            if type(tokens[index]) != RPar:
                raise Exception(f"Expected Identifier or '{RPar.value}'")
        return GetArguments(tokens, index, arguments)
    return index, arguments

def IncrementIndex(tokens: List[Token], index: int) -> int:
    """ Increment the index if incrementing it won't make it go out of bounds.
    Haskell notation:
        IncrementIndex :: [Token] -> Integer -> Integer
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns:
        index (int): The incremented index.
    """
    return index + 1 if index < len(tokens) - 1 else index

def BinaryOperation(f: Callable[[A, B], C], acceptedTokens: List[Token], tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Create BinaryOperationNode.
    The BinaryOperationNode will be assigned with a left node, operator and right node.
    Haskell notation:
        BinaryOperation :: Callable -> [Token] -> [Token] -> Integer -> Tuple
    Parameters:
        f (Callable): Callable which is used to get the left and right nodes for.
        acceptedTokens (Lst): List with all the accepted tokens.
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.               
    Returns:
        node (Node): The resulting node.
        index (int): The incremented index.  
    """
    def AssignNode(lhs: 'Node', i: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
        """ This function assigns the BinaryOperation node when 
        the current token is in the accepted token list. 
        Haskell notation:
            AssignNode :: Node -> Integer -> Tuple 
        Parameters:
            lhs (Node): The left node. 
            i (int): The index.
        Returns
            lhs (BinaryOperationNode): The resulting BinaryOperationNode.
            index (int): The index which will be used throughout the parse process.
        """
        if type(tokens[i]) in acceptedTokens:
            operator = tokens[i]
            i = IncrementIndex(tokens, i)
            right, i = f(tokens, i)
            lhs = BinaryOperationNode(lhs, operator, right)
            return AssignNode(lhs, i)
        else:
            return lhs, i

    left, index = f(tokens, index)
    return AssignNode(left, index)
    
def Term(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Parse a Term.
    Haskell notation:
        Term :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (Node): The resulting node.
        index (int): The incremented index
    """
    return BinaryOperation(Factor, (Multiply, Divide), tokens, index)

def Arithmic(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Parse Arithmic expression.
    Haskell notation:
        Arithmic :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns:
        node (Node): The result of the BinaryOperation function call.
        index (int): The incremented index.
    """
    return BinaryOperation(Term, (Plus, Minus), tokens, index)

def Comparison(tokens: List[Token], index: int) -> Tuple[Union[BinaryOperationNode, NumberNode, VariableAssignNode], int]:
    """ Parse Comparison expression.
    Haskell notation:
        Comparison :: [Token] -> Integer -> Tuple 
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns:
        node (Node): The result of the BinaryOperation function call.
        index (int): The incremented index.
    """
    return BinaryOperation(Arithmic, (Equals, NotEquals, GreaterThan, GreaterThanEquals, LessThan, LessThanEquals), tokens, index)

def Expression(tokens: List[Token], index: int) -> Tuple['Node', int]:
    """ Parse an Expression
    Haskell notation:
        Expression :: [Token] -> Integer -> Tuple 
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns:
        node (VariableAssignNode): The resulting VariableAssignNode.
        index (int): The incremented index.
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

def ElseStatement(tokens: List[Token], index: int) -> Tuple['Node', int]:
    """ Parse an Else Statement.
    Haskell notation:
        ElseStatement :: [Token] -> Integer -> Tuple 
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        elseCase (ListNode): The resulting else case.
        index (int): The incremented index.
    """
    elseCase = None
    if type(tokens[index]) == Else:
        index = IncrementIndex(tokens, index)
        if type(tokens[index]) == NewLine:
            index = IncrementIndex(tokens, index)
            statements, index = Statements(tokens, index)
            elseCase = statements

            if type(tokens[index]) != EndIf:
                raise Exception(f"Expected {EndIf.value} Token..")
            index = IncrementIndex(tokens, index)
        else:
            expression, index = Statement(tokens, index)
            elseCase = expression
    return elseCase, index

def IfStatement(tokens: List[Token], index: int) -> Tuple[IfNode, int]:
    """ Parse an If Statement.
    Haskell notation:
        IfStatement :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (IfNode): The resulting IfNode.
        index (int): The incremented index.
    """
    elseCase = None
    condition, index = Expression(tokens, index)

    if type(tokens[index]) != Then:
        raise Exception(f"Expected {Then.value} token..")
    index = IncrementIndex(tokens, index)

    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        statements, index = Statements(tokens, index)
        case = (condition, statements)

        if type(tokens[index]) == EndIf:
            index = IncrementIndex(tokens, index)
        else:
            elseCase, index = ElseStatement(tokens, index)
    else:
        expression, index = Statement(tokens, index)
        case = (condition, expression)
        elseCase, index = ElseStatement(tokens, index)
    return IfNode(case, elseCase), index

def WhileLoop(tokens: List[Token], index: int) -> Tuple[WhileNode, int]:
    """ Parse a While loop.
    Haskell notation:
        WhileLoop :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (WhileNode): The resulting WhileNode
        index (int): The incremented index.
    """
    condition, index = Expression(tokens, index)
    if type(tokens[index]) != Then:
        raise Exception(f"Expected {Then.value} token..")
    index = IncrementIndex(tokens, index)
    if type(tokens[index]) == NewLine:
        index = IncrementIndex(tokens, index)
        body, index = Statements(tokens, index)
        if type(tokens[index]) != EndWhile:
            raise Exception(f"Expected {EndWhile.value} Token..")
        index = IncrementIndex(tokens, index)
        return WhileNode(condition, body), index

    body, index = Statement(tokens, index)
    return WhileNode(condition, body), index

def FunctionDefenition(tokens: List[Token], index: int) -> Tuple[FunctionDefenitionNode, int]:
    """ Parse a Function defenition.
    Haskell notation:
        Expression :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (FunctionDefenitionNode): The resulting FunctionDefenitionNode.
        index (int): The incremented index.
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
        index, arguments = GetArguments(tokens, index, arguments)  
        if type(tokens[index]) != RPar:
            raise Exception("Expected RPar token..")
    else:
        if type(tokens[index]) != RPar:
            raise Exception("Expected RPar token..")

    index = IncrementIndex(tokens, index)       
    if type(tokens[index]) != NewLine:
        raise Exception(f"Expected a new line after the assignment of '{FunctionDefenitionNode.value}' '{token}'..")

    index = IncrementIndex(tokens, index)
    body, index = Statements(tokens, index)
    if type(tokens[index]) != EndFunction:
        raise Exception(f"Expected {EndFunction.value} Token..")
    index = IncrementIndex(tokens, index)
    return FunctionDefenitionNode(token, arguments, body), index  

def CallFunction(tokens: List[Token], index: int) -> Tuple[Union[NumberNode, VariableAccessNode, IfNode, WhileNode, FunctionCallNode, ReturnNode], int]:
    """ Parsa a function call.
    Haskell notation:
        CallFunction :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (Node): The resulting node.
        index (int): The incremented index.
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
            index, arguments = GetArguments(tokens, index, arguments)
            if type(tokens[index]) != RPar:
                raise Exception("Expected RPar token..")
            index = IncrementIndex(tokens, index)
        return FunctionCallNode(factor, arguments), index
    return factor, index

def Factor(tokens: List[Token], index: int) -> Tuple[Union[NumberNode, VariableAccessNode, IfNode, WhileNode, FunctionCallNode, ReturnNode], int]:
    """ Parse a Factor.
    Haskell notation:
        Factor :: [Token] -> Integer -> Tuple
    This function does most of the work. It detects the type of the current token
    and makes sure the corresponding node gets created and returned.
    Parameters:
        tokens (Lst: List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (Node): The resulting node.
        index (int): The incremented index.
    """
    token = tokens[index]
    tokenType = type(token)
    index = IncrementIndex(tokens, index)

    if tokenType in (Int, Float):
        return NumberNode(token), index
    elif tokenType == Identifier:
        return VariableAccessNode(token), index
    elif tokenType == LPar:
        expression, index = Expression(tokens, index)
        if type(tokens[index]) == RPar:
            return expression, IncrementIndex(tokens, index)
    elif tokenType == If:
        return IfStatement(tokens, index)
    elif tokenType == While:
        return WhileLoop(tokens, index)
    elif tokenType == FunctionDef:
        return FunctionDefenition(tokens, index) 
    elif tokenType == Run:
        return CallFunction(tokens, index)
    elif tokenType == Return:
        expression, index = Expression(tokens, index)
        return ReturnNode(expression), index

def Try(index: int, f: Callable[[List[Token], int], Tuple['Node', int]]) -> Tuple['Node', int]:
    """ Try to get a node.
    The index will get reverted back to where it started when there is no node found.
    Haskell notation:
        Try :: Integer -> Callable -> Tuple
    Parameters:
        index (Lst): The index prior to the function call.
        f (Callable): The function call which will try to retrieve a node.
    Returns
        node (None, Node): None unless there came a node out of the function call.
    """
    if f[0] == None:
        return f[0], index
    return f

def Statement(tokens: List[Token], index: int) -> Tuple['Node', int]:
    """ Parse a Statement.
    Haskell notation:
        Statement :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (Node): The resulting statement.
        index (int): The incremented index.
    """
    if type(tokens[index]) == Return:
        index = IncrementIndex(tokens, index)
        expression, index = Try(index, Expression(tokens, index)) 
        return ReturnNode(expression), index
    return Expression(tokens, index)

def Statements(tokens: List[Token], index: int) -> Tuple[ListNode, int]:
    """ Parse Statements.
    Haskell notation:
        Statements :: [Token] -> Integer -> Tuple
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        node (ListNode): The resulting ListNode.
        index (int): The incremented index.
    """
    @SkipDecorator
    def SkipNewLines(token: Token, tokens: List[Token], index: int, skipped: int) -> Tuple[int, int]:
        """ This function skips new lines. 
        Haskell notation:
            Expression :: Token -> [Token] -> Integer -> Integer -> Tuple
        Parameters:
            token (Token): The token which will be skipped upon. 
            tokens (Lst): List with the tokens which will be parsed.
            index (int): The index which will be used throughout the parse process.
            skipped (int): The counter of how many times a new line has been skipped. 
        Returns:
            index (int): The incremented index.
            skipped (int): The amount of times a new line has been skipped.
        """
        skipped += 1
        return index, skipped

    def GetStatements(tokenList: List[Token], i: int) -> int:
        """ This function gets all statements.
        Haskell notation:
            GetStatements :: [Token] -> Integer -> Integer 
        Parameters:
            tokenList (Lst): List with the tokens which will be parsed.
            i (int): The index which will be used throughout the parse process.
        Returns:
            index (int): The incremented index.
        """
        newLine = 0
        i, newLine = SkipNewLines(NewLine, tokens, i, newLine)   
        if newLine == 0:
            return i
        statement, i = Try(i, Statement(tokens, i))
        if not statement:
            return i
        statements.append(statement)
        return GetStatements(tokenList, i)

    index = SkipNewLines(NewLine, tokens, index, 0)[0]
    statements = []
    statement, index = Statement(tokens, index)
    statements.append(statement)
    index = GetStatements(tokens, index)
    return ListNode(statements), index


def Parse(tokens: List[Token], index: int) -> ListNode:
    """ Parse the tokens and create an AST.
    Haskell notation:
        Parse :: [Token] -> Integer -> ListNode
    Parameters:
        tokens (Lst): List with the tokens which will be parsed.
        index (int): The index which will be used throughout the parse process.
    Returns
        AST (ListNode): The AST which resulted out of the passed tokens.
    """
    statements, index = Statements(tokens, index)
    if type(tokens[index]) == EOF:
        return statements

Node = Union[NumberNode, VariableAccessNode, BinaryOperationNode, VariableAssignNode, ListNode, IfNode, WhileNode, FunctionDefenitionNode, FunctionCallNode, ReturnNode]