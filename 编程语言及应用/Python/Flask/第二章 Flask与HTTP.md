# 第二章 Flask与HTTP

## 一.Flask中的Request对象

flask中的request对象封装了请求对象从客户端发来的请求报文。

`````python
from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    name=request.args.get('name', 'Flask')
    return '<h1>Hello, %s!</h1>' % name
`````



### 1.request对象获取URL

假设URL是http://baidu..com/index?name=flask

| 属性      | 值                                  |
| --------- | ----------------------------------- |
| path      | 'index'                             |
| full_path | 'index?name=flask'                  |
| host      | ‘baidu.com’                         |
| host_url  | 'http://baidu.com/'                 |
| base_url  | 'http://baiducom/index'             |
| url       | 'http://baidu.com/index?name=flask' |
| url_root  | 'http://baidu.com/'                 |

### 2.request对象获取报文中的其他部分

| 属性或者方法 | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| args         | 存储解析后的查询字符串，可以通过键值对的方式访问，要获取未解析的原生查询字符串可以通过query_string访问 |
| blueprint    | 当前蓝本的名称                                               |
| cookies      | 包含所有cookies的字典                                        |
| endpoint     | 与当前请求匹配的端点值                                       |
| files        | 包含所有上传文件，可以用键值对的方式获取，键是上传文件的input标签的name值 |
| form         | 与files类似                                                  |
| values       | 结合了args和form                                             |
| get_data     |                                                              |
| get_json     |                                                              |
| headers      |                                                              |
| is_json      |                                                              |
| json         |                                                              |
| method       |                                                              |
| referer      |                                                              |
| scheme       |                                                              |
| user_agent   |                                                              |

files、form、args等是Werkzeug中的MuliDict或者ImmutableMultiDict类，这两个类是Dict的子类，他们可以通过键值对访问数据，如果没有对应的键不会报错而会返回HTTP 400错误，但是可以通过使用get方法来避免。

## 二.在Flask中处理请求

### 1.路由匹配

flask routes命令得到：

<img src="./images/2.png">

从左到右：端点	方法	路由

### 2.设置监听路由的HTTP方法

这里说的HTTP方法即是GET、POST等方法，一般只会在程序中设置GET、HEAD、OPITION等方法。DELETE、PUT等方法在构建Web API时才会使用。



设置方法：@app.route(路由,methods=['GET','POST'])

### 3.URL处理































