import array

symbols = '$%&*('
codes = [ord(symbol) for symbol in symbols]  # 这是列表推导
codesAnother = (ord(symbol) for symbol in symbols)  # 这是生成器表达式，它仍然生成了一个列表（不是生成了元组），但是比列表推倒更加节省空间
# 列表推导仅仅只能一般用于生成列表，而生成器不仅通常用于生成其他类型的数据，还可以作为函数的参数
tuple(ord(symbol) for symbol in symbols)  # 园括号是生成器不可缺少的一部分，但是函数只有一个参数时，不许要原括号
array.array('I', (ord(symbol) for symbol in symbols))  # 函数有多个参数时，就需要用到圆括号了

