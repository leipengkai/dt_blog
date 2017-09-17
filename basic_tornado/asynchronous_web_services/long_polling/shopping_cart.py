import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

# (购物车)控制器
class ShoppingCart(object):
	totalInventory = 10
	callbacks = []
	carts = {}

	def register(self, callback):
		self.callbacks.append(callback)

	def moveItemToCart(self, session):
		if session in self.carts:
			return
		
		self.carts[session] = True
		self.notifyCallbacks()
	
	def removeItemFromCart(self, session):
		if session not in self.carts:
			return
		
		del(self.carts[session])
		self.notifyCallbacks()
	
	def notifyCallbacks(self):
		print(self.callbacks)
		# [<bound method StatusHandler.on_message of <__main__.StatusHandler object at 0x7fd989244eb8>>]
		self.callbacks[:] = [c for c in self.callbacks if self.callbackHelper(c)]
		# 既然长轮询连接已经关闭，购物车控制器必须删除已注册的回调函数列表中的回调函数。
		# 在这个例子中，我们只需要将回调函数列表替换为一个新的空列表。在请求处理中被调用并完成后删除已注册的回调函数十分重要
		print(self.callbacks)
	
	def callbackHelper(self, callback):
		callback(self.getInventoryCount())
		return False
	
	def getInventoryCount(self):
		return self.totalInventory - len(self.carts)

class DetailHandler(tornado.web.RequestHandler):
	def get(self):
		session = uuid4()
		count = self.application.shoppingCart.getInventoryCount()
		self.render("index.html", session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
	def post(self):
		action = self.get_argument('action')
		session = self.get_argument('session')
		
		if not session:
			self.set_status(400)
			return
		
		if action == 'add':
			self.application.shoppingCart.moveItemToCart(session)
		elif action == 'remove':
			self.application.shoppingCart.removeItemFromCart(session)
		else:
			self.set_status(400)

class StatusHandler(tornado.web.RequestHandler):
	# 需要编写一个在初始化处理方法调用后不会立即关闭HTTP连接的RequestHandler子类,使用Tornado内建的asynchronous装饰器完成这项工作
	# 在get方法返回时不会关闭连接
	@tornado.web.asynchronous
	def get(self):
		print('register')
		self.application.shoppingCart.register()
		self.application.shoppingCart.register(self.on_message)
				# 注册了一个带有购物车控制器的      回调函数
	
	def on_message(self, count):
		print('callbake')
		self.write('{"inventoryCount":"%d"}' % count)
		self.finish()
		# 将当前库存数量写入客户端并关闭连接
	#使用 @tornado.web.asynchronous 在代码描述上类似于 Node.js
# 这里通过设置 on_message 回调函数.
# tornado 的 tornado.gen.coroutine 方便在于, 少定义一个回调函数,
# 以顺序代码的方式(里面有 yield 进程挂起) 书写代码.
		
class Application(tornado.web.Application):
	def __init__(self):

		self.shoppingCart = ShoppingCart()
		
		handlers = [
			(r'/', DetailHandler),# 一到/目录，生成session,并注册回调函数,保存到数组中,但没有调用 GET /cart/status接口,仅仅是加载
			(r'/cart', CartHandler),# 调用所有的回调函数，断开所有长轮询连接,并清空所有的回调函数,而且再次注册新的回调函数(创建新的长轮询连接)session保持不变
			# 调用了 GET /cart/status接口
			(r'/cart/status', StatusHandler) # 创建长轮询连接
		]
		
		settings = {
			'template_path': 'templates',
			'static_path': 'static'
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()
	# 没有逻辑确保我们不会跌破总库存量，更不用说数据无法在Tornado应用的不同调用间或同一服务器并行的应用实例间保留。
	#
	#