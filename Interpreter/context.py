from Interpreter.nodes import Node
from typing import Optional

class Context:
    def __init__(self, parent: 'Context' = None) -> None:
        """ Initialize the parent.
        Haskell:
            Init :: Context -> None
        Parameters:
            parent (Context): The parent context.
        """
        self.parent = parent
        self.symbolDictionary = SymbolDictionary()

        self.registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7"]
        self.labels = [".L2", ".L4", ".L6", ".L8", ".L10"]

class SymbolDictionary:
    def __init__(self, parent: 'SymbolDictionary' =None) -> None:
        """ Initialize the parent and create new dictionary. 
        Haskell:
            Init :: SymbolDictionary -> None
        Parameters:
            parent (SymbolDictionary): The parent SymbolDictionary.
        """
        self.symbols = {}
        self.parent = parent

    def GetValue(self, name: str) -> Optional[Node]: 
        """ This function tries to get the value of the passed name.
        Haskell:
            GetValue :: String -> Node | None
        Parameters:
            name (str): The dictionary key.
        Returns:
            node (Node): The corresponding node.
            Returns None if there is no corresponding node. """
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.GetValue(name)
        return value

    def SetValue(self, name: str, value: 'Node') -> None:
        """ This function creates a dictionary entry with the name and value. 
        Haskell:
            SetValue :: String -> Node -> None
        Parameters:
            name (str): The name of the key.
            value (Node): The node which will be stored.
        """
        self.symbols[name] = value
