# 批处理

## 一.批处理概述

​	在通过JDBC执行SQL语句时，每执行一次语句就需要建立一次TCP连接，这样的开销是比较大的，当我们有多条SQL语句需要执行时，可以使用批处理，将这些语句一次传输。

## 二.操作步骤

使用`createStatement()`方法创建`Statement`对象。

使用`setAutoCommit()`将自动提交设置为`false`。

使用`addBatch()`方法在创建的`Statement`对象上添加SQL语句到批处理中。

在创建的`Statement`对象上使用`executeBatch()`方法执行所有SQL语句。

最后，使用`commit()`方法提交所有更改。

例子:

``````java
package com.test.JDBC;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class BatchJDBC {
    static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    static final String HOST = "jdbc:mysql://ip/数据库";
    static final String USER = "数据库用户";
    static final String PASS = "登录秘钥";
    public static void main(String[] args) {
        try {
            Class.forName(JDBC_DRIVER);
            Connection conn = DriverManager.getConnection(HOST,USER,PASS);

            conn.setAutoCommit(false);
            Statement stmt = conn.createStatement();

            String sql1 = "insert into users values(999,'aoaoao','aoaoao')";
            stmt.addBatch(sql1);
            String sql2 = "insert into users values(1000,'chf','chf')";
            stmt.addBatch(sql2);

            int[] count = stmt.executeBatch();

            conn.commit();

        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }
}
``````

# 事务回滚

## 操作步骤

* 关闭代码自动提交:conn.setAutoCommit(false)
* 其他部分和常规操作相似
* conn.commit()提交或conn.rollback()回滚

## 创建保存点

`````java
try{
   //Assume a valid connection object conn
   conn.setAutoCommit(false);
   Statement stmt = conn.createStatement();

   //set a Savepoint
   Savepoint savepoint1 = conn.setSavepoint("Savepoint1");
   String SQL = "INSERT INTO Employees " +
                "VALUES (106, 24, 'Curry', 'Stephen')";
   stmt.executeUpdate(SQL);  
   //Submit a malformed SQL statement that breaks
   String SQL = "INSERTED IN Employees " +
                "VALUES (107, 32, 'Kobe', 'Bryant')";
   stmt.executeUpdate(SQL);
   // If there is no error, commit the changes.
   conn.commit();

}catch(SQLException se){
   // If there is any error.
   conn.rollback(savepoint1);
}//原文出自【易百教程】，商业转载请联系作者获得授权，非商业请保留原文链接：https://www.yiibai.com/jdbc/jdbc-transactions.html


`````

**releaseSavepoint(Savepoint savepointName):**  - 删除保存点。要注意，它需要一个`Savepoint`对象作为参数。 该对象通常是由`setSavepoint()`方法生成的保存点。