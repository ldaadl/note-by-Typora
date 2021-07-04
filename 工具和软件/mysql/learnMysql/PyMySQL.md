# pymysql概述

* pymysql相当于使用纯python实现的mysql客户端

# 连接和关闭游标

`````python
import pymysql

user = input('username:')
pwd  = input('password:')

conn=pymysql.connect(host='localhost',user='root',password='',database='db1')
cursor = conn.cursor()
sql = "select * from userinfo where user=%s and password=%s"
# sql = "select * from userinfo where user=%(u)s and password=%(p)s"
cursor.execute(sql,[user,pwd])
# cursor.execute(sql,{'u':user,'p':pwd})
ret = cursor.fetchone()

cursor.close()
conn.close()

if ret:
    print('登陆成功！')
else:
    print('登陆失败！')
`````

``````python
connect = pymysql.connect(省略)
# 使用上下文管理器免于关闭cursor
with connect.cursor() as cursor:
    。。。。。。
``````





# 增删查改

* 增删改需要cursor.commit()
* 查需要cursor.fetchone/fetchall
* 获取插入数据自增id,cursor.lastrowid