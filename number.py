class Number:
    def __init__(self, value, context = None):
        self.value = value
        self.context = context

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self):
        return f'{self.value}'

    def Plus(self, other):
        return Number(self.value + other.value, self.context)

    def Minus(self, other):
        return Number(self.value - other.value, self.context)

    def Multiply(self, other):
        return Number(self.value * other.value, self.context)

    def Divide(self, other):
        return Number(self.value / other.value, self.context)

    def Equals(self, other):
        return Number(int(self.value == other.value), self.context)
    
    def NotEquals(self, other):
        return Number(int(self.value != other.value), self.context)

    def GreaterThan(self, other):
        return Number(int(self.value > other.value), self.context)

    def GreaterThanEquals(self, other):
        return Number(int(self.value >= other.value), self.context)

    def LessThan(self, other):
        return Number(int(self.value < other.value), self.context)

    def LessThanEquals(self, other):
        return Number(int(self.value <= other.value), self.context)

    def And(self, other):
        return Number(int(self.value and other.value), self.context)

    def Or(self, other):
        return Number(int(self.value or other.value), self.context)

    def Not(self):
        return Number(1 if self.value == 0 else 0, self.context)
        
    def IsTrue(self):
        return self.value != 0

Number.null = Number(0)
Number.true = Number(1)
Number.false = Number(0)