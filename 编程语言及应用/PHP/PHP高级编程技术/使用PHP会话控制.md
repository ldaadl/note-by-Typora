# 1.什么是会话控制

​	HTTP原本是 无状态协议 ，也就是说HTTP没有内置方法维护两个事物之间的状态，当用户请求完一个页面后再请求同一站点同一站点的另一页面时，HTTP仅本身无法判断两个请求是否来自同一用户。

​	会话控制的思想是在Web站点的单个会话中跟踪用户。可以支持用户登录后根据其身份访问内容，此外还可以记录用户的行为，实现购物车及用户在站点的其他动作。

​	PHP中对回话控制的操作依赖一些函数和$\_SESSION全局变量。

# 2.基本会话功能

​	一次HTTP会话是由一个会话ID所标识，这是一个加密后的随机数（MD5/SHA-1）,会话ID有PHP生成，客户端第一次请求需要页面时，通过set-cookie设或者URL参数返回给客户端。客户端再次请求同一页面的其他站点时，在cookie中带上这个会话ID，来标识一段会话。

​	会话ID也会注册在服务器端，默认情况下它保存在一个文件中，也可以通过自定义函数将其保存在数据库中。

### 1.关于cookie

​	cookie可以起到追踪页面、认证等功能。cookie的格式大致是：Set-Cookie:name=value;[expires=data;path=path;domian=domian_name;secure;HttpOnly]

这应该是一种标准形式，随便查看一个页面的内容，都可以发觉cookie中的内容与这些不太一样。

### 2.通过PHP设置cookie

```````php
// 设置cookie的函数原型
bool setcookie(string name,[,string value[,int expire=0[,string path[,string domain[,int secure=false[,int httponly=false]]]]]])
    
//读取cookie,示例cookie名为cookiename
$_COOKIE['cookiename']
```````

要删除一个cookie只需要调用setcookie函数，并为原cookie设置一个过期时间即可，或者调用函数header（）手工设置cookie。设置cookie的header函数必须在设置任何首部的header()之前调用，这是cookie的使用标准而不是PHP的限制。

### 3.在会话中使用cookie

会话中使用的cookie并不需要使用setcookie函数或者header函数设置，有专门的会话函数使用，但是可以通过函数session_set_cookie_params()查看会话设置的cookie，该函数的原型：

session_set_cookie_params(lifetime,path,domain,[,secure[,httponly]]);	各个参数起到接收返回值的作用。

### 4.保存会话ID

会话ID将在客户端保存，也有其他方法是将会话ID添加到URL（设置php.ini中的session.use_trans_sid或者在后端脚本的URL中手动加上会话ID），但是这样不安全。

### 5.会话控制配置

​	php.ini中有许多关于会话控制的配置，包括服务器端保存ID文件、会话ID加密方式等，此处不再多说。

# 三.会话的使用

### 1.启动会话

session_start()该函数会检测http请求中是否有一个活跃会话（cookie中的PHPSESSID,而且没有过期），如果有则该函数从相应文件中验证并载入会话变量，如果没有则创建一个会话变量则创建一个会话变量交由http响应报文中的Set-Cookie返回。

除了使用该函数，也可以设置php.ini中的seesion.auto_start使得有人访问网站时，会话自动启动。

### 2.注册会话变量

$_SEESION['变量名']=变量值;

设置会话变量之后，该变量会被记录，直到会话结束或者手工取消。会话过期时间由php.ini中的session.auth_start设置。

### 3.使用会话变量

使用前务必要用isset()或者empty()检查会话变量是否设置。

### 4.销毁变量和会话

unset($_SESSION['会话变量名'])即可销毁变量，不能使用unset($\_SESSION)因为这将会销毁会话数组，这表示将禁用会话。

要一次性销毁所有会话变量使用$_SESSION=array();

最后使用session_destroy()函数来销毁会话ID。

# 四.会话控制三个示例

### 1.登录界面

```````php+HTML
<?php
// 启动会话
session_start();

if (isset($_POST['userid']) && isset($_POST['password']))
{
  // if the user has just tried to log in
  $userid = $_POST['userid'];
  $password = $_POST['password'];

  $db_conn = new mysqli('localhost', 'webauth', 'webauth', 'auth');

  if (mysqli_connect_errno()) {
    echo 'Connection to database failed:'.mysqli_connect_error();
    exit();
  }

  $query = "select * from authorized_users where 
            name='".$userid."' and 
            password=sha1('".$password."')";

  $result = $db_conn->query($query);
  if ($result->num_rows)
  {
    // if they are in the database register the user id
    $_SESSION['valid_user'] = $userid;
  }
  $db_conn->close();
}
?>
<!DOCTYPE html>
<html>
<head>
   <title>Home Page</title>
    <style type="text/css">
      fieldset {
         width: 50%;
         border: 2px solid #ff0000;
      }
      legend {
         font-weight: bold;
         font-size: 125%;
      }
      label {
         width: 125px;
         float: left;
         text-align: left;
         font-weight: bold;
      }
      input {
         border: 1px solid #000;
         padding: 3px;
      }
      button {
         margin-top: 12px;
      }
    </style>
</head>
<body>
<h1>Home Page</h1>
<?php
  if (isset($_SESSION['valid_user']))
  {
    echo '<p>You are logged in as: '.$_SESSION['valid_user'].' <br />';
    echo '<a href="logout.php">Log out</a></p>';
  }
  else
  {
    if (isset($userid))
    {
      // if they've tried and failed to log in
      echo '<p>Could not log you in.</p>';
    }
    else
    {
      // they have not tried to log in yet or have logged out
      echo '<p>You are not logged in.</p>';
    }

    // provide form to log in
    echo '<form action="authmain.php" method="post">';
    echo '<fieldset>';
    echo '<legend>Login Now!</legend>';
    echo '<p><label for="userid">UserID:</label>';
    echo '<input type="text" name="userid" id="userid" size="30"/></p>';
    echo '<p><label for="password">Password:</label>';
    echo '<input type="password" name="password" id="password" size="30"/></p>';    
    echo '</fieldset>';
    echo '<button type="submit" name="login">Login</button>';
    echo '</form>';

  }
?>
<p><a href="members_only.php">Go to Members Section</a></p>

</body>
</html>
```````

​		第一次请求这个页面时，请求和得到的响应如下：

``````http
GET /test/twenty_two/authmain.php HTTP/1.1
Host: 120.27.226.67
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
``````

``````http
HTTP/1.1 200 OK
Date: Sat, 24 Jul 2021 05:17:18 GMT
Server: Apache
X-Powered-By: PHP/5.5.38
Set-Cookie: PHPSESSID=fv1h3t1uk18kpcg5m4hu3sf632; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Content-Length: 1069
Connection: close
Content-Type: text/html
``````

然后再次请求该页面，此时没有输入账户密码

``````http
GET /test/twenty_two/authmain.php HTTP/1.1
Host: 120.27.226.67
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: PHPSESSID=fv1h3t1uk18kpcg5m4hu3sf632
``````

`````http
HTTP/1.1 200 OK
Date: Sat, 24 Jul 2021 07:41:49 GMT
Server: Apache
X-Powered-By: PHP/5.5.38
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Content-Length: 1069
Connection: close
Content-Type: text/html
`````

​	注意这两次请求和响应的内容，第一次响应存在Set-Cookie，其内容是PHPSESSID，很明显这时一个会话ID，在第二次响应时，HTTP报文中的cookie就带上了这个ID，然后第二次相应并没有Set-Cookie这一项，原因是产生Set-Cookie直接原因是session_start()函数，第一次请求时函数没有检测到cookie中有PHPSESSID，故要先设置会话变量，第二次检测到了该会话变量故不再设置。

### 2.登录后才能访问的界面

`````php+HTML
<?php
  session_start();
?>
<!DOCTYPE html>
<html>
<head>
   <title>Members Only</title>
</head>
<body>
<h1>Members Only</h1>

<?php
  // check session variable
  if (isset($_SESSION['valid_user']))
  {
    echo '<p>You are logged in as '.$_SESSION['valid_user'].'</p>';
    echo '<p><em>Members-Only content goes here.</em></p>';
  }
  else
  {
    echo '<p>You are not logged in.</p>';
    echo '<p>Only logged in members may see this page.</p>';
  }
?>

<p><a href="authmain.php">Back to Home Page</a></p>

</body>
</html>
`````

### 3.登出界面

`````php+HTML
<?php
  session_start();

  // store to test if they *were* logged in
  $old_user = $_SESSION['valid_user'];
  unset($_SESSION['valid_user']);
  session_destroy();
?>
<!DOCTYPE html>
<html>
<head>
   <title>Log Out</title>
</head>
<body>
<h1>Log Out</h1>
<?php
  if (!empty($old_user))
  {
    echo '<p>You have been logged out.</p>';
  }
  else
  {
    // if they weren't logged in but came to this page somehow
    echo '<p>You were not logged in, and so have not been logged out.</p>';
  }
?>
<p><a href="authmain.php">Back to Home Page</a></p>

</body>
</html>
`````

### 4.总节

在这三个页面中，只有登录页面在用户的账户密码经过验证前就启动了一个会话，这段会话由一个会话ID标识，这ID被保存在文件中，而验证用户身份后，才为这段会话设置了一个会话变量，这个会话变量保存在内存中，并作为用户是否登录的凭证（会话ID只起到标识一段会话的作用而不是鉴定用户身份），其他页面都只能使用或者注销该会话变量，只有登录页面能设置该变量。

