import collections
from random import choice

Card = collections.namedtuple('Card', ['rank', 'suit'])  # collections.namedtuple创建了一个简单类


# namedtuple'用于构建只有少数属性却没有方法的对象，namedtuple('类名', [列表内容为字符串组成的属性名])
# python3所有类是默认继承object类的，object本身就具有许多属性和方法
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._card = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]  # Card对象为元素的列表

    def __len__(self):
        return len(self._card)

    def __getitem__(self, position):
        return self._card[position]


if __name__ == "__main__":
    deck = FrenchDeck()
    print(len(deck))  # deck.len()
    print(deck[0])  # deck.getitem(0),这里类自己的方法代替了通用的魔术方法
    choice(deck)  # 显然，choice()也依赖于方法__getitem__()

    # 查看最上面的三张牌, 显然，切片也离不开__getitem__
    print(deck[:3])
    print(deck[12::13])  # 只看牌面为A的牌
    # 使用了__getitem__方法后，deck变为可迭代的了
    for card in deck:
        print(card)
    for card in reversed(deck):
        print(card)
    # 当deck成为可迭代对象之后，很多常用的方法都可以使用了
    Card('Q', 'hearts') in deck
    Card('7', 'beasts') in deck
    # 实现排序
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


    def spades_high(card):
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]

    # sorted()和list中使用的sort()不同，sorted可用于全体可迭代对象，sorted(iterable, cmp=None, key=None, reverse=False)
    # cmp 必须为一个有两个参数的函数，用于比较两个参数的大小，大于则返回1,等于返回0,小于返回-1，sorted将会把literable中的所有元素传入cmp根据cmp的结果设置排序.key为只有一个参数的函数，，
    # key调用后返回一个值，sorted跟据这个值为literable排序
    for card in sorted(deck, key=spades_high):
        print(card)
