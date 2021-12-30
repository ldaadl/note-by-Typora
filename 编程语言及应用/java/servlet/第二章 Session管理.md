# 第二章 Session管理

Session管理就是常说的会话管理

## 一.网址重写

​	将一个或多个token作为一个查询字符串添加到一个URL中。token的格式一般是键值对:

​	url?key1=value1&key2=value2&key3=value3

适用于：

* token不必在过多的URL中携带

缺点：

* web浏览器的URL长度有限制，token不能过长
* 在静态资源的URL尾部添加token比较麻烦
* 许多字符需要编码
* 明文存在
* 传递的信息难以跨越多个界面

`````java
@WebServlet(name = "TopTouristCityServlet", value = "/Top10")
public class TopTouristCityServlet extends HttpServlet {
    private static final long serialVersionUID = 123456789L;

    private List<String> londonAttraction = new ArrayList();
    private List<String> parisAttraction = new ArrayList();

    @Override
    public void init() throws ServletException {
        int a = 1;
        for(int i=0;i<5;i++) {
            londonAttraction.add("" + a++);
        }
        for(int i=0;i<5;i++) {
            parisAttraction.add("" + a++);
        }
    }
    private void showMain(HttpServletRequest request,HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        writer.print("<a href=\"?page=former\">上半夜</a>\n" +
                "<a href=\"?page=next\">下半夜</a>");
    }
    private void showPage(HttpServletRequest request,HttpServletResponse response, int page) throws IOException {
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        if (page == 1){
            for (String num:londonAttraction){
                writer.println(num+"<br>");
            }
        }else {
            for (String num:parisAttraction){
                writer.println(num+"<br>");
            }
        }
    }
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String tokenValue = request.getParameter("page");
        if (tokenValue==null)
            showMain(request,response);
        else if(tokenValue.equals("former"))
            showPage(request,response,1);
        else if(tokenValue.equals("next"))
            showPage(request,response,2);
        else
            showMain(request,response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

    }
}
`````



## 二.隐藏域

​	将与网址重写类似，但不是将值添加到URL后面，而是将它们放在HTML表单的隐藏域中。

适用于：

* 页面包含表单

优点：

* 传递的token长度更长；无需进行字符编码

缺点：

* 传递的信息难以跨越多个界面

``````java
@WebServlet(name = "CustomerServlet",urlPatterns={"/customer","/editCustomer","/updateCustomer"})
public class CustomerServlet extends HttpServlet {
    private static final long serialVersionUID = -20L;

    private List<Customer> customers = new ArrayList<Customer>();

    @Override
    public void init() throws ServletException {
        Customer customer1 = new Customer();
        customer1.setId(1);
        customer1.setName("lideao");
        customer1.setCity("wuhan");
        customers.add(customer1);

        Customer customer2 = new Customer();
        customer2.setId(2);
        customer2.setName("chf");
        customer2.setCity("tm");
        customers.add(customer2);
    }

    private void sendCustomerList(HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        writer.println("<ul>");
        for(Customer c:customers){
            writer.printf("<li>id %d,name %s, city %s<a href=\"editCustomer?id=%d\">edit</a></li>\n",c.getId(),c.getName(),c.getCity(),c.getId());
        }
        writer.println("</ul>");
    }

    private Customer getCustomer(int customerId){
        for(Customer c:customers){
            if(c.getId()==customerId)
                return c;
        }
        return null;
    }

    private void sendCustomerForm(HttpServletRequest request,HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        int customerId=0;
        customerId=Integer.parseInt(request.getParameter("id"));
        Customer customer= getCustomer(customerId);
        if(customer!=null){
            writer.printf("<form method='POST' action=\"updateCustomer\">\n" +
                    "  <input type=\"hidden\" name=\"id\" value=\"%d\"/>\n" +
                    "  <label>name:</label><br>\n" +
                    "  <input type=\"text\" name=\"name\"/><br>\n" +
                    "  <label>city:</label><br>\n" +
                    "  <input type=\"text\" name=\"city\"/><br>\n" +
                    "<input type=\"submit\">" +
                    "</form>\n",customerId);
        }else
            writer.println("No customer found!");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String url=req.getRequestURI();
        if(url.endsWith("/customer"))
            sendCustomerList(resp);
        else if(url.endsWith("/editCustomer"))
            sendCustomerForm(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int customerId=0;
        customerId=Integer.parseInt(req.getParameter("id"));
        Customer customer= getCustomer(customerId);
        String newName = req.getParameter("name");
        String newCity = req.getParameter("city");
        if(customer!=null){
            if(newName!=null)
                customer.setName(newName);
            if(newCity!=null)
                customer.setCity(newCity);
        }
        // 这样不好，应该使用P/R/G模式
        // sendCustomerList(resp);
        resp.sendRedirect("/demo1_war_exploded/customer");
    }

    class Customer{
        private int id;
        private String name;
        private String city;
        public int getId(){
            return id;
        }
        public void setId(int id){
            this.id = id;
        }
        public String getName(){
            return name;
        }
        public void setName(String name){
            this.name = name;
        }

        public String getCity() {
            return city;
        }
        public void setCity(String city){
            this.city = city;
        }
    }
}
``````

## 三.Cookie

创建cookie：

````java
// 创建一个cookie对象
Cookie cookie = new Cookie(name,value);
// 设置cookie属性
// 首部添加cookie
httpServletResponse.addCookie(cookie);
````

浏览器再次发送对同一资源或者同一服务器的不同资源的请求时，它会同事把从Web浏览器收到的cookie再传回去。

获取一个名为maxRecords的cookie：

```java
Cookies[] cookies = request.getCookies();
Cookie maxrecordCookie = null;
if(cookies!=null){
    for(Cookie cookie:cookies){
        if(cookie.getName().equals("maxRecords")){
        maxRecordsCookie=cookie;
        break; 
        }
    }
}
```

注意：

* 没有通过cookie名直接获取cookie的方法
* 无法直接删除cookie，只能覆盖cookie，即创建一个新的cookie，将其maxAge设为0

删除cookie

```java
Cookie cookie = new Cookie("userName","");
cookie.setMaxAge(0);
response.addCookie(cookie);
```

这里说一下cookie的domain和path属性：正常的Cookie只能在一个应用中访问，即cookie只能由创建他的应用访问。要实现跨应用访问cookie或者跨域访问cookie就得使用到cookie的setPath()和setDomain()方法。

`````java
package com.demo1;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.io.PrintWriter;

@WebServlet(name="LogServlet",urlPatterns={"/log"})
public class LogServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html");
        PrintWriter writer = resp.getWriter();
        writer.print("<form method=\"post\">\n" +
                "  <label>username:</label><br>\n" +
                "  <input type=\"text\" name=\"username\" value=\"\"/><br>\n" +
                "  <label>password:</label><br>\n" +
                "  <input type=\"text\" name=\"password\"/><br>\n" +
                "  <label>name:</label><br>\n" +
                "  <input type=\"text\" name=\"name\"/><br>\n" +
                "  <input type=\"submit\">\n" +
                "</form>\n");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        String name = req.getParameter("name");
        Cookie cookie1 = new Cookie("username",username);
        Cookie cookie2 = new Cookie("password",password);
        Cookie cookie3 = new Cookie("name",name);

        cookie2.setComment("password");
        cookie2.setMaxAge(100);

        resp.addCookie(cookie1);
        resp.addCookie(cookie2);
        resp.addCookie(cookie3);
        resp.sendRedirect("/demo1_war_exploded/log");
    }
}
`````



### 之前的一些关于cookie的问题

* cookie不一定保存在服务器中，创建session后才会保存在服务器中
* cookie的属性存储在哪：浏览器一定有，服务器中创建session后有。比如，maxAge这个属性决定了cookie的存活时间，时间到期后，浏览器中的该cookie将被删除。所以前面说cookie无法直接删除，因为在服务器端我们无法控制浏览器的行为，我们只能创建一个存活时间为0的新cookie，将浏览器中的原cookie覆盖，然后使浏览器删除它
* 只依靠cookie不依靠session如何实现登录：cookie中携带的就是账户和密码（或者做一定转换）等信息

## 四.HttpSession对象

​	HttpSession是当一个用户第一次访问网站时自动创建的，通过HttpServletRequest.getSession()方法，可以获取用户的HttpSession。

* HttpSession getSession() 返回当前HttpSession，如果没有，则创建一个并返回
* HttpSession getSession(true) 同上
* HttpSession getSession(false) 没有则不创建

* void setAttribute(String name,Object value) 将一个值放于HttpSession中，这个对象是保存在内存中的，当内存快满时，可以将对象放入辅存，但还是建议尽量存放小内存对象。新加入的同name Object将会覆盖之前的Object。
* void Object getAttribute(String name) 获取对象
* Enumeration\<String\> getAttributeNames() 获取的对象保存着所有的属性名，可以通过其得到HttpSession中的所有属性

​		HttpSession中保存的内容不会发往客户端，它会生成一个JSESSIONID的cookie或者在url参数中添加jesssionid作为标识一个HttpSession的凭证

* String getId()获取HttpSession标识符

​	Session在默认情况下，是在用户持续一段时间没访问后过期，可以在部署描述符中通过session-timeout设置具体的时间，没有设置的话将由Servlet容器决定。

* void invalidate() 强制销毁session
* int getMaxInactiveInterval() 获取用户离开最后一次访问的秒数
* void setMaxInactiveInterval(int seconds) 设置session期限，注意，second为0表示永不过期，而不是立刻过期 

````java
@WebServlet(name="ShopServlet",urlPatterns={"/products","/viewProductDetails","/addToCart","/viewCart"})
public class ShopServlet extends HttpServlet {
    private static final long serialVersionUID = -20L;
    private static final String CART_ATTRIBUTE = "cart";

    private List<Product> products = new ArrayList<Product>();
    private NumberFormat currentFormat = NumberFormat.getCurrencyInstance(Locale.CHINA);

    class Product{
        public int id;
        public String name;
        public String desc;
        public float price;

        public Product(int id,String name,String desc,float price) {
            this.id=id;
            this.name=name;
            this.desc=desc;
            this.price=price;
        }
    }
    class ShoppingItem{
        public Product product;
        public int quantify;

        public ShoppingItem(Product product,int quantify){
            this.product=product;
            this.quantify=quantify;
        }
    }

    @Override
    public void init() throws ServletException {
        products.add(new Product(1,"TV","watch TV",1000F));
        products.add(new Product(2,"Computer","play computer games",5000F));
    }

    private void showProducts(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        writer.println("<ul>");
        for(Product p:products){
            writer.printf("<li>name %s,desc %s,price %f,<a href='viewProductDetails?id=%d'>details</a></li><br>",p.name,p.desc,p.price,p.id);
        }
        writer.println("</ul><br>");
        writer.println("<a href=\"viewCart\">Cart</a>");
    }

    private void details(HttpServletRequest request, HttpServletResponse response) throws IOException {
        int id = 0;
        id = Integer.parseInt(request.getParameter("id"));
        Product p = getProduct(id);
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        if(p!=null){
            writer.printf("<form method=\"post\" action=\"addToCart\">\n" +
                    "<input type=\"hidden\" name=\"id\" value=\"%d\"/>" +
                    "  <label>Product name:%s</label><br>\n" +
                    "  <label>product description:%s</label><br>\n" +
                    "  <label>product price:%f</label><br>\n" +
                    "  <input type=\"text\" name=\"quantify\"/><br>\n" +
                    "  <input type=\"submit\" value=\"buy\">\n" +
                    "</form>\n" +
                    "<a href=\"products\">back products list</a>",p.id,p.name,p.desc,p.price);
        }else
            writer.println("No such product!");
    }

    private Product getProduct(int id){
        for(Product p:products){
            if(p.id==id)
                return p;
        }
        return null;
    }

    private void viewCart(HttpServletRequest request,HttpServletResponse response) throws IOException {
        HttpSession session=request.getSession();
        List<ShoppingItem> cart = (List<ShoppingItem>) session.getAttribute(CART_ATTRIBUTE);
        response.setContentType("text/html");
        PrintWriter writer = response.getWriter();
        if(cart!=null){
            writer.println("<ul>");
            for (ShoppingItem s:cart){
                writer.printf("<li>product:%s,quantify:%d,sum %f</li><br>",s.product.name,s.quantify,s.product.price*s.quantify);
            }
            writer.println("</ul>");
        }else{
            writer.print("Cart is empty!");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        int id = 0;
        int quantify = 0;
        resp.setContentType("text/html");
        PrintWriter writer = resp.getWriter();
        try {
            id = Integer.parseInt(req.getParameter("id"));
            quantify = Integer.parseInt(req.getParameter("quantify"));
        }catch(Exception e){
            writer.println("id or quantify error!");
            return;
        }
        Product product = getProduct(id);
        if(product!=null&&quantify>=0){
            ShoppingItem shoppingItem = new ShoppingItem(product,quantify);
            HttpSession session = req.getSession();
            List<ShoppingItem> cart = (List<ShoppingItem>) session.getAttribute(CART_ATTRIBUTE);
            if(cart==null){
                cart= new ArrayList<ShoppingItem>();
                session.setAttribute(CART_ATTRIBUTE,cart);
            }
            cart.add(shoppingItem);
            resp.sendRedirect("viewProductDetails?id="+id);
        }else
            writer.print("id or quantify error!");
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String uri = req.getRequestURI();
        if(uri.endsWith("/products"))
            showProducts(req,resp);
        else if(uri.endsWith("/viewProductDetails"))
            details(req,resp);
        else if(uri.endsWith("viewCart"))
            viewCart(req,resp);
    }
}
````

