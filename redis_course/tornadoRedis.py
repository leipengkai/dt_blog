import tornadoredis

CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=100, wait_for_available=True)#使用数据库连接池
c = tornadoredis.Client(host='localhost',port=6379, connection_pool=CONNECTION_POOL)
c.set('name','femn')
print(c.get('name'))
