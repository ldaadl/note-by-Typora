# 容器序列（可存放不同类型的元素）：list，tuple，collections.deque
# 扁平序列（存放单一类型）：str，bytes，bytearray，memoryview，array.array
# 容器序列存放的是包含任意对象的引用，而扁平序列里存放的则是值而不是引用，换言之，扁平序列是一段连续的内存空间。

# 可变类型: list，bytearray，memoryview，array.array，collections.deque
# 不可变类型：tuple，str，bytes

# 不可变类型继承与抽象基类Sequence，可变类型继承与抽象基类MutableSequence，MutableSequence又继承于Sequence
