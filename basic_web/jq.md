jQuery
JavaScript 框架（库）:jQuery
JavaScript 高级程序设计（特别是对浏览器差异的复杂处理），通常很困难也很耗时。
为了应对这些调整，许多的 JavaScript (helper) 库应运而生。
这些 JavaScript 库常被称为 JavaScript 框架。

jQuery使用 CSS 选择器来访问和操作网页上的 HTML 元素（DOM 对象）,极大地简化了 JavaScript 编程.
jQuery 是一个 JavaScript 函数库。
jQuery 库包含以下特性：
     
     HTML 元素选取
     HTML 元素操作
     CSS 操作 
     HTML 事件函数
     JavaScript 特效和动画
     HTML DOM 遍历和修改
     AJAX

### jQuery 语法
基础语法是：$(selector).action()
    美元符号定义 jQuery对象
    选择符（selector）“查询”和“查找” HTML 元素
    jQuery 的 action() 执行对元素的操作

#### jQuery 元素选择器
$(this).hide() 隐藏当前的 HTML 元素

$("#test").hide() 隐藏 id="test" 的元素。

$("p").hide() 隐藏所有 p 元素。

$(".test").hide() 隐藏所有 class="test" 的元素。

$("p.intro") 选取所有 class="intro" 的 p 元素。

$("p#demo") 选取所有 id="demo" 的 p 元素。

$("ul li:first")每个 ul 的第一个 li 元素    

$(":input")所有 input 元素    

$(":text")所有 type="text" 的 input 元素  



#### jQuery 属性选择器
$("[href]") 选取所有带有 href 属性的元素。

$("[href='#']") 选取所有带有 href 值等于 "#" 的元素。

$("[href!='#']") 选取所有带有 href 值不等于 "#" 的元素。

$("[href$='.jpg']") 选取所有 href 值以 ".jpg" 结尾的元素

### jQuery 事件函数是 jQuery 中的核心函数
#### 文档就绪函数
jQuery 函数位于一个 document ready 函数中：

    $(document).ready(function(){

        把所有事件处理函数置于文档就绪事件处理器中
        把 jQuery 代码置于单独的 .js 文件中
        这是为了防止文档在完全加载（就绪）之前运行 jQuery 代码)

    });

$(document).ready(function)将函数绑定到文档的就绪   事件（当文档完成加载时）

$(selector).click(function)触发 或将函数绑定到被选元素的点击事件

$(selector).dblclick(function)触发或将函数绑定到被选元素的双击事件

$(selector).focus(function)触发或将函数绑定到被选元素的获得焦点事件

$(selector).mouseover(function)触发或将函数绑定到选元素的鼠标悬停事件

### AJAX 是与服务器交换数据的艺术，它在不重载全部页面的情况下，实现了对部分网页的更新
AJAX = 异步 JavaScript 和 XML（Asynchronous JavaScript and XML）。

简短地说，在不重载整个网页的情况下，AJAX 通过后台加载数据，并在网页上进行显示

#### jQuery load() 方法
jQuery load() 方法是简单但强大的 AJAX 方法。
load() 方法从服务器加载数据，并把返回的数据放入被选元素中

    $(selector).load(URL,data,callback);
    必需的 URL 参数规定您希望加载的 URL。
    可选的 data 参数规定与请求一同发送的查询字符串键/值对集合。
    可选的 callback 参数是 load() 方法完成后所执行的函数名称
    
    callback:function(responseTxt,statusTxt,xhr)
    responseTxt - 包含调用成功时的结果内容
    statusTXT - 包含调用的状态
    xhr - 包含 XMLHttpRequest 对象

#### jQuery get() 和 post() 方法用于通过 HTTP GET 或 POST 请求从服务器请求数据
GET 基本上用于从服务器获得（取回）数据。注释：GET 方法可能返回缓存数据。
POST 也可用于从服务器获取数据(主要是发送数据)。不过，POST 方法不会缓存数据，并且常用于连同请求一起发送数据

<li class="level1">
<span class="index">11</span>
<span class="text"><a href="#11">标准库</a></span>
</li>

