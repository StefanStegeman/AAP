from typing import Union, Tuple, List
from Compiler.context import Context

class Number:
    def __init__(self, value: Union[int, float], context: Context, register: str) -> None:
        """ Initialize the passed value, context and register. 
        Haskell:
            Init :: Int | Float -> Context -> String -> None
        Parameters:
            value (int, float): The value for the number.
            context (Context): The existing context.
            register (str): The register for the number.
        """
        self.value = value
        self.context = context
        self.register = register

    def __str__(self) -> str:
        """ Represents self.value as a string. """
        return f'{self.value}'

    def Plus(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function adds other.value with self.value.
        Haskell:
            Plus :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number): The other number to add with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tADD \t{self.register}, {other.register}\n")
        return Number(self.value + other.value, self.context, self.register)

    def Minus(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function subtracts other.value with self.value. 
        Haskell:
            Minus :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number): The other number to subtract with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tSUB \t{self.register}, {other.register}\n")
        return Number(self.value - other.value, self.context, self.register)

    def Multiply(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function multiplies self.value with other.value. 
        Haskell:
            Multiply :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number): The other number to multiply with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tMUL \t{self.register}, {other.register}\n")
        return Number(self.value * other.value, self.context, self.register)

    def Divide(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function divides self.value with other.value. 
        Haskell:
            Divide :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number): The other number to divide with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation.
        """
        resultRegister = context.registers.pop(0)
        instructions[5].add(resultRegister)
        instructions.append("\tPUSH\t{R0, R}\n")
        instructions.append(f"\tMOV \tR0, {self.register}\n") 
        instructions.append(f"\tMOV \tR1, {other.register}\n")
        instructions.append("\tBL  \t__aeabi_idiv\n")
        instructions.append(f"\tMOV \t{resultRegister}, R0\n")
        instructions.append("\tPOP \t{R0, R1}\n")
        if(other.value == 0):
            return Number(self.value / 1, self.lineNumber, context, resultRegister)
        return Number(self.value / other.value, context, resultRegister)

    def Equals(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is equal compared with other.value.
        Haskell:
            Equals :: Number -> Context -> [String & Set] -> Tuple 
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        instructions[5].add(tempRegister)
        instructions.append(f"\tSUB \t{tempRegister}, {other.register}, {self.register}\n")
        instructions.append(f"\tNEG \t{resultRegister}, {tempRegister}\n")
        instructions.append(f"\tADC \t{resultRegister}, {resultRegister}, {tempRegister}\n")
        return Number(int(self.value == other.value), self.context, resultRegister)
    
    def NotEquals(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is not equal compared to other.value. 
        Haskell:
            NotEquals :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        instructions[5].add(tempRegister)
        instructions.append(f"\tSUB \t{resultRegister}, {other.register}, {self.register}\n")
        instructions.append(f"\tSUB \t{tempRegister}, {resultRegister}, #1\n")
        instructions.append(f"\tSBC \t{resultRegister}, {resultRegister}, {tempRegister}\n")
        return Number(int(self.value != other.value), self.context, resultRegister)

    def GreaterThan(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is greater than other.value. 
        Haskell:
            GreaterThan :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        instructions[5].add(resultRegister)
        label = context.labels.pop(0)
        instructions.append(f"\tMOV \t{resultRegister}, #1\n")
        instructions.append(f"\tCMP \t{self.register}, {other.register}\n")
        instructions.append(f"\tBGT \t{label}\n")
        instructions.append(f"\tMOVS\t{resultRegister}, #0\n")
        return Number(int(self.value > other.value), self.context, resultRegister)

    def GreaterThanEquals(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is greater than or equal to other.value. 
        Haskell:
            GreaterThanEquals :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        instructions[5].add(tempRegister)
        instructions.append(f"\tASR \t{resultRegister}, {self.register}, #31\n")
        instructions.append(f"\tLSR \t{tempRegister}, {other.register}, #31\n")
        instructions.append(f"\tCMP \t{self.register}, {other.register}\n")
        instructions.append(f"\tADC \t{resultRegister}, {resultRegister}, {tempRegister}\n")
        return Number(int(self.value >= other.value), self.context, resultRegister)

    def LessThan(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is less than other.value. 
        Haskell:
            LessThan :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        instructions[5].add(resultRegister)
        label = context.labels.pop(0)
        instructions.append(f"\tMOV \t{resultRegister}, #1\n")
        instructions.append(f"\tCMP \t{self.register}, {other.register}\n")
        instructions.append(f"\tBLT \t{label}\n")
        instructions.append(f"\tMOVS\t{resultRegister}, #0\n")
        instructions.append(f"{label}:\n")
        return Number(int(self.value < other.value), self.context, resultRegister)

    def LessThanEquals(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value is less than or equal to other.value. 
        Haskell:
            LessThanEquals :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        tempRegister = context.registers[0]
        instructions[5].add(tempRegister)
        instructions.append(f"\tLSR \t{resultRegister}, {self.register}, #31\n")
        instructions.append(f"\tASR \t{tempRegister}, {other.register}, #31\n")
        instructions.append(f"\tCMP \t{other.register}, {self.register}\n")
        instructions.append(f"\tADC \t{resultRegister}, {resultRegister}, {tempRegister}\n")
        return Number(int(self.value <= other.value), self.context, resultRegister)

    def And(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value and other.value are true. 
        Haskell:
            And :: Number -> Context -> [String & Set] -> Tuple
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        instructions[5].add(otherRegister)
        instructions.append(f"\tASR \t{firstRegister}, {self.register}, #31\n")
        instructions.append(f"\tSUB \t{resultRegister}, {firstRegister}, {self.register}\n")
        instructions.append(f"\tASR \t{firstRegister}, {other.register}, #31\n")
        instructions.append(f"\tSUB \t{otherRegister}, {firstRegister}, {other.register}\n")
        instructions.append(f"\tAND \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        instructions.append(f"\tLSR \t{resultRegister}, {resultRegister}, #31\n")
        return Number(int(self.value and other.value), self.context, resultRegister)

    def Or(self, other: 'Number', context: Context, instructions: List[Union[str, set]]) -> 'Number':
        """ This function checks whether self.value or other.value are true.
        Haskell:
            Or :: Number -> Context -> [String & Set] -> Tuple 
        Parameters:
            other (Number) : The other number to compare with.
            instructions (Lst): The list of instructions which get updated.
        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        resultRegister = context.registers.pop(0)
        firstRegister = context.registers[0]
        otherRegister = context.registers[1]
        instructions[5].add(otherRegister)
        instructions.append(f"\tASR \t{firstRegister}, {self.register}, #31\n")
        instructions.append(f"\tSUB \t{resultRegister}, {firstRegister}, {self.register}\n")
        instructions.append(f"\tASR \t{firstRegister}, {other.register}, #31\n")
        instructions.append(f"\tSUB \t{otherRegister}, {firstRegister}, {other.register}\n")
        instructions.append(f"\tORR \t{resultRegister}, {resultRegister}, {otherRegister}\n")
        instructions.append(f"\tLSR \t{resultRegister}, {resultRegister}, #31\n")
        return Number(int(self.value or other.value), self.context, resultRegister)

    def IsTrue(self) -> bool:
        """ This function checks whether self.value is true. 
        Haskell:
            IsTrue :: Boolean
        Returns:
            number (Number): The result of the check. This can be either 1 (true) or 0 (false)
        """
        return self.value != 0