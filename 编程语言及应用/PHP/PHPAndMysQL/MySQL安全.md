# MySQL安全

1. 从操作系统看：

2. 1. 以root用户运行MySQL不是好的选择，这会给MySQL读写操作系统任意文件的权限；最好为运行MySQL创建专门的用户，并且严格限制该用户可以访问的目录。

1. 密码：

2. 1. 如果需要在脚本文件中保存密码，要确保只有写入密码的用户才能查看该脚本。
   2. 使用专门的脚本文件来保存密码等重要信息，而且最好将该脚本放于文档树之外。
   3. 如果要在web文档树中存放保存有密码的文档，要避免以纯文本的方式存放他们。

3. 用户权限：

4. 1. MySQL除了有一般的对数据库和表的访问、修改权限之外，还有很多系统级的权限。
   2. 注意alter权限的授予，因为alter可以改变表的结构，如果修改了权限表，则会有攻破权限系统的风险。
   3. host表使用IP而不是域名

