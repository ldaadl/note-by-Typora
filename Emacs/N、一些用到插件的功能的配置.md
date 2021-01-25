##  一、美化Emacs

<strong>emacs中自带了插件管理器melpa，函数为package-list-packages（需换源）[^1]，可以直接在里面下载[^2]所要的插件</strong>。此外，emacs自带了很多主题，使用函数load-theme就可以查看它们。

美化Emacs我使用了github上的项目emacs-dashboard[^3]，使用主题doom-one。

[^1]: 将     (add-to-list 'package-archives'  ("elpa" . "http://mirrors.tuna.tsinghua.edu.cn/elpa/gnu/") t) (add-to-list 'package-archives'   ("marmalade" . "http://mirrors.tuna.tsinghua.edu.cn/elpa/marmalade/") t) (add-to-list 'package-archives'  ("melpa" . "http://mirrors.tuna.tsinghua.edu.cn/elpa/melpa/") t) (package-initialize)          添加到init.el中。换源后使用函数package-refresh-contents更包列表
[^2]: 进入melpa后选择下载，或者直接用函数package-install 包名称
[^3]: https://github.com/emacs-dashboard/emacs-dashboard/blob/master/README.org

## 二、拼写检查器（ispell）

在init.el中加上(ispell-minor-mode t)使拼写检查器永久生效，另外加上(flyspell-mode t)使一个辅助模式永久生效。

该模式下的快捷键：

M-$ 手动纠正最近一个拼写错误的单词。

ispell-region 调用某个区域的单词拼写

ispell-buffer 调用从光标到缓冲区结束大的单词拼写

C-M i 自动纠正最近拼写错误的单词

