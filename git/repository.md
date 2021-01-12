repository

star

fork

pull request

watch

issue



github主页

repository主页

个人主页



一个git库对应一个开源项目，我们通过git管理该项目



git：

working directory -》暂存区-》git repository

git status 查看文件状态 

git add 文件名 添加到暂存区

git commit -m “提交描述”

一般流程：git status,git add,git status,git commit -m,git status



初始化操作：

设置用户名：git config --global user.name "用户名"

设置用户邮箱：git config --global user.email "邮箱"

初始化一个新的Git仓库：

在本地新建一个文件夹

在文件内初始化git（把文件夹变为一个git仓库） cd 文件夹-》git init

向仓库中添加文件：

修改仓库：

修改本地的文件之后，不会自动同步，还需自己再次上传，步骤同添加文件

删除仓库中文件：

删除本地文件

git rm 文件名 删除仓库文件

git commit -m “提交描述”



git管理远程仓库：

目的：备份，实现代码集中化管理

git push命令将本地的仓库同步到远程仓库

但是我们需要先将远程仓库fork到本地，在进行修改提交：

git clone 仓库地址







github pages搭建网站：

创建个人站点-》新建仓库（仓库名称必须是用户名.github.io-》在该仓库下新建index.html即可

* 仅支持静态网页
* 仓库里只能是html文件

可以为每个仓库搭建一个站点：

项目主页：settings-》launch automatic page generator-》新建站点基础信息设置-》选择住他-》生成网页

生成站点后的网页文件全部在自动生成的另一个分支里。