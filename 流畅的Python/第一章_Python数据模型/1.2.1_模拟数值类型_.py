# hypot() 返回欧几里德范数 sqrt(x*x + y*y)。
from math import hypot


class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # 和__str__的区别是__str__仅会在使用print打印时表现友好，而__repr__无论在打印时还是控制台直接输出时均表现友好
    def __repr__(self):
        return f'Vector({self.x},{self.y})'

    def __str__(self):
        return "????"

    #
    def __abs__(self):
        return hypot(self.x, self.y)

    # 每当需要判断一个值为真还是为假的时候，python解释器都会调用bool()（在很多地方他都被隐式调用了，例如while 1：），这个函数只能返回True或者False
    # 我们自定义的类一般被默认为真，除非它有自己的__bool__()
    def __bool__(self):
        return bool(abs(self))  # 更高效的写法是return bool(self.x or self.y)

    # 相当于一种变相的运算符重载
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)


my_vector = Vector()
# %r是用来__repr__内置函数
print('%r' % my_vector)
# %s是使用了__str__内置函数，当__str__未定义时，使用__repr__。当我们同时定义了__str__和__repr__时，我们尽可能地将__repr__的内容设置为它所代表的对象
print('%s' % my_vector)
print(my_vector)
