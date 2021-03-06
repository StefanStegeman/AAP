from Interpreter import interpreter
from Interpreter.context import Context, SymbolDictionary
from Interpreter.nodes import ListNode
from Interpreter.number import Number
from Interpreter.tokens import *
from typing import List

class Function:
    def __init__(self, name: str, arguments: List[Identifier], body: ListNode, context: Context) -> None:
        """ Initialize the function class. 
        Haskell notation:
            Init :: String -> [Identifier] -> ListNode -> Context -> None
        Parameters:
            name (str): The name of the function. 
            arguments (Lst): The arguments for the function.
            body (Node): The body of the function in the form of a Node.
            context (context): The context for the function.
        """
        self.name = name
        self.arguments = arguments
        self.body = body
        self.context = context

    def Execute(self, arguments: List[Number]) -> Number:
        """ Execute the function's body. 
        Haskell notation:
            Execute :: [Number] -> Number
        Parameters:
            arguments (Lst): The arguments passed into the function.
        Returns:
            number (Number): The result of executing the function's body.
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
        return interpreter.VisitNode(self.body, context)