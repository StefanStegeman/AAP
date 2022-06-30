from Interpreter import interpreter
from Interpreter.context import Context, SymbolDictionary
from Interpreter.tokens import *

class Function:
    def __init__(self, name, arguments, body, context) -> None:
        """ Initialize the function class. 
        Parameters:
            name (str)        : The name of the function. 
            arguments (Lst)   : The arguments for the function.
            body (Node)       : The body of the function in the form of a Node.
            context (context) : The context for the function.
        """
        self.name = name
        self.arguments = arguments
        self.body = body
        self.context = context

    def Execute(self, arguments):
        """ Execute the function's body. 
        
        Parameters:
            arguments (Lst) : The arguments passed into the function.
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