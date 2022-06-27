class SymbolDictionary:
    def __init__(self, parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def GetValue(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.GetValue(name)
        return value

    def SetValue(self, name: str, value):
        self.symbols[name] = value

class Context:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.symbolDictionary = None