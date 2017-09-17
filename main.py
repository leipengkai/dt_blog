# coding=utf-8
import os, sys

import concurrent.futures
import logging
import tornado.ioloop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options


import log_config
from config import config, redis_pub_sub_config, site_cache_config, redis_session_config
from controller.base import BaseHandler
from extends.cache_tornadis import CacheManager
from extends.session_tornadis import SessionManager
from service.init_service import flush_all_cache
from service.pubsub_service import PubSubService
from url_mapping import handlers

# tornado server相关参数
settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    compress_response=config['compress_response'],
    xsrf_cookies=config['xsrf_cookies'],
    cookie_secret=config['cookie_secret'],
    login_url=config['login_url'],
    debug=config['debug'],
    default_handler_class=BaseHandler,
)


# sqlalchemy连接池配置以及生成链接池工厂实例
def db_poll_init():
    engine_config = config['database']['engine_url']
    # 创建一个带连接池的引擎
    engine = create_engine(engine_config, **config['database']["engine_setting"])
    config['database']['engine'] = engine
    # 当使用session后就显示地调用session.close()，也不能把连接关闭，连接由QueuePool连接池管理并复用
    db_poll = sessionmaker(bind=engine) # 负责执行内存中的对象和数据库表之间的同步工作,
    # session = db_poll()  # 先使用工程类来创建一个session
    # ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    # session.add(ed_user)
    # # 提交事务
    # session.commit()

    # 在session上面调用query()方法会创建一个Query对象
    # session.query(User).order_by(User.id).filter_by(fullname='Ed Jones')
    # 官方教程  http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
    return db_poll


def cache_manager_init():
    cache_manager = CacheManager(site_cache_config)
    return cache_manager


# 继承tornado.web.Application类，可以在构造函数里做站点初始化（，，，等）
class Application(tornado.web.Application):
    def __init__(self): # 初始站点配置
        # todo 加载缓存
        super(Application, self).__init__(handlers, **settings)
        self.session_manager = SessionManager(config['redis_session']) # 加载redies session 适用tornado的session
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(config['max_threads_num']) # 初始异步线程池
        self.db_pool = db_poll_init() # 初始数据库连接池
        self.cache_manager = cache_manager_init() # 加载站点缓存
        self.pubsub_manager = None


#  从命令行读取配置，如果这些参数不传，默认使用config.py的配置项
def parse_command_line():
    options.define("port", help="run server on a specific port", type=int)
    options.define("log_console", help="print log to console", type=bool)
    options.define("log_file", help="print log to file", type=bool)
    options.define("log_file_path", help="path of log_file", type=str)
    options.define("log_level", help="level of logging", type=str)
    # 集群中最好有且仅有一个实例为master，一般用于执行全局的定时任务
    options.define("master", help="is master node? (true:master / false:slave)", type=bool)
    # sqlalchemy engine_url, 例如pgsql 'postgresql+psycopg2://mhq:1qaz2wsx@localhost:5432/blog'
    options.define("engine_url", help="engine_url for sqlalchemy", type=str)
    # redis相关配置, 覆盖所有用到redis位置的配置
    options.define("redis_host", help="redis host e.g 127.0.0.1", type=str)
    options.define("redis_port", help="redis port e.g 6379", type=int)
    options.define("redis_password", help="redis password set this option if has pwd ", type=str)
    options.define("redis_db", help="redis db e.g 0", type=int)

    # 读取 项目启动时，命令行上添加的参数项
    options.logging = None  # 不用tornado自带的logging配置
    options.parse_command_line()
    # 覆盖默认的config配置
    if options.port is not None:
        config['port'] = options.port
    if options.log_console is not None:
        config['log_console'] = options.log_console
    if options.log_file is not None:
        config['log_file'] = options.log_file
    if options.log_file_path is not None:
        config['log_file_path'] = options.log_file_path
    if options.log_level is not None:
        config['log_level'] = options.log_level
    if options.master is not None:
        config['master'] = options.master
    if options.engine_url is not None:
        config['database']['engine_url'] = options.engine_url
    if options.redis_host is not None:
        redis_session_config['host'] = options.redis_host
        site_cache_config['host'] = options.redis_host
        redis_pub_sub_config['host'] = options.redis_host
    if options.redis_port is not None:
        redis_session_config['port'] = options.redis_port
        site_cache_config['port'] = options.redis_port
        redis_pub_sub_config['port'] = options.redis_port
    if options.redis_password is not None:
        redis_session_config['password'] = options.redis_password
        site_cache_config['password'] = options.redis_password
        redis_pub_sub_config['password'] = options.redis_password
    if options.redis_db is not None:
        redis_session_config['db_no'] = options.redis_db
        site_cache_config['db_no'] = options.redis_db


if __name__ == '__main__':
    # http://huangx.in/18/alembic-simple-tutorial
    #Alembic 是 Sqlalchemy 的作者实现的一个数据库版本化管理工具，它可以对基于Sqlalchemy的Model与数据库之间的历史关系进行版本化的维护
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'upgradedb':
            # 更新数据库结构，初次获取或更新版本后调用一次python main.py upgradedb即可
            from alembic.config import main
            main("upgrade head".split(' '), 'alembic')# 更新(迁移)数据库
            # alembic会在当前目录中查找迁移(即os.getcwd()) 查到的是alembic这个目录
            # $ alembic init alembic(目录)
            # 1.env.py 每次执行Alembic都会加载这个模块，主要提供项目Sqlalchemy Model 的连接,
            # 以及指定Alembic的数据库连接(也可以用alembic.ini文件去指定Alembic的数据库连接)

            # $ alembic revision -m "create account table"  #创建一个基本数据库版本
            # versions 存放生成的迁移脚本目录
            # $ alembic upgrade head 更新好最新的版本

            # 创建和编辑迁移脚本   script.py.mako 迁移脚本生成模版 4.编辑 upgrade  downgrade 方法，init数据库
            # 对model/models的数据库进行修改之后 直接运行如下命令 即可更新数据库和此迁移脚本
            # alembic revision --autogenerate -m "add weibo token fields for user"
            exit(0)
    # 加载命令行配置
    parse_command_line()
    # 加载日志管理
    log_config.init(config['port'], config['log_console'],
                    config['log_file'], config['log_file_path'], config['log_level'])
    # 创建application
    application = Application()
    application.listen(config['port'])
    logging.info(config['port'])
    # 全局注册application
    config['application'] = application
    loop = tornado.ioloop.IOLoop.current()
    # 加载redis消息监听客户端
    pubsub_manager = PubSubService(redis_pub_sub_config, application, loop)
    # SUBSCRIBE 、 UNSUBSCRIBE 和 PUBLISH 订阅/发布
    # 每次的请求都会更新主节点的缓存内容

    pubsub_manager.long_listen()
    application.pubsub_manager = pubsub_manager
    # 为master节点注册定时任务
    if config['master']:
        from extends.time_task import TimeTask
        TimeTask(config['database']['engine']).add_cache_flush_task(flush_all_cache).start_tasks()
    loop.start()
