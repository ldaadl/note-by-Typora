# 普通Python脚本引用

``````python
# 引用python包，在其默认路径里
import math
from math import sqrt
# 引用本项目的其他Python脚本
import first
from first import a
# 引用其他目录的Python脚本;注意这里采用的是 . 号连接路径
from .ui.second import *
# 或者，在利用sys模块在此python脚本里增加路径
import sys
sys.path.append('要引用的脚本所在的目录')
import second
``````

# 自编写包的引用

* 报的编写方式:这里主要要注意的是_\_init__.py真个包的引用的影响。
* * _\_init__.py中引用同一个包的文件，也要用 . 号连接引用
  * 可以通过设置import使外部引用包变的方便
  * 而_\_all__变量的作用是限定import引入的内容