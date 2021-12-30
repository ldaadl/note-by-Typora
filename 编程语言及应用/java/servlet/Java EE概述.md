# Java EE概述

* Java SE是基础库，由SUN公司开发，Oracle维护
* Java EE是SUN公司提供的一个庞大的类库，方便程序员在此基础上进行企业级开发

* Java EE规范是一个比较大的规范，包括13个子规范

  * Servlet3.0
  * JDBC
  * 。。。

  Tomcat服务器，不同的版本实现了不同的servlet规范，Tomcat7实现了Tomcat3.0规范



* Java EE技术不止servlet和JSP，一共有13个规范，Tomcat只是Servlet/JSP容器，Tomcat只实现了servlet和JSP的标准，表现在我们安装Tomcat之后关于servlet和JSP的内容无需额外导包，而像JDBC之类的还需要导包，而不是Java EE容器或者HTTP服务器

* Web服务器和Web容器：Tomcat=Web服务器+Servlet/JSP容器。Web服务器专注于响应HTTP请求，它的工作重心在于响应静态资源，而Web容器可以看做是根据一定的标准产生的框架，它规定了如何对HTTP请求的<u>内容</u>进行响应，重心在于根据动态资源产生静态资源；Web容器也是Web应用程序和Web服务器之间的接口，可以让Web应用程序无需考虑Web服务器的实现细节。
