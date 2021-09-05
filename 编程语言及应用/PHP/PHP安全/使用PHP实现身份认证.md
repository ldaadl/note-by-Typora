# 使用PHP实现身份认证

​	我们创建一个简单的页面来进行验证：

`````php+HTML
<!DOCTYPE html>
<html>
<head>
   <title>Secret Page</title>
</head>
<body>

<?php
  if ((!isset($_POST['name'])) || (!isset($_POST['password']))) {
  // visitor needs to enter a name and password
?>
    <h1>Please Log In</h1>
    <p>This page is secret.</p>
    <form method="post" action="secret.php">
    <p><label for="name">Username:</label> 
    <input type="text" name="name" id="name" size="15" /></p>
    <p><label for="password">Password:</label> 
    <input type="password" name="password" id="password" size="15" /></p>
    <button type="submit" name="submit">Log In</button>    
    </form>
<?php
  } else if(($_POST['name']=='user') && ($_POST['password']=='pass')) {
    // visitor's name and password combination are correct
    echo '<h1>Here it is!</h1>
          <p>I bet you are glad you can see this secret page.</p>';
  } else {
    // visitor's name and password combination are not correct
    echo '<h1>Go Away!</h1>
          <p>You are not authorized to use this resource.</p>';
  }
?>
</body>
</html>
`````

​	这样验证身份将会带来四个问题：

* 一个php脚本中保存的密码和账户数量有限
* 只保护一个页面，其他页面的访问要么无需输入密码，要么每次都向这样输入密码。这显然不方便
* 密码以文本形式保存
* 密码传输以明文形式

## 解决问题

### 密码的存储和传输

  上面那个脚本中对用户名和密码的处理是直接在脚本中验证，现实中不可能只有一个或者几个用户，大量用户不适合存放于脚本中，可以选择存放于文件，或者数据库中（更好）。如果存放于文件中，一定要注意文件存放的位置，不要存放于web文档树中。

  此外，密码在服务器端明文存储也不是一个好的选择，常有的做法是使用函数对密码进行单项hash后，存储hash值。

  关于密码明文传输的问题，这里使用表单提交密码和用户名一定是无法做到加密的，这里需要使用http基本认证解决这个问题。

### 使用基本认证

#### 编写PHP脚本实现基本认证

`````php+HTML
<?php
if ((!isset($_SERVER['PHP_AUTH_USER'])) &&
    (!isset($_SERVER['PHP_AUTH_PW'])) &&
    (substr($_SERVER['HTTP_AUTHORIZATION'], 0, 6) == 'Basic ')
   ) {

  list($_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW']) =
    explode(':', base64_decode(substr($_SERVER['HTTP_AUTHORIZATION'], 6)));
}

// Replace this if statement with a database query or similar
if (($_SERVER['PHP_AUTH_USER'] != 'user') ||
   ($_SERVER['PHP_AUTH_PW'] != 'pass')) {

   // visitor has not yet given details, or their
   // name and password combination are not correct

  header('WWW-Authenticate: Basic realm="Realm-Name"');
  header('HTTP/1.0 401 Unauthorized');
} else {
?>
<!DOCTYPE html>
<html>
<head>
   <title>Secret Page</title>
</head>
<body>
<?php

echo '<h1>Here it is!</h1>
      <p>I bet you are glad you can see this secret page.</p>';
}
?>
</body>
</html>
`````

  这里首先解释一下$_SERVER[]，显然这个是和$\_POST差不多的东西，但是$\_SERVER是获取超全局变量的方法，这些变量包括服务器的配置的一些变量、HTTP首部等内容。

  我们先看第二个if的内容，判断条件是对用户账号的密码的匹配判断，如果失败则调用header()函数。header()函数用于给http报文添加首部，必须在任何打印语句出现前调用。这里理所应当的，若用户不匹配，则返回401和WWW-Authenticate: Basic realm="Realm-Name"，401无需多说，WWW-Authenticate首部会使客户端开启一个认证弹窗，这就是http基本认证。

<img src="./image/1.png">

Basic表示认证类型是Basic，时最常见的一种类型。后面的realm=“。。。”，字符串相当于是提示信息。

​	接下来让我们看看HTTP是如何将密码与账户返回的：

````http
HTTP/1.1 200 OK
Date: Tue, 20 Jul 2021 06:20:39 GMT
Server: Apache
X-Powered-By: PHP/5.5.38
Content-Length: 172
Connection: close
Content-Type: text/html
````

`````http
GET /test/sixteen/basic_auth.php HTTP/1.1
Host: 120.27.226.67
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Authorization: Basic c2FzYXM6YXNhc2FzYXM=
`````

  响应头无需多说，而请求头注意观察Authorization: Basic c2FzYXM6YXNhc2FzYXM=，这是与认证有关的首部Basic后的是 用户名:密码 形式经过base64编码的结果，这一定程度上解决了密码明文传输的问题，但是还是不够安全，使用HTTPS则可以更好地解决这个问题。

  第一个if中的内容比较简单，只需要i简单介绍一下几个函数：

* explode(分隔字符,字符串)，将字符串以分隔字符为间隔分隔并返回数组
* list(变量1，变量2，。。。) = 数组 ，将数组的赋值给多个变量。

#### 使用apache配置的http基本认证

  除了编写脚本之外，也可以直接使用apache的配置开启http基本认证。这里使用了.htaccess文件，.htaccess文件存放于web文档树的某个目录下，表示apache对这个目录下的配置，需要知道的是，这个文件并不推荐使用，一是因为访问该目录下任何脚本时apache都会先访问这个文件，这会使服务器的效率降低，还有一个是apache的主配置文件可以做到.htacess能做到的任何事，而且比它更安全，.htaccess位于文档树中有被恶意用户访问的危险。 

`````txt
// 表示验证用户与密码的文件
AuthUserFile /www/web/default/test/sixteen/idenByHta/.htpass
//  认证类型
AuthType Basic
// 提示信息
AuthName "Authorization Needed"
// 认证提供方，这里是file表示文件
AuthBasicProvider file
// 指定可访问的用户，这里是认证用户，也可以是特定用户或用户组
Require valid-user
// 不同的返回响应码可以提供不同文件，而不是使用浏览器的默认页面
ErrorDocument 404 /www/web/default/test/sixteen/idenByHta/rejection.html
`````

关于文件.htpass，这个文件是使用apache工具组中的htpasswd创建的：

htpasswd -bc 文件名 用户名 密码

注意两点，一是选项c只有首次创建用户时才调用，否则会覆盖已有的文件；二是创建的文件必须放于web文档树外。



关于apache的配置：

1. 这里的认证功能用到了mod_auth_basic模块和一个重定向模块，必须在配置文件中去掉他们前面的#，启用他们
2. apache的.htaccess功能是默认关闭的，需要在配置文件中选择使用它

````xml
# Directory标签后面跟的路径是配置作用目录
<Directory "/www/web/default/test/sixteen/idenByHta">
    AllowOverride All
    Require all granted
</Directory>
````



apache配置的http基本认证和php脚本编写的认证都是使用了WWW-Authenticate首部，无太大差别，只不过apache配置HTTP基本认证对鉴别的处理直接交由apache服务器处理了。





  