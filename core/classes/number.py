from core.classes.errors import FuseRuntimeError


class FuseNumber:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        """
        Sets the position of the FuseNumber. Not required for function, but generally recommended for error handling.
        :param pos_start: The starting position.
        :param pos_end: The ending position.
        :return:
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        """
        Adds a context. Not required for functionality, but recommended for error handling.
        :param context: the `Context` class to give it.
        :return:
        """
        self.context = context
        return self

    def add(self, other):
        """
        Adds two FuseNumbers together.
        :param other: The other FuseNumber to add.
        :return: The sum of the FuseNumbers.
        """
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value + other.value).set_context(self.context), None

    def sub(self, other):
        """
        Subtracts two FuseNumbers.
        :param other: The other FuseNumber to subtract.
        :return: The FuseNumber being called, minus the FuseNumber provided.
        """
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value - other.value).set_context(self.context), None

    def multiply(self, other):
        """
        Multiplies two FuseNumbers together.
        :param other: The other FuseNumber to multiply.
        :return: The product of the two FuseNumbers.
        """
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value * other.value).set_context(self.context), None

    def power(self, other):
        """
        Exponentiates two FuseNumbers.
        :param other: The other FuseNumber to exponentiate.
        :return: The two numbers, powered together.
        """
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value ** other.value).set_context(self.context), None

    def divide(self, other):
        """
        Divides two FuseNumbers. Note that this can return an error.
        :param other: The other FuseNumber to subtract.
        :return: The FuseNumber being called, divided by the FuseNumber provided. Note that this can return a FuseRuntimeError.
        """
        if isinstance(other, FuseNumber):
            if other.value == 0:
                return None, FuseRuntimeError(
                    other.pos_start, other.pos_end,
                    "Division by zero",
                    self.context
                )
            return FuseNumber(self.value / other.value).set_context(self.context), None

    def copy(self):
        """
        Makes a clone of a FuseNumber.
        :return: a copy of the FuseNumber.
        """
        copy = FuseNumber(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def equals(self, other):
        """
        Checks if a FuseNumber equals another FuseNumber.
        :param other: The other FuseNumber to compare.
        :return: 1 if equivalent, 0 if not.
        """
        if self.value == other.value:
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def less(self, other):
        """
        Checks if a FuseNumber is less than another FuseNumber. Also used in greater than or equals.
        :param other: The other FuseNumber to compare.
        :return: 1 if less, 0 if not.
        """
        if self.value < other.value:
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def greater(self, other):
        """
        Checks if a FuseNumber is greater than another FuseNumber. Also used in less than or equals.
        :param other: The other FuseNumber to compare.
        :return: 1 if greater, 0 if not.
        """
        if self.value > other.value:
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def not_l(self):
        """
        Inverts the value, assuming it is a logical boolean. 0 is falsy, everything else is truthy.
        :return: 1 if the number isn't 0, otherwise returns a 1.
        """
        if self.value == 0:
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def or_l(self, other):
        """
        Logically ORs the two values together. 0 is falsy, everything else is truthy.
        :param other: The other value to compare.
        :return: The values OR'd together.
        """
        if bool(self.value) or bool(other.value):
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def xor_l(self, other):
        """
        Logically XORs the two values together. 0 is falsy, everything else is truthy.
        :param other: The other value to compare.
        :return: The values XOR'd together.
        """
        if bool(self.value) + bool(other.value) == 1:
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None

    def and_l(self, other):
        """
        Logically ANDs the two values together. 0 is falsy, everything else is truthy.
        :param other: The other value to compare.
        :return: The values AND'd together.
        """
        if bool(self.value) and bool(other.value):
            return FuseNumber(1).set_context(self.context), None
        else:
            return FuseNumber(0).set_context(self.context), None


    def __repr__(self):
        return str(self.value)
