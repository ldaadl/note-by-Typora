# OS模块

## 1.部分方法和属性简介

* os.name

  返回操作系统类型

  return str,'posix' is linux,'nt' is windows

* os.getcwd()

  get current work directory，获取当前的工作目录

  例如：'C:\\\\Users\\\\Administrator'

* os.listdir(path)

  列出目录下所有的文件和目录名,以列表形式返回

* os.remove(path)

  删除path指定的文件

* os.rmdir(path)

  删除指定目录

* os.mkdir(path)

  创建指定目录

* os.makedirs(path)

  可递归创建目录

* os.path.isfile(path)

  判断指定对象是否为文件

* os.path.isdir(path)

  判断指定对象是否为目录，返回True和False

* os.path.split(path)

  将文件的路径和文件名分隔，以元组形式返回

* os.path.exists(path)

  检验文件是否存在，返回True或者False

* os.chdir(path)

  移动当前目录到指定path

* os.system(cmd)

  执行系统命令，0代表成功，1代表不成功

* os.path.getsize(path)

  获取文件的大小，如果是目录返回0

* os.path.abspath(path)

  获取文件的绝对路径

* os.path.join(path,name)

  与os.path.split(path)相对，连接目录和文件名

* os.path.basename(path)

  返回文件名

* os.path.dirname(path)

  返回文件路径

* os.walk(top[,topdown=True[,onerror=None[,followlinks=False]]])

  这个函数遍历整个目录树，包括目录的子目录，每个目录由一个三元组表示，每个元组是一个列表：返回值root（当前目录，这里的当前目录是指正在办理的目录）、dirs（当前目录下的直接目录）、files（当前目录下的直接文件）

  top是要遍历的目录

  topdown为True是优先遍历top目录，否则优先遍历top子目录，这和数据结构中树的遍历的两种方法很像

  onerror需要一个callable对象，当wark异常时，会调用

  followlinks为True时会遍历目录下快捷方式所指向的目录