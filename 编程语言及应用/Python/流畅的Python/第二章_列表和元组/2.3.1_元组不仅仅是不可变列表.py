# 元组还可以用作记录，即一个元组内存储某个事物的一些相关信息
traveler_id = [('USA', '1'), ('BRA', '2'), ('ESP', '3')]  # 每个元组内存储的是国家缩写和国家编号，这就是元组用作记录

for country, _ in traveler_id:
    print(country)
