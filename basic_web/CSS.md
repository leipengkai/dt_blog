CSS(层叠样式表 (Cascading Style Sheets)) :是定义如何显示 HTML 元素(标签里的所有代码==元素),通常存储在 CSS 文件中,多个样式定义可层叠为一.(外部样式).

### 解决内容与表现分离的问题.
HTML 标签原本被设计为用于定义文档内容。通过使用 h1,p,table 这样的标签，HTML 的初衷是表达“这是标题”、“这是段落”、“这是表格”之类的信息。
同时文档布局由浏览器来完成，而不使用任何的格式化标签(应该就是CSS).

由于两种主要的浏览器（Netscape 和 Internet Explorer）不断地将新的 HTML 标签和属性（比如字体标签和颜色属性）添加到 HTML 规范中，创建文档内容清晰地独立于文档表现层的站点变得越来越困难.

### 外部样式表使你有能力同时改变站点中所有页面的布局和外观
由于允许同时控制多重页面的样式和布局，CSS 可以称得上 WEB 设计领域的一个突破。作为网站开发者，你能够为每个 HTML 元素定义样式，并将之应用于你希望的任意多的页面中。
如需进行全局的更新，只需简单地改变样式，然后网站中的所有元素均会自动地更新。

### 当读到一个样式表时，浏览器会根据它来格式化 HTML 文档
当同一个 HTML 元素被不止一个样式定义时，会使用哪个样式呢？

1.内联样式（在 HTML 元素内部）
    
    <p style="color: sienna; margin-left: 20px">
    This is a paragraph
    </p>

2.内部样式表（位于 head 标签内部）使用 style 标签在文档头部定义内部样式表


    <head>
    <style type="text/css">
      hr {color: sienna;}
      p {margin-left: 20px;}
      body {background-image: url("images/back40.gif");}
    </style>
    </head>

3.外部样式表

    # 1.外部样式表:每个页面使用 <link> 标签链接到样式表。<link> 标签在（文档的）头部
    <head>
    <link rel="stylesheet" type="text/css" href="mystyle.css" />
    </head>    
    # 浏览器会从文件 mystyle.css 中读到样式声明，并根据它来格式文档


4.浏览器缺省设置,所有的浏览器均支持CSS.

### CSS语法
选择器通常是您需要改变样式的 HTML 元素。

每条声明由一个属性和一个值组成。

1.基本语法

    h1 {color:red; font-size:14px;}
 这行代码的作用是将 h1 元素内的文字颜色定义为红色，同时将字体大小设置为 14 像素。

2.选择器分组:可以分享相同的声明

    h1,h2,h3,h4,h5,h6 {color: green;}

 所有的标题元素都是绿色的

3.继承

    body {
     font-family: Verdana, sans-serif;
     }
    p  {
     font-family: Times, "Times New Roman", serif;
     }
 站点的 body 元素将使用 Verdana 字体（假如访问者的系统中存在该字体的话）,段落的字体是 Times

通过 CSS 继承，子元素将继承最高级元素（在本例中是 body）所拥有的属性（这些子元素诸如 td(表格单元), ul, ol, ul, li, dl, dt,和 dd）。
不需要另外的规则，所有 body 的子元素都应该显示 Verdana 字体，子元素的子元素也一样。并且在大部分的现代浏览器中，也确实是这样的

4.派生选择器(上下文选择器):通过依据元素在其位置的上下文关系来定义样式，你可以使标记更加简洁

    li strong {
    font-style: italic;
    font-weight: normal;
     }

 列表中的 strong 元素变为斜体字，而不是通常的粗体字
    
    <p><strong>我是粗体字，不是斜体字，因为我不在列表当中，所以这个规则对我不起作用</strong></p>
    <ol>
    <li><strong>我是斜体字。这是因为 strong 元素位于 li 元素内。</strong></li>
    <li>我是正常的字体。</li>
    </ol>
只有 li 元素中的 strong 元素的样式为斜体字，无需为 strong 元素定义特别的 class 或 id，代码更加简洁。

5.id 选择器以 "#" 来定义。

    #red {color:red;}
    #green {color:green;}
 第一个可以定义元素的颜色为红色，第二个定义元素的颜色为绿色.

    <p id="red">这个段落是红色。</p>
    <p id="green">这个段落是绿色。</p>
 在HTML 代码中，id 属性为 red 的 p 元素显示为红色，而 id 属性为 green 的 p 元素显示为绿色.

 id 属性只能在每个 HTML 文档中出现一次

6.类选择器以一个点号显示

    .center {text-align: center}
 所有拥有 center 类的 HTML 元素均为居中

    <h1 class="center">
    This heading will be center-aligned
    </h1>

    <p class="center">
    This paragraph will also be center-aligned.
    </p>
 在HTML 代码中，h1 和 p 元素都有 center 类。这意味着两者都将遵守 ".center" 选择器中的规则

 类名的第一个字符不能使用数字！它无法在 Mozilla 或 Firefox 中起作用。

    td.fancy {
    color: #f60;
    background: #666;
     }
 类名为 fancy 的表格单元将是带有灰色背景的橙色

    <td class="fancy">
 在HTML中


7.[属性选择器](http://www.w3school.com.cn/css/css_syntax_attribute_selector.asp)

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
             "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>
    <head>
    <style type="text/css">
    [title]
    {
    color:red;
    }
    </style>
    </head>

    <body>
    <h1>可以应用样式：</h1>
    <h2 title="">Hello worldyyy</h2>
    <a title="W3School" href="http://w3school.com.cn">W3School</a>
    <a title="" href="http://w3school.com.cn">W3School</a> <!-- 效果和上面的一样-->
    <hr />
    # 例子2
    [title=W3School]
        {
        border:5px solid blue;
        }

    <img title="W3School" src="/i/w3school_logo_white.gif" />
    <br />
    <a title="W3School" href="http://w3school.com.cn">W3School</a>
[CSS测试工具](http://www.w3school.com.cn/tiy/t.asp?f=csse_selector_attribute_form)


###  HTML (Hyper Text Markup Language:超文本标记语言):是用来描述网页的一种标记语言，不是一种编程语言，它有一套标记标签来描述网页.
HTML标记标签==HTML标签:由尖括号包围的关键词,通常是成对出现的 对大小写不敏感
    
    <b> 和 </b>

HTML 元素指的是从开始标签（start tag）到结束标签（end tag）的所有代码
### HTML 文档 = 网页(由 HTML 元素定义的)
Web 浏览器的作用是读取 HTML 文档，并以网页的形式显示出它们。浏览器不会显示 HTML 标签，而是使用标签来解释页面的内容.

    <html> 与 </html> 之间的文本描述网页 是定义了整个 HTML 文档
    <body> 与 </body> 之间的文本是可见的页面内容  是HTML 文档的主体
    <head> 与 </head>
    <h1> 与 </h1> 之间的文本被显示为标题
    <p> 与 </p> 之间的文本被显示为段落
    <a href="http://www.w3school.com.cn" style="text-decoration:none">This is a link</a>  HTML (超)链接是通过 <a> 标签进行定义的。
    <img src="w3school.jpg" width="104" height="142" />  HTML 图像是通过 <img> 标签进行定义的。
    <br></br> 换行 <br /> 
    <hr /> 在 HTML 页面中创建水平线
    <!-- This is a comment  注释--> 
    默认情况下，HTML 会自动地在块级元素前后添加一个额外的空行，比如段落、标题元素,div前后
    <style>定义样式定义。
    <link>定义资源引用。        
    <div>定义文档中的节或区域（块级）。
    <span>定义文文档中的行内的小块或区域。
    
### HTML属性为HTML 元素提供附加信息
HTML 标签可以拥有属性。属性提供了有关 HTML 元素的更多的信息。
    
HTML属性总是以名称/值对的形式出现，比如：name="value",属性和属性值对大小写不敏感.总是在 HTML 元素的开始标签中规定

    属性   值                描述
    class  classname         规定元素的类名（classname）
    id     id               规定 元素的唯一 id
    style style_definition  规定元素的行内样式(inline style）
    title   text            规定元素的额外信息（可在工具提示示中显示）

### HTML输出
对于 HTML，您无法通过在 HTML 代码中添加额外的空格或换行来改变输出的效果。

当显示页面时，浏览器会移除源代码中多余的空格和空行.HTML 代码中的所有连续的空行（换行）也被显示为一个空格

### 什么是响应式 Web 设计？
RWD 指的是响应式 Web 设计（Responsive Web Design）
RWD 能够以可变尺寸传递网页
RWD 对于平板和移动设备是必需的

### HTML脚本:[JavaScript](http://www.w3school.com.cn/js/index.asp) 使 HTML 页面具有更强的动态和交互性
script 元素既可包含脚本语句，也可通过 src 属性指向外部脚本文件。

必需的 type 属性规定脚本的 MIME 类型。

JavaScript 最常用于图片操作、表单验证以及内容动态更新


