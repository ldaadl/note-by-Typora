# 基本语法

`````mysql
-- 简单case表达式
-- 这里的sex可以是一个字段，可也以s
case sex
	when '1' then '男'
	when '2' then '女'
else '其他' end
-- 搜索case表达式
case 
	when sex='1' then '男'
	when sex='2' then '女'
else '其他' end
`````

* case表达式如其名，只是一个表达式
* 不能忽略结尾的end
* 当遇到when后的条件为真时，后续的判断就会终止
* 各分支的返回类型必须相同

