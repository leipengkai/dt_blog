 ### HTML脚本:[JavaScript](http://www.w3school.com.cn/js/index.asp) 使 HTML 页面具有更强的动态和交互性
 script 元素既可包含脚本语句，也可通过 src 属性指向外部脚本文件。

JavaScript 是因特网上最流行的脚本语言,可插入 HTML 页面的编程代码,插入 HTML 页面后，可由所有的现代浏览器执行.
JavaScript 语句向浏览器发出的命令。语句的作用是告诉浏览器该做什么,浏览器会按照编写顺序来执行每条语句.

当网页被加载时，浏览器会创建页面的文档对象模型（Document Object Model),通过可编程的对象模型，JavaScript 获得了足够的能力来创建动态的 HTML.

JavaScript 能够改变页面中的所有 HTML 元素, HTML 属性,CSS 样式,所有事件做出反应

JavaScript 是脚本语言。浏览器会在读取代码时，逐行地执行脚本代码。而对于传统编程来说，会在执行前对所有代码进行编译。

    <script src="myScript.js"></script>

HTML 中的脚本必须位于 script 与 /script 标签之间。

    <script>
    alert("My First JavaScript");
    </script>

脚本可被放置在 HTML 页面的 body 和 head 部分中,通常的做法是把函数放入 head 部分中，或者放在页面底部。这样就可以把它们安置到同一处位置，不会干扰页面的内容

    <body>
    <script>
    document.write("<h1>This is a heading</h1>");
    document.write("<p>This is a paragraph</p>");
    </script>
    <body>

JavaScript 函数和事件:我们把 JavaScript 代码放入函数中，就可以在事件发生时调用该函数.函数是由事件驱动的或者当它被调用时执行的可重复使用的代码块


js的注释用 //, /* */.区分大小写

在 JavaScript 函数内部声明的变量（使用 var）是局部变量

在函数外声明的变量是全局变量，网页上的所有脚本和函数都能访问它

在 JavaScript 中，对象是数据（变量），拥有属性和方法。
当您像这样声明一个 JavaScript 变量时：
    var txt = "Hello";
您实际上已经创建了一个 JavaScript 字符串对象。字符串对象拥有内建的属性 length。对于上面的字符串来说，length 的值是 5。字符串对象同时拥有若干个内建的方法。

js对象：var person={firstname:"Bill", lastname:"Gates", id:5566}; name=person.lastname;

js数组：var cars=new Array("Audi","BMW","Volvo");
    
    for (var i=0;i<cars.length;i++)
        {
        document.write(cars[i] + "<br>");
        }

js布尔：var x=true

    greeting=(visitor=="PRES")?"Dear President ":"Dear ";

如果变量 visitor 中的值是 "PRES"，则向变量 greeting 赋值 "Dear President "，否则赋值 "Dear"。


js条件:if...else if....else,if ..else..,if () {},

js循环:for (在代码块开始之前执行，执行代码块的条件，代码块被执行之后执行){代码块},while(条件){需要执行的代码},do{代码块}while(条件)


 
 必需的 type 属性规定脚本的 MIME 类型。 
 
 JavaScript 最常用于图片操作、表单验证以及内容动态更新

JavaScript 被数百万计的网页用来改进设计、验证表单、检测浏览器、创建cookies，以及更多的应用。


jQuery
JavaScript 框架（库）:jQuery
JavaScript 高级程序设计（特别是对浏览器差异的复杂处理），通常很困难也很耗时。
为了应对这些调整，许多的 JavaScript (helper) 库应运而生。
这些 JavaScript 库常被称为 JavaScript 框架。
