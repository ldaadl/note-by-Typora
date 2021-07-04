from collections import namedtuple

# nametuple可以生成简单的类，其实就是生成具名元组，这也是该函数名中带有tuple的原因
Card = namedtuple('Card', ['rank', 'suit'])
card1 = Card(1, 2)
tuple_card = namedtuple('Card', 'rank suit')  # 生成具名元组,第一个字符串是元组名，第二个字符串中由空格分割开的是元组内元素名
card2 = tuple_card(1, 2)

print(card2)
# 具名元组除了从普通元组继承来的属性以外，还有一些特有的属性和方法
print(card2._fields)  # 是包含这个具名元组所有字段名的元组
a = (1, 2)
card3 = tuple_card._make(a)  # _make()对传入的其他‘可迭代对象’进行解包，作为参数构造具名元组
print(card3._asdict())  # Python3.4时还是返回一个有序字典，Orderedict类型，但是目前我使用的3.9已经是返回一个字典

# naemdtuple构建的对象之是简单类，因为它访问属性的方式是Card.name而不是__getitem__,但是它又有元组的一些属性
