# 第十五章 else和上下文管理器

## 1.else的较少的用法

​	一般我们见到else的地方都是if/else，这表示一种对立的关系，要么if实现，要么else实现。但是else在某些地方的使用更偏向于then的意思。这些地方就是try、while、for/else，在这些地方使用时就表示，如果try、while、for正常执行完毕，那么else中的内容也会执行，如果遇到异常、break、return等意外跳出了try、while、for，那么else内的内容将不会被执行。

​	一个使用的场景：

`````python
try:
    func1()
except:
    func2()
else:
    func3()
`````

想象这样一个场景，我们要使用函数func1()和func3(),但是func1()有抛出异常的风险，但是func3()是绝对安全的;如果一旦发生异常，我们将抛弃函数func1和func3的组合，转而使用func2(),这个时候try/else就能很好地发挥作用。

**需要注意的是try/else不能和try/finally同时使用**。

## 2.上下文管理器

​	<u>上下文管理器与函数一样有着代码复用的功能，只不过复用的是上下文（不换壳）。</u>

### 上下文管理器介绍	

​	我们在进行I/O编程的时候，会用到with，我们用with的原因是因为，它可以自动帮我们关闭文件。with的用法是Python的一种语法，而他的背后既是上下文管理器。

​	with用法的目的是简化try/finally，即自动地完成一些必要的操作。迭代器是实现了\_\_iter\_\_和\_\_next_\_方法的类，上下文管理器与迭代器有一点类似，它是实现了\_\_enter\_\_（只有一个self参数）和\_\_exit\_\_（一个self参数和三个接受异常的参数，默认为三个None）的类。with调用上下文管理器的过程大概是：运行第一句with时，调用创建上下文管理器，并调用\_\_enter\_\_，如果有as则把\_\_enter__的返回值绑定到as后面的引用，当with模块内的语句运行完毕之后执行\_\_exit\_\_(完成try/finally中finally的任务)。

例子：

`````python
class LookingClass:
    
    def __enter__(self):
        import sys
        self.original_write=sys.stdout.write
        sys.stdout.write=self.reverse_write
        return 'JABBERWOCKY'
    
    def reverse_write(self, text):
        self.original_write(text[::-1])
        
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write=self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True

# 不使用with手动执行上下文管理器
manager=LookingClass()
monster=manager.__enter__()
print(monster)
print('hello world')
manager.__exit__()
`````

### 与上下文管理器相关的装饰器

​	主要介绍contextlib模块中的contextmanager装饰器

`````python
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write=sys.stdout.write
    
    def reverse_write(text):
        original_write(text[::-1])
        
    sys.stdout.write=reverse_write
    msg=''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg='Please DO NOT divide by zero!'
    finally:
        sys.stdout.write=original_write
        if msg:
            print(msg)
`````

@contextmanager装饰器是将一个特殊的生成器函数包装为上下文管理器，yield语句及其前面部分将会被包装成\_\_enter\_\_，后面的则被包装成\_\_exit\_\_，注意上述例子中的异常捕捉如果with块内出现异常，那么这个异常将会在yield处抛出，如果我们没有进行异常检测，yield后面的代码将无法执行，即\_\_exit\_\_将不会执行，所以finally和except是必须的。