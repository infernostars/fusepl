from core.classes.errors import FuseRuntimeError


class FuseNumber:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value + other.value).set_context(self.context), None

    def sub(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value - other.value).set_context(self.context), None

    def multiply(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value * other.value).set_context(self.context), None

    def power(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value ** other.value).set_context(self.context), None

    def divide(self, other):
        if isinstance(other, FuseNumber):
            if other.value == 0:
                return None, FuseRuntimeError(
                    other.pos_start, other.pos_end,
                    "Division by zero",
                    self.context
                )
            return FuseNumber(self.value / other.value).set_context(self.context), None

    def copy(self):
        copy = FuseNumber(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)