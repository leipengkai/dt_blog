# coding=utf-8
import tornado.ioloop
import tornado.gen
import tornadis
import logging

logger = logging.getLogger(__name__)


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

    #比如说， 要订阅频道 foo 和 bar ， 客户端可以使用频道名字作为参数来调用 SUBSCRIBE 命令：
    # redis> SUBSCRIBE foo bar
    # 当有客户端发送信息到这些频道时， Redis 会将传入的信息推送到所有订阅这些频道的客户端里面

    def get_pub_client(self):
        if not self.pub_client:
            self.pub_client = tornadis.Client(host=self.redis_pub_sub_config['host'],
                                              port=self.redis_pub_sub_config['port'],
                                              password=self.redis_pub_sub_config['password'],
                                              autoconnect=self.autoconnect)
        return self.pub_client

    @tornado.gen.coroutine
    # todo 指定更新内容 客户端发送内容 先不管有没有关注 交给do_msg() 的update_by_sub_msg()去判断该做
    # 向所有 节点发布信息  收到之后 将通过do_msg() 方法去更新redis的site_cache
    def pub_call(self, msg, *channels):
        pub_client = self.get_pub_client()
        if not pub_client.is_connected():
            yield pub_client.connect()
        if not channels:
            channels = self.redis_pub_sub_config['channels']
        for channel in channels:
            yield pub_client.call("PUBLISH", channel, msg)


    # 当有客户端发送信息到这些频道时
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
                yield self.first_do_after_subscribed()
                logging.info(2) # 启动main走 1,2 ，并且到2就停止了
                while True:
                    msgs = yield self.client.pubsub_pop_message()
                    # logging.info('只有在 启动时才有唯一一个的self.client')
                    # logging.info(self.client) # <tornadis.pubsub.PubSubClient object at 0x7f2649d02d50>
                    logging.info(3) # 当localhost:8888请求时,执行3,4, 之后的任何一次请求都走  3和4 不管有没有调用pub_call
                    try:
                        yield self.do_msg(msgs) # 难道有点长连接的意思
                        logging.info(4)
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

    # override
    @tornado.gen.coroutine
    def first_do_after_subscribed(self):
        logger.info("订阅成功")

    # override
    @tornado.gen.coroutine
    def do_msg(self, msgs):
        logger.info("收到订阅消息"+ str(msgs))
