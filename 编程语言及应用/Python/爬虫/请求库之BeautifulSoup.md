# 请求库之BeautifulSoup4

在使用BeautifulSoup之前，我们必须安装bs4库，和一个推荐的解析器库lxml。

所有解析器名都要以字符串传入



示例：

``````python
from bs4 import BeautifulSoup
import lxml

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, lxml)
print(soup.prettify())  # 可以明显看到解析后的格式和解析前相比有序的多

``````

​	上述示例中，BeautifulSoup将一个html文档解析为BeautifulSoup对象，但是需要指出的是这个文档可以是一个字符串，也可以是一个文件对象.

``````python
BeautifulSoup(open('a.html'))
``````

​	**文档会被转化为Unicode编码**

## 一、四个重要对象

### 1.Tag

``````python
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>')
tag = soup.b
type(tag)
# <class 'bs4.element.Tag'>
``````



​	Tag对象等同于html文档中的标签

#### a.重要属性之name

​	这里的name不同于html标签中的name属性，这个name的含义是标签名，例如\<p\>中的p

``````python
tag.name
# b
``````

name属性可更改

`````python
tag.name = "blockquote"
tag
# <blockquote class="boldest">Extremely bold</blockquote>
`````

#### b.重要属性之Attributes

​	tag的属性

``````python
tag['class']
# boldest
tag.attrs
# {'class':'boldest',}
``````

​	tag的属性可以增删查改，操作方法和字典类似

#### c.多值属性

​	有的tag属性可以包含多个值，例如class一个tag可以引用多个CSS的class

​	在BeautifulSoup中一个多值属性（即使只有一个值）的返回值为列表。

### 2.NavigableString

​	该对象是文本内容，既包括标签所包含的也包括标签之间的（常常容易被忽略的是标签之间的回车换行）

​	该对象不可编辑，但是可以替换

````python
tag.string.replace_with('替换字符串')
````

​	该对象是BeautifulSoup对象的一部分，如果要在外部使用这个对象，可以用unicode()方法直接将其转换为普通unicode字符串。

### 3.BeautifulSoup

​	唯一需要说的是BeautifulSoup的name属性是document

### 4.Comment对象

​	Comment是NavigableString的子类，可用以表示注释之类

​	bs4还有一些其他对象，他们如同Comment一样都是NavigableString的子类，都是用于表示一些注释和特殊字符。

## 二、遍历文档树

### 1.子节点

#### a.获取

​	在html文档中，tag可以是层层嵌套的，BeautifulSoup中也是这样

`````python
soup.head.title
soup.body.p

soup.a
# 当a在文档中不是唯一的时候，这样只能获取第一个a标签
# 想找到所有的a需要使用find_all方法
soup.find_all('a')  # 返回列表
`````

​	需要注意，标签中包裹的文本不是标签但也是子节点，但是它没有子节点

#### b.contents和children

​	.contents获取标签的全部子标签，以列表（列表的每个元素是该标签对象）的形式返回

​	children和contents很相似，只不过children返回的是生成器

#### c.descendants

​	该属性只包括tag的直接子节点

#### d.string

​	如果tag只有一个 `NavigableString` 类型子节点，那么通过`string`可以得到（文本节点必须是这个tag的直接子对象）

​	值得一提的是，当tag只有一个子节点时，及时它不是`NavigableString`类型，也可以通过string得到

​	其他情况返回none

#### e.strings和stripped_strings

​	tag中如果包含多个文本(所有子节点都算在内，与上面的string有较大区别)，可以使用strings返回一个生成器，获取每一个的文本

​	stripped_strings与strings类似，只不过返回的内容中少了首尾空白字符和空白行。

#### d.get_text()

get_text()和strings的功能很类似,但是功能更强大

`````````python
markup = '<a href="http://example.com/">\nI linked to <i>example.com</i>\n</a>'
soup = BeautifulSoup(markup)

# 获取strings,以空格形式分隔
soup.get_text()
u'\nI linked to example.com\n'
soup.i.get_text()
u'example.com'


# soup.get_text("|")，以为分隔符
u'\nI linked to |example.com|\n'


# soup.get_text("|", strip=True)，消除每个string首尾的空白字符，相当于stripped_strings
u'I linked to|example.com'
`````````



### 2.父节点

#### a.parent

#### b.parents

​	parents获取元素的所有父辈节点

`````python
link = soup.a
link
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
for parent in link.parents:
    if parent is None:
        print(parent)
    else:
        print(parent.name)
# p
# body
# html
# [document]
# None
`````

### 3.兄弟节点

#### a.next_sibling和previous_sibling

使用这两个属性1时要注意，空白字符和字符串也是节点，这两个属性经常会获取到空白字符

#### b.next_siblings和previous_siblings

### 4.前进和回退

#### a.next_element和previous_element

​	next_sibling获取的是下一个和自己平级的兄弟节点，而next_element则是获取的按文档顺序来的下一个节点，无论这个节点是它的子节点还是其他什么节点。

#### b.next_elements和previous_elements

## 三、搜索文档树

​	搜索文档树最重要的是find和find_all函数

### 1.过滤器

​	过滤器可以理解为使用函数搜索文档时的依据

#### a.字符串

``````python
soup.find_all('b')
# 传入的参数并不是和文档内容任意匹配，而是匹配标签名
# [<b>The Dormouse's story</b>]
``````

也可以传入byte类型，但是会被当做utf-8编码，

#### b.正则表达式

​	这里的正则表达式必须是编译后的正则表达式

``````python
import re
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
# body
# b
``````

#### c.列表

``````python
soup.find_all(["a", "b"])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
``````

​	简单来说就是同事搜索a和b

#### d.True

​	返回所有除文本外的标签节点

#### e.自定义方法作为过滤器

​	自定义方法可以接受一个参数（文档中的标签对象），返回True或者False

例如：

`````python
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')
`````

### 2.find_all详解

#### a.各参数和用法详解

find_all(name,attrs,recursive,text,**kwargs)

* name查找标签的名字，可以传入任何类型的过滤器

* **kwargs

  ``````python
  find_all(id='hello')
  # 查找属性id为hello的tag
  soup.find_all(href=re.compile("elsie"))
  soup.find_all(id=True)
  # 可使用除自定义函数之外的所有过滤器
  
  data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
  data_soup.find_all(data-foo="value")
  # SyntaxError: keyword can't be an expression
  # 有些属性无法识别，但是按使用attrs可以避免这个问题
  data_soup.find_all(attrs={"data-foo": "value"})
  # [<div data-foo="value">foo!</div>]
  ``````

* 按CSS搜索：按CSS搜索实际上还是对tag的class属性的搜索，既可以用attrs参数也可以用**kwargs参数，但是特别注意的是，再使用\*\*kwargs参数时，必须使用`class_=''`的形式，要增加一个下划线，这是为了防止和关键字class相冲突。此外class作为一个多值属性，多个值可以用空格分隔（多个值注意他们的顺序）。

* text参数：text搜索文档中的字符串内容，text接收除自定义函数之外的所有过滤器。text参数单独使用时是搜索字符串，但是和其他参数结合使用则可以查找tsg

  `````python
  soup.find_all("a", text="Elsie")
  # [<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>]
  `````

* limit：limit也是对**kwargs参数的运用，limit可以限制返回结果的数量，这在返回结果非常巨大时可以起作用

  `````python
  soup.find_all("a", limit=2)
  # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
  #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
  `````

* recursive参数：该参数默认为True，这表示find_all函数将检索当前tag的所有子标签，可以设置该参数为False，则表示只检索当前tag的直接子节点



#### 	b.简便的调用方法

```````python
soup.find_all("a")
soup("a")

soup.title.find_all(text=True)
soup.title(text=True)
```````

### 3.其他搜索函数

#### a.find详解

find( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find和find_all一样，只不过返回的是一个tag对象（单个），而不是列表（多个）

#### b.find_parents和find_parent

find_parents( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find_parent( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

这两个函数和find_all、find相似，只不过搜索的是父节点

#### c.find_next_siblings和find_next_sibling

find_next_siblings( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find_next_sibling( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

#### d.find_previous_siblings和find_previous_sibling()

find_previous_siblings( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find_previous_sibling( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

#### e.find_all_next 和 find_next

find_all_next( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find_next( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

#### f.find_all_previous 和 find_previous

find_all_previous( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

find_previous( [name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id32) , [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#css) , [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#recursive) , [text](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#text) , [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#keyword) )

### 4.CSS选择器

​	CSS选择器是css作用于html文档的一种语法，而BeautifulSoup中可以使用这种语法来搜索文档树，使用这种语法的是select方法。

​	由于我对CSS选择器语法不太熟，这里就复制粘贴一些例子：

通过tag名查找

``````python
soup.select("title")
# [<title>The Dormouse's story</title>]

soup.select("p nth-of-type(3)")
# [<p class="story">...</p>]
``````

通过tag标签逐层查找

`````python
soup.select("body a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("html head title")
# [<title>The Dormouse's story</title>]
`````

查找直接子标签：

```````python
soup.select("head > title")
# [<title>The Dormouse's story</title>]

soup.select("p > a")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("p > a:nth-of-type(2)")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

soup.select("p > #link1")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select("body > a")
# []
```````

找到兄弟节点标签

``````python
soup.select("#link1 ~ .sister")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie"  id="link3">Tillie</a>]

soup.select("#link1 + .sister")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
``````

通过CSS类型查找：

`````python
soup.select(".sister")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select("[class~=sister]")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
`````

通过tag的id查找

`````python
soup.select("#link1")
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select("a#link2")
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
`````

通过是否存在某个属性来查找

``````python
soup.select('a[href]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
``````

通过属性的值来查找：

``````python
soup.select('a[href="http://example.com/elsie"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.select('a[href^="http://example.com/"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href$="tillie"]')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.select('a[href*=".com/el"]')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
``````

通过语言设置来查找

``````python
multilingual_markup = """
 <p lang="en">Hello</p>
 <p lang="en-us">Howdy, y'all</p>
 <p lang="en-gb">Pip-pip, old fruit</p>
 <p lang="fr">Bonjour mes amis</p>
"""
multilingual_soup = BeautifulSoup(multilingual_markup)
multilingual_soup.select('p[lang|=en]')
# [<p lang="en">Hello</p>,
#  <p lang="en-us">Howdy, y'all</p>,
#  <p lang="en-gb">Pip-pip, old fruit</p>]
``````

## 四、修改文档树

### 1.在tag中修改

#### a.修改tag的名称和属性

前面已经提到过，修改方式和字典十分相似

`````python
# 修改名称
tag.name = ''
# 修改属性
tag['class'] = ''
# 删除属性
del tag['class']
`````

#### b.修改string

`````python
# 相当于tag.string.replace('')
tag.string = '新的内容'
`````

### 2.在tag的末尾插入

#### a.append()向tag中增加NavigableString

`````python
soup = BeautifulSoup("<a>Foo</a>")
soup.a.append("Bar")

soup
# <html><head></head><body><a>FooBar</a></body></html>
soup.a.contents
# [u'Foo', u'Bar']
`````

#### b.向tag中增加tag和注释

`````python
from bs4 import Comment
new_comment = soup.new_string("Nice to see you.", Comment)
tag.append(new_comment)
tag
# <b>Hello there<!--Nice to see you.--></b>
tag.contents
# [u'Hello', u' there', u'Nice to see you.']


soup = BeautifulSoup("<b></b>")
original_tag = soup.b

new_tag = soup.new_tag("a", href="http://www.example.com")
original_tag.append(new_tag)
original_tag
# <b><a href="http://www.example.com"></a></b>

new_tag.string = "Link text."
original_tag
# <b><a href="http://www.example.com">Link text.</a></b>
`````

### 3.在节点的指定位置插入

#### a.insert()

``````python
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
tag = soup.a

tag.insert(1, "but did not endorse ")
tag
# <a href="http://example.com/">I linked to but did not endorse <i>example.com</i></a>
tag.contents
# [u'I linked to ', u'but did not endorse', <i>example.com</i>]
``````

将插入tag的所有直接子节点视为一个列表，tag.insert(列表位置,内容)

#### b.insert_before()和insert_after()

这两个方法相当于对一个tag插入兄弟节点

### 4.移除节点

#### a.clear()

这个方法清除当前节点下的所有子节点

#### b.extract()

将当前t节点移除文档树，并且返回，返回的是一个新的文档树

#### c.decompose()

将当前节点移除并且销毁

### 5.修改节点

#### a.replace_with()

`PageElement.replace_with()` 方法移除文档树中的某段内容,并用新tag或文本节点替代它:

``````python 
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

new_tag = soup.new_tag("b")
new_tag.string = "example.net"
a_tag.i.replace_with(new_tag)

a_tag
# <a href="http://example.com/">I linked to <b>example.net</b></a>
``````

#### b.wrap()

`PageElement.wrap()` 方法可以对指定的tag元素进行包装 [[8\]](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id89) ,并返回包装后的结果:

````python
soup = BeautifulSoup("<p>I wish I was bold.</p>")
soup.p.string.wrap(soup.new_tag("b"))
# <b>I wish I was bold.</b>

soup.p.wrap(soup.new_tag("div"))
# <div><p><b>I wish I was bold.</b></p></div>
````

#### c.unwrap()

`Tag.unwrap()` 方法与 `wrap()` 方法相反.将移除tag内的所有tag标签,该方法常被用来进行标记的解包:

``````python
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup)
a_tag = soup.a

a_tag.i.unwrap()
a_tag
# <a href="http://example.com/">I linked to example.com</a>
``````

## 五.输出

### 1.格式化输出prettify()

prettify()方法将文档树格式化后以unicode编码输出，每个xml/html标签独占一行

### 2.压缩输出

直接使用str或者unicode方法

``````python
str(soup)
# '<html><head></head><body><a href="http://example.com/">I linked to <i>example.com</i></a></body></html>'

unicode(soup.a)
# u'<a href="http://example.com/">I linked to <i>example.com</i></a>'
``````

## 六.编码

任何HTML或XML文档都有自己的编码方式,比如ASCII 或 UTF-8,但是使用Beautiful Soup解析后,文档都被转换成了Unicode:

``````python
markup = "<h1>Sacr\xc3\xa9 bleu!</h1>"
soup = BeautifulSoup(markup)
soup.h1
# <h1>Sacré bleu!</h1>
soup.h1.string
# u'Sacr\xe9 bleu!'
``````

BeautifulSoup大多数时候会自动检测出文档的编码，并将其转为unicode编码，但是少数时候也会出错，这时候需要手动指定编码：

``````python
soup = BeautifulSoup(markup, from_encoding="iso-8859-8")
soup.h1
<h1>םולש</h1>
soup.original_encoding
'iso8859-8'
``````

