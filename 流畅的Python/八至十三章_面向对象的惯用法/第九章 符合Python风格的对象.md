# 第九章 符合Python风格的对象

## 1.用一个很长的例子来讲述这一章要介绍的Python风格对象所需的属性和方法

* 绝大多数自定义类型的魔术方法的实现都是利用了基本类型的魔术方法

````python
from array import array
import math

class Vector2d:
    """这是一个符合Python风格的向量类"""
    typecode = 'd'
    
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
        
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    # __iter__()的作用是将类变为可迭代对象
    def __iter__(self):
        return (i for i in (self.x, self.y))  # 返回了一个生成器;实此处我还有困惑
    
    def __repr__(self):
        class_name = type(self).__name__  # 不直接使用Vector2d的原因是为了继承考虑
        return '{}({!r}, {!r})'.format(class_name, *self)  # 能够解包是因为实现了__iter__(),解包依赖于这个方法
    
    def __str__(self):
        return str(tuple(self))  # str()函数依赖于__str__()方法，此处先把self转为tuple（依赖于__iter__()），再将tuple类型转为str。
    
    def __bytes__(self):
        return (bytes([ord(self.bytecode)]) + bytes(array(self.typecode, self)))  # ord()是与chr()和unchr()相对的函数，后两者是将码位转为字符，前者是将字符转为码位;而bytes()传入的参数有两种，一是可迭代对象，提供0～255之间的数值，二是一个str对象和一个encoding关键字参数（即array类型）。注意，我们返回的不是元组。
    
    def __eq__(self, other):
        return tuple(self) == tuple(other)  # 如果是一个数值和self相同的可迭代对象，即时不是我们定义的向量类型，它也是相等的，但这是一个副作用或者是优秀之处要按情况区分
    
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)  
    
    def __abs__(self):
        return bool(abs(self))  
    
    def angle(sefl):  # 返回向量的角度
        return math.atan2(self.y, self.x)
    
    def __format__(self, fmt_spac=''):  # format()和str.format()背后实际上是这个方法
        if fmt_spec.endwith('p'):
            fmt_spec = fmt_spec[:-1]
            coord = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)
    
    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
````

## 2.补充

### a.关于自定义类型变为可散列对象

​	在第三章时曾说过，所有的自定义类型都是可散列的，散列值是他们的id()，但是这一张给我的感觉与之前的描述不一致，我只感到自定义类型都是可以变成可散列的，而且散列值不一定为id().

​	将我们自定义的类型变为可散列对象需要实现几点：1,\_\_hash__()，\_\_eq\_\_()两个函数。2.将前面两个函数所用到的类的可能变化的属性变为只读。

​	第一点我们好理解，这是之前说过的可散列需要的方法。我们继续看看这两个方法的实现细节，\_\_eq__()没什么好说的，根据需要怎么样的两个类的实例是相等的，就怎样设置。关于\_\_hash__\_\_()，我们知道，可散列对象的一个要求就是\_\_eq\_\_()相等,\_\_hash\_\_()必须相等，所以我们尽量保证\_\_eq\_\_()中用到的类的属性，\_\_hash__()中都要用到，而且比较Python的做法是类的哈西值取各属性哈西值做异或运算的结果。

​	第二点，也好理解，就是使自定义类一定程度上变为不可变类型。<u>但是此处有两个题外话要讲：</u>

> 1. 在c++中，我们知道子类有一个和父类同名的方法或者属性，则会发生同名覆盖现象，但是父类的属性和方法并没有被真的覆盖，它仍然有方法可以访问到，但是Python中则不然，同名覆盖真的会覆盖父类中的属性和方法。
> 2. 谈谈类中的私有属性，类中的私有属性的定义方式是以双下划线开头，结尾至多有一个下划线，这样定义的属性就变为了私有属性。原理是，在类的实例中，所有属性均被保存在\_\_dict\_\_字典中，如果一个属性为私有属性，它保存在\_\_dict__中的名称将不再是它原来的名称，而变为了   '\_类名\_\_私有对象'，这就使我们不能按我们定义的名称去访问私有属性，但是如果我们知道类这个名称变化规则，还是可以轻而易举地访问到私有属性，所以说私有属性是防止误操作的手段，而不是防御手段。（有些人觉得这种设置是多此一举的，所以他们提倡定义私有属性的时候在前面加上单下划线即可，就如同全局变量的定义).

### b.关于在__init\_\_外定义的bytecode

### c.@classmethed和@staticmethed

### d.格式化显示

### e.使用\_\_slots__类属性