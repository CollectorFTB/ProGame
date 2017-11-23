import util
from kivy.uix.image import Image


class NormImage(Image):
    def __init__(self, **kwargs):
        super(NormImage, self).__init__(**kwargs)
        self.rx = kwargs['x']  # real world x
        self.ry = kwargs['y']  # real world y


class Fraction:
    def __init__(self, *args):
        if len(args) == 1:
            self.numerator = args[0]
            self.denominator = 1
        elif len(args) == 2:
            self.numerator = args[0]
            self.denominator = args[1]
        else:
            self.numerator = 0
            self.denominator = 0

    def expand(self, factor):
        """
        multiplies top and bootom by factor
        :param factor: integer to expand numerator and denominator by 
        :return: 
        """
        if type(factor) is int:
            self.numerator *= factor
            self.denominator *= factor

    def simplify(self):
        """
        get simple form of the fraction
        :return: whether something was changed
        """
        re = self.numerator
        common_factor = util.gcd(self.numerator, self.denominator)
        self.numerator /= common_factor
        self.denominator /= common_factor
        return self.numerator == re

    def __add__(self, other):
        re = 0
        if isinstance(other, int):
            re = Fraction(self.numerator + other*self.denominator, self.denominator)
        elif isinstance(other, Fraction):
            lcm = (self.denominator * other.denominator) / util.gcd(self.denominator, other.denominator)
            re = Fraction((lcm / self.denominator) * self.numerator + (lcm / other.denominator) * other.numerator, lcm)
        return re

    def __mul__(self, other):
        re = 0
        if isinstance(other, int):
            re = Fraction(self.numerator * other, self.denominator)
        elif isinstance(other, Fraction):
            re = Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        return re

    def __truediv__(self, other):
        re = 0
        if isinstance(other, int):
            re = self.__mul__(Fraction(1, other))
        elif isinstance(other, Fraction):
            re = self.__mul__(Fraction(other.denominator, other.numerator))
        return re

    def __cmp__(self, other):
        re = False
        if isinstance(other, int):
            re = (float(other) == float(self.numerator) / self.denominator)
        elif isinstance(other, Fraction):
            return (float(self.numerator) / other.denominator) == (self.numerator / other.denominator)

        return re

    def __iadd__(self, other):
        f = self.__add__(other)
        self.numerator = f.numerator
        self.denominator = f.denominator
        return self

    def __imul__(self, other):
        f = self.__mul__(other)
        self.numerator = f.numerator
        self.denominator = f.denominator
        return self

    def __idiv__(self, other):
        f = self.__truediv__(other)
        self.numerator = f.numerator
        self.denominator = f.denominator
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return str(float(self.numerator)/self.denominator)

    def __str__(self):
        return str(self.numerator) + "/" + str(self.denominator)

    def evaluate(self):
        return float(self.numerator) / self.denominator
