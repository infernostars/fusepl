class FuseNumber:
    def __init__(self, value):
        self.value = value
        self.set_pos()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def add(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value + other.value), None

    def sub(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value - other.value), None

    def multiply(self, other):
        if isinstance(other, FuseNumber):
            return FuseNumber(self.value * other.value), None

    def divide(self, other):
        if isinstance(other, FuseNumber):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    "Division by zero"

                )
            return FuseNumber(self.value / other.value), None

    def __repr__(self):
        return str(self.value)