# PHP的其他有用特性

### eval()函数

### 中止执行

exit()和die()

`````php
易出错操作 or die();
`````

### 序列化

* serialize(变量)，返回字符串
* unserialized(序列化对象)

使用unserialized之前，必须引入相应的类定义

会话控制可以代替序列化

### 找到已载入的扩展

get_loaded_extensions()将返回当前PHP可用的函数集数组,get_extension_funcs()根据给定的函数集返回可用函数

``````php
<?php
echo 'Function sets supported in this install are: <br />';
$extensions = get_loaded_extensions();
foreach ($extensions as $each_ext)
{
  echo $each_ext.'<br />';
  echo '<ul>';
  $ext_funcs = get_extension_funcs($each_ext);
  foreach($ext_funcs as $func)
  {
    echo '<li>'.$func.'</li>';
  }
  echo '</ul>';
}
?>
``````

### 识别脚本属主

`````php
echo get_current_user();
echo `id -a`;
`````

### 获取脚本被修改的时间

`````php
echo date('g:i a,j M Y',getlastmod());
// getlastmod()返回的是时间戳
`````

### 临时修改运行环境

``````php
<?php
$old_max_execution_time = ini_set('max_execution_time', 120);
echo 'old timeout is '.$old_max_execution_time.'<br />';

$max_execution_time = ini_get('max_execution_time');
echo 'new timeout is '.$max_execution_time.'<br />';
?>
``````

函数ini_set(设置选项名,值)，设置选项

函数ini_get(设置选项名)，获取设置的值



并非所有选项都可以使用ini_set函数设置，php配置文件中的所有选项都有设置级别：

PHP_INI_USER 可以用Ini_set设置

PHP_INI_PERDIR  可以在php.ini  .htaccess  httpd.conf中设置

PHP_INI_SYSTEM  可以在php.ini和httpd.conf中设置

PHP_INI_ALL  可以使用以上任何一种方法进行设置

### 显示源代码

show_source()或者highlight_file()，传入参数为.php文件

### 在命令行上使用PHP

php 脚本文件

echo '<?php php语句; ?>' | php

php -r 'php语句;'