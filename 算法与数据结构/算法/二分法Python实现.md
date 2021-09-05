# 二分法Python实现

​	二分法是很简单的查找算法了，我最近在写SQL注入攻击脚本的时候用到了二分法。因为这个脚本对http请求的次数有要求，在算法中的体现是不能做太多次比较，而我感觉我写出的蹩脚脚本似乎做了一些而外的比较，于是从新来整理一下二分法。

## 一.python实现二分法

### 1.递归实现

```````python
# coding=utf-8
class BinarySearch(object):
    def binary_search(self, array, data):
        """二分查找法递归实现"""
        if len(array) == 0:
            return False
        array.sort()
        mid_index = len(array) // 2
        if array[mid_index] == data:
            return True
        if data > array[mid_index]:
            return self.binary_search(array[mid_index + 1:], data)
        else:
            return self.binary_search(array[:mid_index], data)
```````

​	好吧，其实感觉自己写的也没毛病

### 2.非递归实现

```````python
    def binary_search_normal(self, array, data):
        """二分查找法非递归实现"""
        array.sort()
        start, end = 0, len(array)-1
        while start <= end:
            mid_index = (start + end) // 2
            if array[mid_index] == data:
                return True
            if data > array[mid_index]:
                start = mid_index + 1
            else:
                end = mid_index - 1
        return False
```````



## 二.借助python的	实现二分法查找

​	前面的没有花费多少笔墨，因为二分法确实很简单，简单到Python中有现成的轮子给我们使用。这个现成的轮子就是bisect模块，这里只介绍这个模块中的两个主要函数：

* bisect.bisect(haystack,needle) haystack是一个序列，needle需要查找的值，返回值是needle在序列中的位置
* bisect.insort(seq,item) 将item插入seq并保持seq的升序

   

