import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

import urllib
import json
import datetime
import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	@tornado.gen.engine
	# 记住@tornado.gen.engine装饰器的使用需要刚好在get方法的定义之前；这将提醒Tornado这个方法将使用tornado.gen.Task类
	def get(self):
		query = self.get_argument('q','')
		client = tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(client.fetch,r'https://twitter.com/search?q=python3&src=typd')
		#tornado.gen.Task对象的一个实例，将我们想要的调用和传给该调用函数的参数传递给那个函数。
		# 这里，yield的使用返回程序对Tornado的控制，允许在HTTP请求进行中执行其他任务。
		# 当HTTP请求完成时，RequestHandler方法在其停止的地方恢复。这种构建的美在于它在请求处理程序中返回HTTP响应，而不是回调函数中
		# 所有请求相关的逻辑位于同一个位置,而HTTP请求依然是异步执行的
		body = json.loads(response.body)
		result_count = len(body['results'])
		now = datetime.datetime.utcnow()
		raw_oldest_tweet_at = body['results'][-1]['created_at']
		oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
				"%a, %d %b %Y %H:%M:%S +0000")
		seconds_diff = time.mktime(now.timetuple()) - \
				time.mktime(oldest_tweet_at.timetuple())
		tweets_per_second = float(result_count) / seconds_diff
		self.write("""
<div style="text-align: center">
	<div style="font-size: 72px">%s</div>
	<div style="font-size: 144px">%.02f</div>
	<div style="font-size: 24px">tweets per second</div>
</div>""" % (query, tweets_per_second))
		self.finish()

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

	# 传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。
	# 如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高
	import time


	def consumer(): # 服务端
		r = ''
		while True:
			n = yield r  # 3. consumer通过yield拿到消息，处理，又通过yield把结果传回
			if not n: return print('[CONSUMER] Consuming %s...' % n)  # n为计数器

			print(n)

			time.sleep(1)
			r = '200 OK'

	def produce(c):
		next(c)  # 不是值 1. 启用生成器
		n = 0
		while n < 5:
			n = n + 1
			print('[PRODUCER] Producing %s...' % n)
			r = c.send(n)  # 这里才是迭代器中的值 2. 一旦生产了东西，通过c.send(n)切换到consumer执行
			print('[PRODUCER] Consumer return: %s' % r)  # 4. produce拿到consumer处理的结果，继续生产下一条消息
		c.close()  # 5. produce决定不生产了，通过c.close()关闭consumer，整个过程结束


	if __name__ == '__main__':
		c = consumer()
		produce(c)
	# 整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。 子程序就是协程的一种特例.
	# 线程确实比协程性能更好。因为线程能利用多核达到真正的并行计算，如果任务设计的好，线程能几乎成倍的提高你的计算能力，说线程性能不好的很多 是因为没有设计好导致大量的锁，切换，等待，这些很多都是应用层的问题.
	# 而协程因为是非抢占式，所以需要用户自己释放使用权来切换到其它协程，因此 同一时间其实只有一个协程拥有运行权，相当于单线程的能力
