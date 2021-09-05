# HTML name、id、class 的区别

　　在一个页面中，有许多的控件(元素或标签)。为了更方便的操作这些标签，就需要给这些标签标识一个身份牌。



# 1. name

指定标签的名称。

## 1.1 格式

<input type="text" name="username" />

## 1.2 应用场景

①form表单：name可作为转递给服务器表单列表的变量名；如上面的传到服务器的名称为：username='text的值'。

②input type='radio'单选标签：把几个单选标签的 name设为一个相同值时，将会进行单选操作。

```
<input type="radio" name='sex'/>男
<input type="radio" name='sex'/>女
```

③快速获取一组name相同的标签：获取拥有相同name的标签，一起进行操作，如:更改属性、注册事件等。

```
function changtxtcolor() {
    var txts = document.getElementsByName('txtcolor'); //获取所有name=txtcolor 的标签
    for (var i = 0; i < txts.length; i++) { //循环遍历标签，并把背景色改为red
        txts[i].style.backgroundColor = 'red';
    }
}
```

## 1.3 特性

name属性的值，在当前page页面中并非唯一性。

 

# 2. id

指定标签的唯一标识。

## 2.1 格式

<input type=password id="userpwd" />

## 2.2 应用场景

①根据提供的唯一id号，快速获取标签对象。如：document.getElementById(id)

②用于充当label标签for属性的值：示例：<label for='userid'>用户名：</label>，表示单击此label标签时，id为userid的标签获得焦点。

## **2.3 特性**

id属性的值，在当前的page页面要是唯一的。

 

# 3. class

指定标签的类名。

## **3.1 格式**

<input type=button class="btnsubmit" />

## **3.2 应用场景**

①CSS操作，把一些特定样式放到一个class类中，需要此样式的标签，可以在添加此类。

## **3.3 特性**

可以把多个类，放在一个class属性里，但必须用空格隔开；如：class='btnsubmit btnopen'