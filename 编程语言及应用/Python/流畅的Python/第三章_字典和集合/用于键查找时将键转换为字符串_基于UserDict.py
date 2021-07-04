import collections


# UserDict并不是dict的子类
class StrKeyDict1(collections.UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data  # data属性是UserDict类存储数据的地方

    # 构造字典时也用到了__setitem__,但是dict类型没有用到__setitem__
    def __setitem__(self, key, item):
        print('a')
        self.data[str(key)] = item


"""UserDict继承于抽象基类MutableMapping，MutableMapping又继承于Mapping模块，但是dict与它们之间没有继承关系。因此，虽然都属于映射类型，有一些同名的方法，但是其实现的方式大都不同有不同之处。
1.MutableMapping.update可传入映射类型的参数，也可传入元素为(key, value)的可迭代对象参数，但是这个方法背后实际上使用了方法self[key]=value,即__setitem__,而dict.update则不会使用该方法.
2.Mapping.get方法背后调用了__getitem__，而dict.get则不会使用__getitem__."""