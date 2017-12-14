import util
from kivy.uix.image import Image


class Animation:
    """
    ughhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
    """
    def __init__(self, points, image):
        self.iterator = 0
        self.image = image
        self.points = points

    def next_frame(self, func):
        self.image.rx, self.image.ry = self.points[self.iterator]  # get the current position of image
        func(self.image)  # set the kivy xy to match real xy

        # self.image.x -= self.image.texture.size[0] / 2  # center image instead of corner
        # self.image.y -= self.image.texture.size[1] / 2
        self.iterator = (self.iterator + 1) % len(self.points)  # prepare next position


class NormImage(Image):
    """
          a normal image with what you would expect in rx,ry and what kivy will make of it in x,y 
    """
    def __init__(self, **kwargs):
        super(NormImage, self).__init__(**kwargs)
        self.rx = kwargs['x']  # real world x
        self.ry = kwargs['y']  # real world y
        self.i = 0
        self.j = 0

    def __copy__(self):
        return NormImage(source=self.source, x=self.x, y=self.y)


class Fraction:
    """
    idk what this is even for ignore this completely
    """
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
        if isinstance(factor, int):
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
