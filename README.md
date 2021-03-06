这是一个开源分布式博客，其web框架使用的是tornado(一个基于异步IO的python web框架)。
同时我把它设计成一个可以多进程多主机部署的分布式架构，如果你对异步IO的web框架感兴趣，或者对高并发分布式的架构感兴趣并处于入门阶段，那么很希望你来尝试dt_blog，一定会有所收获。

### 一、为什么写dt_blog
作为一个码农怎么能没有一个属于自己的个人博客呢？即便没人看，作为日记来记录编码生涯也是很有必要。其实开源的blog有很多，比如WordPress、LifeType等等，
但是There are a thousand Hamlets in a thousand people's eyes（一千个读者眼里有一千个哈姆雷特），所以我还是喜欢自己写属于自己的"哈姆雷特"。
既然要做新项目，那不用点新东西就会觉得没有意义。恰逢当时淘宝双11，双11会场的页面都是由node.js支撑，node.js做web项目最大的特点就是异步IO，我js不怎么熟，我就选择了python的异步IO框架tornado。
但是单个tornado实例无法充分利用多核CPU的资源，所以就实现了dt_blog这样一个简单的基于tornado的分布式架构博客。

### 二、dt_blog简介
首先非常感谢开源博客[Blog_mini](https://github.com/xpleaf/Blog_mini)，因为整个dt_blog是基于[Blog_mini](https://github.com/xpleaf/Blog_mini)重构的。

我不太擅长前端，所以基本照搬[Blog_mini](https://github.com/xpleaf/Blog_mini)的页面，但是整个后端逻辑都是重写的，以下是与[Blog_mini](https://github.com/xpleaf/Blog_mini)的主要区别：

1. 改用tornado框架，是个基于异步IO的web server。
2. 分布式架构，可以多进程多主机启动server实例，再通过nginx等代理服务器做负载均衡，实现横向扩展提高并发性能。
3. 提高多数主要页面访问性能。对频繁查询的组件（例如博客标题、菜单、公告、访问统计）进行缓存，
    优化sql查询（多条sql语句合并一次执行、仅查需要的字段，例如搜索博文列表不查博文的具体内容）以提高首页博文等主要页面访问性能
4. 访问统计改为日pv和日uv。
5. 博文编辑器改为markdown编辑器。
6. 引入alembic管理数据库版本。
7. 可使用docker快速部署。

但是，作为一个个人blog，其实并不需要分布式的架构，即便引入了这样的架构，我依然希望其他开发者能够快捷的搭建环境并上手使用，
因此dt_blog只是简单的实现了分布式，并不能保证绝对的高可用，主从需要启动实例时手动指定，存在单点故障的可能，
如果有开发者希望以此架构扩展到大型生产环境请自行配合zookeeper等实现动态选主+完整的日志分析、性能监控以及完善报警机制来保证高可用。

**注：** dt_blog目前架构并不需要考虑线程安全问题，因为tornado是单线程的，
    仅用到多线程的地方只有通过线程池访问数据库，数据库连接session是线程局部变量，其他并无线程间共享的变量，不会带来线程安全问题。

### 三、dt_blog部署与开发环境搭建
#### 1. 构建运行环境
###### 需要安装以下组件：

1. python2.7(python3 没试过，不知道行不行)
2. mysql(或者其他sqlalchemy支持的数据库)
3. redis

###### clone项目，安装依赖：

	git clone https://github.com/leipengkai/bt_blog.git
	#项目依赖（如果用的不是mysql可以将MySQL-python替换使用的数据库成所对应的依赖包）
	pip install -r requirements.txt
###### 创建数据库(注意使用utf-8编码)
    CREATE DATABASE `dt_blog` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    grant all privileges on dt_blog.* to root@localhost identified by '' with grant option;
###### 启动redis
###### 修改config.py，配置数据库、redis、日志等
###### 创建数据库或更新表
	python main.py upgradedb
###### 启动server
	python main.py --master=true --port=8888

###### 初始化管理员账户
访问http://[host]:[port]/super/init注册管理员账号。

注:仅没有任何管理员时才可以访问到该页面。

### 四、开发注意事项
dt_blog是个异步IO的架构，相对于常见的同步IO框架，需要注意以下几点：

- IO密集型的操作请务必使用异步的client，否则无法利用到异步的优势
- 由于多数异步IO的框架都是单线程的，所以对于CPU密集型的操作最好交由外部系统处理，防止阻塞，大型项目可以配合消息队列使用更佳
- 如果必须用同步的IO组件，可以配合线程池使用（dt_blog中使用了sqlalchemy就是配合线程池使用的）
- 如果你是ORM+线程池使用(dt_blog中就是sqlalchemy+线程池)，一般的ORM都有lazy load的机制，在异步框架中请勿使用，因为lazy load的执行在主线程中，很可能会阻塞主线程，影响别的请求。

dt_blog是分布式的架构，相对于单进程的项目一般需要注意以下几点：

- 多实例间的日志冲突。
- 多实例间的缓存同步。
- 多实例间的session同步。
- 多实例间主从关系，例如一些定时任务可能主需要集群中一个节点处理。

当然以上几点都可以从dt_blog的源代码中找到至少一种解决方案。

如果你对异步IO的web框架、分布式的架构感兴趣，或者想对dt_blog做二次开发，那么你可以阅读以下dt_blog的其他相关博文，并配合源代码学习，一定会很快掌握。

1. [学习于此](https://github.com/xtg20121013/blog_xtg)

####### 一些基本教程
[tornado介绍](http://tornado.moelove.info/zh/latest/guide/intro.html)
[sqlalchemy数据库](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html)
[Alembic介绍](http://huangx.in/18/alembic-simple-tutorial)
[redis订阅/发布](https://www.jianshu.com/p/d0911a195968)