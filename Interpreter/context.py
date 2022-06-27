class Context:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.symbolDictionary = SymbolDictionary()

        self.registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7"]
        self.labels = [".L2", ".L4", ".L6", ".L8", ".L10"]

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
