# 从Web查询数据库

基本步骤：

1. 检查和过滤用户输入的数据
2. 创建和设置数据库连接
3. 查询数据库
4. 读取查询结果
5. 向用户展示搜索结果

这时我们使用的例子：

````php
<!DOCTYPE html>
<html>
<head>
  <title>Book-O-Rama Search Results</title>
</head>
<body>
  <h1>Book-O-Rama Search Results</h1>
  <?php
    // create short variable names
    $searchtype=$_POST['searchtype'];
    $searchterm=trim($_POST['searchterm']);

    if (!$searchtype || !$searchterm) {
       echo '<p>You have not entered search details.<br/>
       Please go back and try again.</p>';
       exit;
    }

    // whitelist the searchtype
    switch ($searchtype) {
      case 'Title':
      case 'Author':
      case 'ISBN':   
        break;
      default: 
        echo '<p>That is not a valid search type. <br/>
        Please go back and try again.</p>';
        exit; 
    }

    $db = new mysqli('localhost', 'bookorama', 'bookorama123', 'books');
    if (mysqli_connect_errno()) {
       echo '<p>Error: Could not connect to database.<br/>
       Please try again later.</p>';
       exit;
    }

    $query = "SELECT ISBN, Author, Title, Price FROM Books WHERE $searchtype = ?";
    $stmt = $db->prepare($query);
    $stmt->bind_param('s', $searchterm);  
    $stmt->execute();
    $stmt->store_result();
  
    $stmt->bind_result($isbn, $author, $title, $price);

    echo "<p>Number of books found: ".$stmt->num_rows."</p>";

    while($stmt->fetch()) {
      echo "<p><strong>Title: ".$title."</strong>";
      echo "<br />Author: ".$author;
      echo "<br />ISBN: ".$isbn;
      echo "<br />Price: \$".number_format($price,2)."</p>";
    }

    $stmt->free_result();
    $db->close();
  ?>
</body>
</html>
````

​	这里的事例中，对于数据库的操作全都是面向对象的，但是PHP也提供了与面向对象功能相当的面

向过程的数据库操作方式，这里不再赘叙。

还有一个插入数据的例子：

`````php
<!DOCTYPE html>
<html>
<head>
  <title>Book-O-Rama Book Entry Results</title>
</head>
<body>
  <h1>Book-O-Rama Book Entry Results</h1>
  <?php

    if (!isset($_POST['ISBN']) || !isset($_POST['Author']) 
         || !isset($_POST['Title']) || !isset($_POST['Price'])) {
       echo "<p>You have not entered all the required details.<br />
             Please go back and try again.</p>";
       exit;
    }

    // create short variable names
    $isbn=$_POST['ISBN'];
    $author=$_POST['Author'];
    $title=$_POST['Title'];
    $price=$_POST['Price'];
    $price = doubleval($price);

    @$db = new mysqli('localhost', 'bookorama', 'bookorama123', 'books');

    if (mysqli_connect_errno()) {
       echo "<p>Error: Could not connect to database.<br/>
             Please try again later.</p>";
       exit;
    }

    $query = "INSERT INTO Books VALUES (?, ?, ?, ?)";
    $stmt = $db->prepare($query);
    $stmt->bind_param('sssd', $isbn, $author, $title, $price);
    $stmt->execute();

    if ($stmt->affected_rows > 0) {
        echo  "<p>Book inserted into the database.</p>";
    } else {
        echo "<p>An error has occurred.<br/>
              The item was not added.</p>";
    }
  
    $db->close();
  ?>
</body>
</html>
`````



## 1.检查并过滤输入数据

​	这个脚本从前端接收了两个参数，searchtype和searchterm,这两searchtype将作为SQL查询语句中的where后的字段名，而searchterm则作为相应的值。

​	searchtype虽然是select标签限定的值，但是也可能被修改，所以此处还是要检查一下，这就是后面switch语句的作用（一种白名单的工作模式）。

​	而searchterm作为用户的输入值，则需要更加各种检查和处理，但是此处只使用了trim()函数和后面的if条件判断，这只能判断它是否为空或空字符，这是因为后面的SQL语句使用了预处理技术，将SQL与巨大的代码与数据分离，searchterm将仅能被视作数据。

## 2.设置连接

````php
@$db=new mysqli(主机IP，用户名，口令，数据库);
// 这创建了一个数据库对象，接下来的数据库操作大多都要通过这个对象
 if (mysqli_connect_errno()) {
       echo '<p>Error: Could not connect to database.<br/>
       Please try again later.</p>';
       exit;
    }
// mysqli_connect_errno()函数用于判断数据库连接是否成功，这很重要，因为接下来的操作都依赖数据库的连接成功；需要特别指出的是，面向对象和面向过程两者对于这个函数是通用的
````

​	还有一个实例中没有的操作，那就是切换数据库：

* $db->select_db(数据库名)

## 3.查询数据

````php
$query="select ISBN, AUthor, Title, Price from Books where $searchtype = ?";
````

​	有的地方还可以看到$query="select ISBN, AUthor, Title, Price from Books where $searchtype = '$searchterm'";这样的写法，但是这样并不是很好，上面的写法是一种预处理技术，可以明确的告诉数据库？所代表的的内容一定是数据，而刚刚的写法则没有这样的功能，需提前对变量做很多处理来避免可能存在的SQL注入攻击。

### 使用预处理

`````php
$query = "SELECT ISBN, Author, Title, Price FROM Books WHERE $searchtype = ?";
// 获得预处理对象
$stmt = $db->prepare($query);
// 将？与要传入的数据变量绑定，多个变量时按顺序传入参数，‘s’代表字符串类型，‘i’表示整数类型，‘b’表示blob类型
$stmt->bind_param('s', $searchterm);
// 执行查询
$stmt->execute();
`````

## 4.读取结果

`````php
// 获取结果集
$stmt->store_result();
// 将结果集的四个字段与四个变量相绑定
$stmt->bind_result($isbn, $author, $title, $price);
// ￥stmt->num_rows是获取结果集后存储在预处理对象中的行数
echo "<p>Number of books found: ".$stmt->num_rows."</p>";
// 每次执行fetch()会将一个数据行的数据返回给绑定的变量
while($stmt->fetch()) {
  echo "<p><strong>Title: ".$title."</strong>";
  echo "<br />Author: ".$author;
  echo "<br />ISBN: ".$isbn;
  echo "<br />Price: \$".number_format($price,2)."</p>";
}
`````

​	PHP还有另一种读取结果的方法，$results=$stmt->get_result();将会直接返回真个结果集，这与Python中的处理类似，此处不再赘叙。

## 5.向用户展示搜索结果

​	向用户展示搜索结果没有太多好说的，但是最后还有一个步骤，那就是断开数据库连接（非强制的，脚本运行结束后会自动断开）：

`````php
// 释放结果集
$stmt->free_result();
// 关闭数据库连接
$db->close();
`````

