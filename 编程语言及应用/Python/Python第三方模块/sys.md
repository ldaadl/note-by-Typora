# sys常用类和函数

# 其他详解

## print和sys.stdout

​	python中的print语句实现打印操作，但是print函数的本质是将一个躲着多个对象转化为文本表达形式，然后发送给标准输出流或者类似的文件流。

​	实际上print是将传入的参数写入到了stdout流，stdout流在sys模块中，绑定的是sys.stdout，print(123)实际上是sys.stdout.write('123'+'\n')。看到这其实有一个小技巧可以使用了，就是改变sys.stdout绑定的内容，可以改为一个文件对象或者任何其他对象，前提是要实现write方法。