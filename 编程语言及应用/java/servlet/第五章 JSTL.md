# 第五章 JSTL

## 一.JSTL概述

### 1.JSTL简介

​	JSTL是一种流行的标签库，它的存在可以使我们用标签完成复杂的Scriptlet才能完成的功能，它在Scriptlet被禁用的情况下弥补了EL在功能上的不足。

### 2.JSTL安装

下载相应的jar包，放于WEB-INF下的lib目录即可。

## 二.使用JSTL

### 1.JSTL的库类

| 类别   | 功能                                   | URI                                    | 前缀 |
| ------ | -------------------------------------- | -------------------------------------- | ---- |
| Core   | 变量支持、流向控制、URL管理、杂项      | http://java.sun.com/jsp/jstl/core      | c    |
| XML    | Core、流向控制、转换                   | http://java.sun.com/jsp/jstl/xml       | x    |
| 118n   | 语言环境、消息格式化、数字和日期格式化 | http://java.sun.com/jsp/jstl/fmt       | fmt  |
| 数据库 | SQL                                    | http://java.sun.com/jsp/jstl/sql       | sql  |
| 功能   | 吉和长度、字符串操作                   | http://java.sun.com/jsp/jstl/functions | fn   |

在JSP页面中使用JSTL库类时，必须使用taglib指令导入：<%@taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>

### 2.通用动作指令

#### out标签

`````jsp
<c:out value="value" escapeXml="true" default=""/>
`````

* 功能：将value中的内容输出到JSP页面。
* 属性：value,必须存在，为输出到JSP的内容，可以为静态字符串或Scriptlet或EL；escapeXm可选l，默认为true，表示是否对输出的HTML特殊符号转义为实体代码；default可选，当value中的结果为null时的默认输出，默认为空字符。

#### set标签

````jsp
<%-- 创建一个名为foo的字符串，作用域为page --%>
<c:set var="foo" value="The wisest fool" scope="page"/>
<%-- 引用一个对象，引用的作用域为page --%>
<c:set var="foo1" value="${requestScope.position}" scope="page"/>
<%-- 为一个对象的属性设置一个值 --%>
<c:set target="${address}" property="city" value="Tokyo"/> 
````



* 功能：创建一个字符串和引用该字符串的一个限域变量；创建一个限于变量，并引用以及存在的某一个限域变量；设置限域对象的属性
* 属性：var,可选，只能为静态字符串，创建新变量的变量名；value，可选，要创建的字符串，或者要引用的限域对象，或者新的属性，可以为字符串、Scriptlet或者EL；scope，可选，新建限域对象的范围，只能为page、request、session、application；target，可选，限域对象，必须是JavaBean示例或者Map，可以为字符串、Scriptlet或者EL；property，可选，要更新的属性名，可以为字符串、Scriptlet或者EL。

#### remove

````jsp
<c:remove var="job" scope="page"/>
````

* 功能：删除限域对象
* 属性：var，可选；scope，可选

### 3.条件式动作指令

#### if标签

基本用法：

``````jsp
<C:if test="${a>0}" var="test" scope="page">
主体内容
</C:if>
``````

* 功能：进行if条件判断，为true则执行 主体内容。
* 属性：test，可选，可以为字符串、Scriptlet或者EL，表示判断条件；var，将判断结果存储到指定限域变量；scope，可选；主题内容，可以为字符串、Scriptlet或者EL，结果将直接输出。

* 注意：if标签无法直接实现if-else或if-else if-else，需要多次使用if标签然后更改测试条件以达成目的。

#### choose、when和otherwise标签

``````jsp
<c:choose>
	<c:when test="${a==1}">
    	主题内容1
    </c:when>
    <c:when test="${a==2}">
    	主题内容2
    </c:when>
    <c:otherwise>
    	主题内容3
    </c:otherwise>
</c:choose>
``````

* 功能：类似于switch case default；如果多个when都为true，则执行第一个，仅当所有when都不为true时才执行otherwise
* 属性：

### 4.iterator动作指令

#### forEach

两种用法：

````````jsp
<c:forEach var="x" begin="1" end="5" step="1">
	<c:out value="${x}"/>
</c:forEach>
````````

等同于：

`````python
for x in range(1,6,1):
    print(x)
`````



`````jsp
<c:forEach var="phone" items="${address.phones}">
	${phone}
</c:forEach>
`````

`````jsp
<c:forEach var="mapItem" items="map">
	${mapItem.key}:${mapItem.value}
</c:forEach>
`````



* 功能：迭代器
* 属性：var，可选，静态字符串，限域变量名；items，可选，可为字符串、Scriptlet或者EL，要迭代对象的集合；varStatus，可选，静态字符串，保存迭代状态的限域变量名；begin，可选，可为字符串、Scriptlet或者EL，索引开始处（包含）；end，可选，可为字符串、Scriptlet或者EL，索引结束处（包含）；step，可选，步长，不能小于等于0，可为字符串、Scriptlet或者EL。varStatus,可选，静态字符串，获取迭代器的状态对象。

#### forTokens

````jsp
<c:forTokens var="item" items="a,b,c" delims=",">
	<c:out value="${item}"/><br/>
</c:forTokens>
````

* 功能：以特定分隔符将字符串分隔迭代
* 属性：var，可选，静态字符串，引用当前迭代项的限域变量名称；items，可为字符串、Scriptlet或者EL，要迭代的字符串；varStatus，静态字符串，保存迭代状态对象；begin；end；step；delims，静态字符串，一组分界符。

