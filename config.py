# coding=utf-8

cookie_keys = dict(
    session_key_name="TR_SESSION_ID",# cookie_name:
    # TR_SESSION_ID:session_id(uuid)
    # session_id:(session)以json的形式 保存着session_keys的信息
    uv_key_name="uv_tag", # cookie_name
    # uv_tag:datetime.date.today().day
)

# session相关配置（redis实现）
redis_session_config = dict(
    db_no=0,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
    session_key_name=cookie_keys['session_key_name'],
    session_expires_days=7,
)

session_keys = dict(
    login_user="login_user",
    messages="messages",# TR_SESSION_ID:{u'messages': [{u'category': u'success', u'message': u'\u521b\u5efa\u6210\u529f!'}],u'user':{}}
    article_draft="article_draft",
)


# 基于redis的消息订阅（发布接收缓存更新消息）
redis_pub_sub_channels = dict(
    cache_message_channel="site_cache_message_channel",
)

# 消息订阅(基于redis)配置
redis_pub_sub_config = dict(
    host="127.0.0.1",
    port=6379,
    password=None,
    autoconnect=True,
    channels=[redis_pub_sub_channels['cache_message_channel'],],
)


# 站点缓存(redis)
site_cache_config = dict(
    db_no=1,
    host="127.0.0.1",
    port=6379,
    password=None,
    max_connections=10,
)

# 关联model.site_info中的字段,只缓存这些在redis 1中
site_cache_keys = dict(
    title="title", # 网站标题
    signature="signature", # 个人签名
    navbar="navbar", # 导航橍
    menus="menus", # 主菜单
    article_types_not_under_menu="article_types_not_under_menu",
    plugins="plugins",
    pv="pv", # PV(访问量)：即Page View, 即页面浏览量或点击量，用户每次刷新即被计算一次
    uv="uv", # UV(独立访客)：即Unique Visitor,访问您网站的一台电脑客户端为一个访客。00:00-24:00内相同的客户端只被计算一次
    article_count="article_count",
    comment_count="comment_count",
    article_sources="article_sources",
    source_articles_count="source_{}_articles_count",
)

# 数据库配置
database_config = dict(
    engine=None,
    # engine_url='postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog',
    # 如果是使用mysql+mysqldb，在确认所有的库表列都是uft8编码后，依然有字符编码报错，
    # 可以尝试在该url末尾加上queryString charset=utf8
    engine_url='mysql://root:Nwhh-2018+@localhost:3306/dt_blog?charset=utf8',
    # engine_url='mysql+mysqldb://root:1qaz2wsx@localhost:3306/dt_blog?charset=utf8',
    engine_setting=dict(
        echo=False,  # print sql
        echo_pool=False,
        pool_recycle=25200,# 设置7*60*60秒后回收连接池，默认-1，从不重置
        # 该参数会在每个session调用执行sql前校验当前时间与上一次连接时间间隔是否超过pool_recycle，如果超过就会重置。
        # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
        # 如果mysql重启或断开过连接，那么依然会在第一次时报"MySQL server has gone away"，
        # 假如需要非常严格的mysql断线重连策略，可以设置心跳。
        # 心跳设置参考https://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away
        # 如果connection空闲了2小时, 自动重新获取, 以防止connection被db server关闭
        pool_size=20, # 指定的数据库池的大小
        max_overflow=20, # max_overflow时候就不能在创建连接了
    ),
)

# 站点相关配置以及tornado的相关参数
config = dict(
# http://localhost:63342/dt_blog/basic_web/1.html?_ijt=pdjaobmhqd6tui2jgk2ae8vb16
    debug=False,
    log_level="DEBUG",
    # log_level="WARNING",
    log_console=True,
    # log_console=False,
    log_file=True,
    log_file_path="logs/log",  # 末尾自动添加 @端口号.txt_日期
    compress_response=True,
    xsrf_cookies=True,
    cookie_secret="kjsdhfweiofjhewnfiwehfneiwuhniu",
    login_url="/auth/login",
    port=8887,
    max_threads_num=500,
    database=database_config,
    redis_session=redis_session_config,
    session_keys=session_keys,
    master=True,  # 是否为主从节点中的master节点, 整个集群有且仅有一个,(要提高可用性的话可以用zookeeper来选主,该项目就暂时不做了)
    navbar_styles={"inverse": "魅力黑", "default": "优雅白"},  # 导航栏样式
    default_avatar_url="identicon",
    # 刚好我的qq邮箱使用的gravatar 保存在current_user['avatar']中
    # https://www.gravatar.com/avatar/dfe6cbdc8d08992c55350d9c26e5975a?s=40&d=identicon
    application=None,  # 项目启动后会在这里注册整个server，以便在需要的地方调用，勿修改
)