# 下例为将字符串变为Unicode码位的列表
symbols = '$%&*('
codes = []
for symbol in symbols:
    codes.append(ord(symbol))
# 或者
codes = [ord(symbol) for symbol in symbols]

# 使用列表推倒通常的原则是只用于创建新的列表，且尽量不超过两行
