from ast import arg


class Function:
    """ Function class which makes it easier to execute a function."""
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

    def Compile(self, arguments, context):
        assert(len(arguments)) == len(self.arguments)
        zippedArguments = list(zip(map(lambda a: a.value, self.arguments), map(lambda a: a, arguments)))
        # zippedArguments = list(zip(self.arguments, arguments))
        context.symbolDictionary.symbols.update(zippedArguments)
        return self.body, context

    def __repr__(self) -> str:
        return f"Wife {self.name}"