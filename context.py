class SymbolDictionary:
    def __init__(self, parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def GetValue(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.GetValue(name)
        return value

    def SetValue(self, name, value):
        print(f"Name: {name}, Value: {type(value)}")
        self.symbols[name] = value

    def RemoveValue(self, name):
        del self.symbols[name]

    def Print(self):
        for item in self.symbols.values():
            print(item, type(item))

class Context:
    def __init__(self, parent = None, parent_entry = None) -> None:
        self.parent = parent
        self.parent_entry = parent_entry
        self.symbolDictionary = None