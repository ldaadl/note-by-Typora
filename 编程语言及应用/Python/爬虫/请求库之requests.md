# 请求库之requests

## 一.初级用法

这里只简单补充知识点：

* requests.text和requests.comtent两者返回的内容相同，只不过前者是unicode的字符串，后者是bytes；后者常用于图片、视频、音频的获取
* requests.code.状态，可以得到各种状态码

* requests.json()可以将返回的json转为字典

## 二.高级用法

### 1.上传文件

``````python
import requests

a = open('github.ico', 'rb')
files = {'file': a}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

``````

### 2.cookies

获取遍历cookies

````python
import requests

url = 'https://www.baidu.com'
r = requests.get(url)
print(r.cookies)

for key,value in cookies.items():
    print(key,value)
````

设置cookies

``````python
import requests

url = 'https://www.zhihu.com/people/yi-yi-gu-xing-28-8'
headers = {
    'Cookies': '略',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.45'
                  '15.131 Safari/537.36',
}

r = requests.get(url, headers=headers)
print(r.text)
``````

还有另一种生成cookie的方式，要用到requests.cookies.RequestCookieJar对象，比较麻烦

### 3.维持会话

`````python
import requests
# 生成了一个会话
s = requests.Session()

url = 'https://www.baidu.com'
s.get(url)
`````

### 4.SSL证书验证

`````python
# 设置verify参数为False不进行证书验证
requests.get('https://www.baidu.com',verify=False)

# 指定本地证书
requests.get(url,cert=('证书文件路径','秘钥文件路径'))
`````

### 5.设置代理

``````python
proxies = {
    'http':'http://ip地址',
    'https':'http://ip地址'
}

requests.get(url,proxies=proxies)
``````

### 6.http基本认证

有三种解决方案：

* 设置cookies
* 在URL中使用user:pass@host

```python
requests.get(url,auth=(用户名,密码))
```

还有一些其他的认证方式有的需要一些额外的包

### 7.超时设置

```````python
# timeout为最长响应时间，单位为秒，默认为None，时间无限
requests.get(url,timeout=1)
```````

### 8.获取我们发送的请求

这在requests中是Prepared Request对象

```````python
s=Session()
req=Request('POST',url,data=data,headers=headers)
# 这就是我们的http请求
prepared=s.prepare_request(req)
r=s.send(prepared)
print(r.text)
```````

