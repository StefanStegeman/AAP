from Interpreter.context import Context
from Interpreter.nodes import ListNode
from Interpreter.tokens import *
from typing import List, Tuple

class Function:
    def __init__(self, name: str, arguments: List[Identifier], body: ListNode, context: Context) -> None:
        """ Initialize the function class. 
        Haskell notation notation:
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

    def Compile(self, arguments: ListNode, context: Context) -> Tuple[ListNode, Context]:
        """ Compile the function's body.
        Haskell notation notation:
            Compile :: ListNode -> Context -> Tuple
        Parameters:
            arguments (Lst): The arguments passed into the function.
            context (Context): The current existing context. 
        Returns:
            body (ListNode): The body which will be compiled.
            context (Context): The updated context. 
        """
        if len(arguments) > len(self.arguments):
            raise Exception(f"Too many arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")
        elif len(arguments) < len(self.arguments):
            raise Exception(f"Too little arguments given for {FunctionDef.value} {self.name}.. Expected {len(self.arguments)}, got {len(arguments)}")
        
        zippedArguments = list(zip(map(lambda a: a.value, self.arguments), map(lambda a: a, arguments)))
        context.symbolDictionary.symbols.update(zippedArguments)
        return self.body, context

    def __repr__(self) -> str:
        return f"Wife {self.name}"