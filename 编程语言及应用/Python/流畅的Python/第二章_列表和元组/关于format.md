format函数可以代替print传统的标准输入输出模式
* 最常见、最简便的用法：
```python
a = "lda"
b = 1
print(f"hello {a, b}")  # a,b可以是任意类型的变量
```
* 较为完整的写法："str{1}{0}".format(a,b),.format()的括号内是要代替字符串括号的内容，而大括号内的数字则表示要用第几个.format()内的参数来替换这个括号,不写数字则使用默认顺序
* 也可以通过传入字典来使用
```python
# 解包的字典
a = {'lda':'sb'}
print("This people is {lda}".format(lda='sb'))
# 或者实际上完全相同的
print("This people is {lda}".format(**a))
# 没有解包的字典
print("This people is {0[lda]}".format(a))
```
* .format()中传入列表
```python
my_list = ['lda', 'xiesenlin']
print('There are two people {0[0]} and {0[1]}'.format(my_list))
# 或者
print('There are two people {0} and {1}'.format(*my_list))
```

* 使用.format()的标准输出

<p>下表展示了 str.format() 格式化数字的多种方法：</p>
<pre>
&gt;&gt;&gt; print("{:.2f}".format(3.1415926))
3.14
</pre>
<table class="reference">
<tbody><tr><th width="10%">数字</th><th width="30%">格式</th><th width="30%">输出
</th><th width="30%">描述</th></tr>
<tr><td> 3.1415926 </td>
    <td> {:.2f} </td>
    <td> 3.14 </td>
    <td> 保留小数点后两位 </td>
</tr>
<tr><td> 3.1415926 </td>
    <td> {:+.2f} </td>
    <td> +3.14 </td>
    <td> 带符号保留小数点后两位 </td>
</tr>
<tr><td> -1 </td>
    <td> {:+.2f} </td>
    <td> -1.00 </td>
    <td> 带符号保留小数点后两位 </td>
</tr>
<tr><td> 2.71828 </td>
    <td> {:.0f} </td>
    <td> 3 </td>
    <td> 不带小数 </td>
</tr>
<tr><td> 5 </td>
    <td> {:0&gt;2d} </td>
    <td> 05 </td>
    <td> 数字补零 (填充左边, 宽度为2) </td>
</tr>
<tr><td> 5 </td>
    <td> {:x&lt;4d} </td>
    <td> 5xxx </td>
    <td> 数字补x (填充右边, 宽度为4) </td>
</tr>
<tr><td> 10 </td>
    <td> {:x&lt;4d} </td>
    <td> 10xx </td>
    <td> 数字补x (填充右边, 宽度为4) </td>
</tr>
<tr><td> 1000000 </td>
    <td> {:,} </td>
    <td> 1,000,000 </td>
    <td> 以逗号分隔的数字格式 </td>
</tr>
<tr><td> 0.25 </td>
    <td> {:.2%} </td>
    <td> 25.00% </td>
    <td> 百分比格式 </td>
</tr>
<tr><td> 1000000000 </td>
    <td> {:.2e} </td>
    <td> 1.00e+09 </td>
    <td> 指数记法 </td>
</tr>
<tr><td> 13 </td>
    <td> {:&gt;10d} </td>
    <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;13</td>
    <td> 右对齐 (默认, 宽度为10) </td>
</tr>
<tr><td> 13 </td>
    <td> {:&lt;10d} </td>
    <td> 13 </td>
    <td> 左对齐 (宽度为10)</td>
</tr>
<tr><td> 13 </td>
    <td> {:^10d} </td>
    <td> &nbsp;&nbsp;&nbsp;&nbsp;13 </td>
    <td> 中间对齐 (宽度为10) </td>
</tr>
<tr><td> 11 </td>
    <td><pre>'{:b}'.format(11)
'{:d}'.format(11)
'{:o}'.format(11)
'{:x}'.format(11)
'{:#x}'.format(11)
'{:#X}'.format(11)</pre></td>
    <td><pre>1011
11
13
b
0xb
0XB
</pre></td>
    <td> 进制</td>
</tr>
</tbody></table>
<p><span class="marked">^</span>, <span class="marked">&lt;</span>, <span class="marked">&gt;</span> 分别是居中、左对齐、右对齐，后面带宽度， <span class="marked">:</span> 号后面带填充的字符，只能是一个字符，不指定则默认是用空格填充。</p><p>
<span class="marked">+</span> 表示在正数前显示 <span class="marked">+</span>，负数前显示 <span class="marked">-</span>；<span class="marked">&nbsp;</span> （空格）表示在正数前加空格</p>
<p>b、d、o、x 分别是二进制、十进制、八进制、十六进制。</p>

<p>此外我们可以使用大括号 <span class="marked">{}</span> 来转义大括号，如下实例：</p>

<div class="example"> 
<h2 class="example">实例</h2> 
<div class="example_code">
<div class="hl-main"><span class="hl-comment">#!/usr/bin/python</span><span class="hl-code">
</span><span class="hl-comment"># -*- coding: UTF-8 -*-</span><span class="hl-code">

</span><span class="hl-identifier">print</span><span class="hl-code"> </span><span class="hl-brackets">(</span><span class="hl-quotes">&quot;</span><span class="hl-string">{} 对应的位置是 {{0}}</span><span class="hl-quotes">&quot;</span><span class="hl-code">.</span><span class="hl-identifier">format</span><span class="hl-brackets">(</span><span class="hl-quotes">&quot;</span><span class="hl-string">runoob</span><span class="hl-quotes">&quot;</span><span class="hl-brackets">)</span><span class="hl-brackets">)</span></div>
</div>
</div><p>输出结果为：</p>
<pre>
runoob 对应的位置是 {0}
</pre><hr>
