import fractions

class FuseNumber(fractions.Fraction):
    def __init__(self, numerator: int, denominator: int = 1):
        super.__init__(numerator, denominator)