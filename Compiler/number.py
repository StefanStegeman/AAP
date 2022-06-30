from typing import Union
from Interpreter.context import Context
class Number:
    """ The Number class contains all data and all the functions which can be applied to a number. """

    def __init__(self, value: Union[int, float], context, register):
        """ Store the passed value and context. 
        
        Parameters:
            value (int, float) : The value for the number.
            register (int)  : The register of the number.
        """
        self.value = value
        self.context = context
        self.register = register

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'

    def Plus(self, other, context, instructions):
        """ This function adds other.value with self.value. 
        
        Parameters:
            other (Number) : The other number to add with.

        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tADD \t{self.register}, {other.register}\n")
        return Number(self.value + other.value, self.context, self.register)

    def Minus(self, other, context, instructions):
        """ This function subtracts other.value with self.value. 
        
        Parameters:
            other (Number) : The other number to subtract with.

        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tSUB \t{self.register}, {other.register}\n")
        return Number(self.value - other.value, self.context, self.register)

    def Multiply(self, other, context, instructions):
        """ This function multiplies self.value with other.value. 
        
        Parameters:
            other (Number) : The other number to multiply with.

        Returns:
            number (Number): The result of the operation.
        """
        instructions.append(f"\tMUL \t{self.register}, {other.register}\n")
        return Number(self.value * other.value, self.context, self.register)

    def Divide(self, other, context, instructions):
        """ This function divides self.value with other.value. 
        
        Parameters:
            other (Number) : The other number to divide with.

        Returns:
            number (Number): The result of the operation.
        """
        resultRegister = context.registers.pop(0)
        instructions[5].add(resultRegister)
        instructions.append("\tPUSH\t{R0, R}\n") # Push original values to stack
        instructions.append(f"\tMOV \tR0, {self.register}\n") # Move registers to divide to r0 and r1.
        instructions.append(f"\tMOV \tR1, {other.register}\n")
        instructions.append("\tBL  \t__aeabi_idiv\n")
        instructions.append(f"\tMOV \t{resultRegister}, R0\n") # Store result of division.
        instructions.append("\tPOP \t{R0, R1}\n") # Restore original values of r0 and r1.
        if(other.value == 0):
            return Number(self.value / 1, self.lineNumber, context, resultRegister)
        return Number(self.value / other.value, context, resultRegister)

    def Equals(self, other, context, instructions):
        """ This function checks whether self.value is equal compared with other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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
    
    def NotEquals(self, other, context, instructions):
        """ This function checks whether self.value is not equal compared to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def GreaterThan(self, other, context, instructions):
        """ This function checks whether self.value is greater than other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def GreaterThanEquals(self, other, context, instructions):
        """ This function checks whether self.value is greater than or equal to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def LessThan(self, other, context, instructions):
        """ This function checks whether self.value is less than other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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
        return Number(int(self.value < other.value), self,context, resultRegister)

    def LessThanEquals(self, other, context, instructions):
        """ This function checks whether self.value is less than or equal to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def And(self, other, context, instructions):
        """ This function checks whether self.value and other.value are true. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def Or(self, other, context, instructions):
        """ This function checks whether self.value or other.value are true. 
        
        Parameters:
            other (Number) : The other number to compare with.

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

    def IsTrue(self):
        """ This function checks whether self.value is true. 
        
        Returns:
            number (Number): The result of the check. This can be either 1 (true) or 0 (false)
        """
        return self.value != 0