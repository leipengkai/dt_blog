# coding=utf-8
import tornado.ioloop
import tornado.gen
import tornadis
import logging

logger = logging.getLogger(__name__)

# 根据发布/订阅 去更新站点内容
class PubSubTornadis(object):

    def __init__(self, redis_pub_sub_config, loop=None):
        self.redis_pub_sub_config = redis_pub_sub_config
        if not loop:
            loop = tornado.ioloop.IOLoop.current()
        self.loop = loop
        self.autoconnect = self.redis_pub_sub_config['autoconnect']
        self.client = self.get_client()
        self.pub_client = None
        self.connect_times = 0
        self.max_connect_wait_time = 10

    # 发送者（发送信息的客户端）不是将信息直接发送给特定的接收者（接收信息的客户端）， 而是将信息发送给频道（channel）
    # 然后由频道将信息转发给所有对这个频道感兴趣的订阅者。


    # 发布端
    def get_pub_client(self):
        if not self.pub_client:
            self.pub_client = tornadis.Client(host=self.redis_pub_sub_config['host'],
                                              port=self.redis_pub_sub_config['port'],
                                              password=self.redis_pub_sub_config['password'],
                                              autoconnect=self.autoconnect)
        return self.pub_client

    @tornado.gen.coroutine
    def pub_call(self, msg, *channels):
        pub_client = self.get_pub_client()
        if not pub_client.is_connected():
            yield pub_client.connect()
        if not channels:
            channels = self.redis_pub_sub_config['channels']
        for channel in channels:
            yield pub_client.call("PUBLISH", channel, msg)


    # 订阅接收端
    def get_client(self):
        client = tornadis.PubSubClient(host=self.redis_pub_sub_config['host'], port=self.redis_pub_sub_config['port'],
                                       password=self.redis_pub_sub_config['password'],
                                       autoconnect=self.autoconnect)
        return client

    def long_listen(self):
        # logging.info('在ioloop开启后执行的回调函数callback 只执行一个的')
        self.loop.add_callback(self.connect_and_listen, self.redis_pub_sub_config['channels'])

    @tornado.gen.coroutine
    def connect_and_listen(self, channels):
        # logging.info('这里也是 只执行了一次')
        connected = yield self.client.connect()
        logging.info(1)
        if connected:
            # 订阅频道 subscribed
            subscribed = yield self.client.pubsub_subscribe(*channels)
            if subscribed:
                self.connect_times = 0
                # 更新站点缓存信息
                yield self.first_do_after_subscribed()
                logging.info(2) # 启动main走 1,2 ，并且到2就停止了
                while True:
                    # 每个请求都会发布一条信息,没有请求则阻塞着(实则只要调用了pub_call就会接收到信息)
                    # 默认是发送add_pv_uv()中的'blog_view_count_updated'内容
                    msgs = yield self.client.pubsub_pop_message()
                    logging.info(3) # 当localhost:8888请求时,执行3,4, 之后的任何一次请求都走  3和4
                    try:
                        yield self.do_msg(msgs)
                        # logging.info(4)
                        if isinstance(msgs, tornadis.TornadisException):
                            # closed connection by the server
                            break
                    except Exception, e:
                        logger.exception(e)
            self.client.disconnect()
        if self.autoconnect:
            wait_time = self.connect_times \
                if self.connect_times < self.max_connect_wait_time else self.max_connect_wait_time
            logger.warn("等待{}s，重新连接redis消息订阅服务".format(wait_time))
            yield tornado.gen.sleep(wait_time)
            self.long_listen()
            self.connect_times += 1

    # 通过设置IOLoop端口时,增加的回调函数,此回调函数的作用是
    # 1. 在host=localhost的redis这个数据库中 对频道的订阅
    # 2. 第一次根据mysql去初始化redis数据库并更新站点内容,之后则仅仅是读取redis数据库
    # 3. 等待发布端 发布信息
    # 每个请求都会发布一条信息,没有请求则阻塞着 默认是发送add_pv_uv()中的'blog_view_count_updated'内容
    # 4. 按发布信息的内容 去更新站点的内容

    # override
    @tornado.gen.coroutine
    def first_do_after_subscribed(self):
        logger.info("订阅成功")

    # override
    @tornado.gen.coroutine
    def do_msg(self, msgs):
        logger.info("收到订阅消息"+ str(msgs))
