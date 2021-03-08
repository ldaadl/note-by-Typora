# 第九章 符合Python风格的对象

## 1.用一个很长的例子来讲述这一章要介绍的Python风格对象所需的属性和方法

* 绝大多数自定义类型的魔术方法的实现都是利用了基本类型的魔术方法

````python
from array import array
import math

class Vector2d:
    """这是一个符合Python风格的向量类"""
    __slots__ = ('typecode', '__x', '__y')
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
        return (i for i in (self.x, self.y))  # 返回了一个生成器;此处我还有困惑
    
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

​	在类的\_\_init__外定义的bytecode是一个类属性，意思是在创建类的实例时，实例的\_\_dict\_\_中并不存在这个属性，不过可以访问到该属性，但是实例的该属性实际上是调用了类的属性，就如同C++的静态成员一样。

​	不过需要注意的是，Python的类可以在除\_\_init__以外的其他方法中新增属性，也可以通过实例增加属性，如果增加的属性和类属性同名，那么实例将真正拥有该属性。

### c.@classmethed和@staticmethed还有@property

​	@classmethed装饰器是将被装饰的方法声明为备选构造函数（转换构造函数），被修饰的方法第一个参数为类，参数名最好尾cls，这个装饰器会使得 a = Vector2d.frombytes(bytes(v1))可以调用方法frombytes并传入Vector2d作为cls。

​	@staticmethed是将被装饰方法声明为静态方法。

​	@property,可以使得被装饰的属性只有只读权限

### d.格式化显示

​	format函数和str.format的背后其实是方法\_\_format\_\_(f_s)，f_s是format函数的第二个参数，是str.format使用时，str中{}所使用的格式说明符。我们定义的\_\_format\_\_还定义了我们自己的规则，以'p'结尾时用极坐标显示。

### e.使用\_\_slots__类属性

​	我们在上面说了，类的实例以\_\_dict\_\_字典存储属性，我们之前学习过，字典以哈西表的形式存储，以时间换空间，这本来很好，但是当我们需要创建几百万个拥有简单属性的时候，这样就太浪费空间类。这个时候我们将使用**\_\_slots\_\_**类属性，注意，这是一个类属性，实例是不独自具有的，而且这个属性会取代\_\_dict\_\_，但是使用了**\_\_slots\_\_**之后就限定了实例中只能存在**\_\_slots\_\_**中存在的属性，实例新增属性将会受到一定限制。