# 第四章 EL

​	使用El后而完全不使用JSP脚本元素，这将使JSP更靠近模板引擎。

## 一.语法

* ${expression}

* ${expression1}${expression2}，将视作两个字符串拼接

* ${expression}可以作为<u>JSP</u>中某个标签的属性

  ```````jsp
  <my:tag someAttribute="${expression}"/>
  ```````

  这里的${expression}被视作EL而不是字符串，要发送字符串需要对$进行转义

### 1.保留字

and 	eq	gt	true	instanceof	

or	ne	le	flase	empty

not	It	ge	null	div	mod

### 2.[]和.运算符

​	这两个运算符是访问对象的property的运算符，作用类似。

​	如果某些对象的名称不是Java中的合法标识符，那么只能使用[]访问而不能使用.访问，例如：

${accept-language["zh-CN"]}

### 3.运算规则

${expr-1[expr-2]}

1. 计算expr-1，得到value-1
2. 若value-1为null则返回
3. 运算expr-2，得到value-2
4. 若value-2为null，返回
5. 若
   1. value-1为map，get(value-2)，返回相应值或null
   2. value-1为list，强转value-2后，抛出异常或get(value-2),返回相应值或抛出异常
   3. value-1为JavaBean，value-1.getValue-2()

## 二.EL隐式对象

​	JSP中的隐式对象只有JSP脚本元素才能访问，在无脚本的JSP页面中，可以通过EL自身提供的一组对象访问。

| 对象             | 描述                                                         |
| ---------------- | ------------------------------------------------------------ |
| pageContext      |                                                              |
| initParam        | 包含所有context初始化参数，以参数名为key组成Map              |
| param            | 包含所有请求参数并以参数名为key组成Map，多个同名参数只能获取第一个值 |
| paramValues      | 包含所有请求参数并以参数名为key组成Map，value是一个字符串数组，可以处理多个同名参数 |
| header           | 包含所有请求标头，并以标头名称作为key组成Map，多个相同标头只能获取第一个值 |
| headerValues     | 类似paramValues                                              |
| cookie           | 包含所有cookie，cookie名为key，value映射到一个cookie对象     |
| applicationScope | 包含ServletContext对象中所有属性并以属性名作为key的Map       |
| sessionScope     | 包含HttpSession对象中所有属性并以属性名作为键的Map           |
| requestScope     |                                                              |
| pageScope        |                                                              |

### 1.pageContext

​	pageContext表示当前JSP页面的javax.servlet.jsp.PageContext。它包含所有其他JSP隐式对象：

| 对象        | 类型                    |
| ----------- | ----------------------- |
| request     | 当前HttpServletRequest  |
| response    | 当前HttpServiceResponse |
| out         | JspWriter               |
| session     | HttpSession             |
| application | ServletContext          |
| config      | ServletConfig           |
| pageContext | PageContext             |
| page        | HttpJspPage             |
| exception   | Throwable               |

​	获取一个EL隐式对象的方式很简单，${pageContext\["request"\]\["method"\]}。需要说明的是PageContext和HttpJspPage的区别，Pagecontext已经说过，它代表本次请求的JSP页面的context，而Page则代表当前Page的servlet实例，使用较少。

### 2.paramValues

可以获取多个同名参数的值，也可以获取指定的某一个${paramValues.selectedOptions[0]}。

### 3.四个Scope

​	对应四大域对象，这个没什么好说的，但是有一个用法要指出：

​	${today}，EL隐式对象中没有这个对象，这代表某个context中的一个property，至于是哪个context，EL会自动从最大范围的ServletContext到最小范围的PageContext。

## 三.EL的其他运算符

### 1.算术运算符

\+ \- \* / div % mod

### 2.关系运算符

* == eq
* != ne
* \> gt
* \>= ge
* < It
* <= le

### 3.逻辑运算符

* AND && and
* OR || or
* NOT ! not

### 4.条件运算

* ？：

### 5.empty运算符

* ${empty X}

## 四.结合使用JSP和Servlet构建符合规范的应用

### 1.两个JavaBean，为Model

`````java
public class Address {
    private String streetName;
    private String streetNumber;
    private String city;
    private String state;
    private String zipCode;
    private String country;

    public void setStreetName(String streetName) {
        this.streetName = streetName;
    }

    public void setStreetNumber(String streetNumber) {
        this.streetNumber = streetNumber;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public void setState(String state) {
        this.state = state;
    }

    public void setZipCode(String zipCode) {
        this.zipCode = zipCode;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getStreetName() {
        return streetName;
    }

    public String getStreetNumber() {
        return streetNumber;
    }

    public String getCity() {
        return city;
    }

    public String getState() {
        return state;
    }

    public String getZipCode() {
        return zipCode;
    }

    public String getCountry() {
        return country;
    }
}

`````

``````java
public class Employee {
    private int id;
    private String name;
    private Address address;

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Address getAddress() {
        return address;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setAddress(Address address) {
        this.address = address;
    }
}
``````

### 2.一个servlet作为Control

`````java
@WebServlet(urlPatterns = {"/employee"})
public class EployeeServlet extends HttpServlet implements Serializable {
    private static final long serialVersionUID = 1L;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Address address = new Address();
        address.setStreetName("302号");
        address.setCity("武汉");
        address.setState("徐家棚街道");
        address.setZipCode("图书馆9楼");
        address.setCountry("中国");

        Employee employee = new Employee();
        employee.setId(165);
        employee.setName("lideao");
        employee.setAddress(address);

        req.setAttribute("employee",employee);
        Map<String,String> capitals = new HashMap<String,String>();
        capitals.put("China","Beijing");
        capitals.put("Asutralia","Canberra");
        capitals.put("Canada","Ottawa");

        req.setAttribute("capitals",capitals);

        // 请求转发
        RequestDispatcher rd = req.getRequestDispatcher("/JSP/employee.jsp");
        rd.forward(req,resp);
    }
}
`````

### 3.一个jsp作为View

`````jsp
<%--
  Created by IntelliJ IDEA.
  User: Administrator
  Date: 2021/12/27
  Time: 12:29
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Employee</title>
</head>
<body>
<ul>
    <li>session id:${pageContext.session.id}</li>
    <li>employee:${requestScope.employee.name},${employee.address.city}</li>
    <li>capitals:${capitals.Canada}</li>
</ul>
</body>
</html>

`````

### 4.总结

​	上面三部分组成的应用就是一个标准的MVC模式，两个JavaBean作为数据的载体，为Model，在实际项目中往往要结合数据库编写；；servlet处理请求，是Control，组织model之间的通信，作为view和model之间的桥梁；jsp作为View层，使用model的数据来展示。

​	有一点需要注意，按照业务逻辑来说，JSP页面需要通过一个servlet来间接请求，所以应该有一些方式阻止JSP页面被直接请求，这在之后可以通过过滤器等实现。

## 五.在JSP2.0和更高版本中配置EL

### 1.禁用JSP

``````xml
<jsp-config>
	<jsp-property-group>
    	<url-pattern>*.jsp</url-pattern>
        <scripting-invalid>true</scripting-invalid>
    </jsp-property-group>
</jsp-config>
``````

### 2.关闭EL

* 使用<%@page isELTgnored="true"%>
* 在部署描述符中设置

`````xml
<jsp-config>
	<jsp-property-group>
    	<url-pattern>*.jsp</url-pattern>
        <el-ignored>true</el-ignored>
    </jsp-property-group>
</jsp-config>
`````

注意：

* 低于JSP2.0版本默认关闭EL
* 上述两种方法中任意存在一种，EL都会关闭
