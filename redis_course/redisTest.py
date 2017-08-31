import redis
if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # 选择数据库 默认是0数据库
    # > select 1
    r.publish()
    # r.set('foo', 'bar')
    # # True
    # print(r.get('foo'))#./redis-server ./server-cli get foo
    # 'bar'

    print(r.exists('foo'))#True
    # r.append('one','Hello')
    # r.append('one',' World')
    print(r.get('one'))#b'Hello World'
    print(r.getrange('one',0,4))#b'Hello'    和python的list不同，它包括4
    print(r.bitcount('one'))# 计算字节的总个数 43
    # a =0
    # for i in r.get('one'):
    #     b = len(int(i).to_bytes(4,'big'))#这个算不出来
    #     a+=b
    # print(a)
    #
    a = '雷'.encode()#b'\xe9\x9b\xb7'
    # r.set('雷','\xe9\x9b\xb7')
    print(r.bitpos('雷',1))# 2
    print(r.decr('雷'))# -2

    # print(r.incr('number'))#1
    # print(r.getset('number','0'))#b'1'
    # print(r.get('number'))# b'0'

    # print(r.incrby('sum',10))# 10
    # print(r.incrbyfloat('sum',2.0e2))#200 +10  210

    print(r.mget('number','sum','one','nonexisting'))#[b'0', b'210', b'Hello World',None]
    # r.mset({'1':1,'2':2})
    # r.msetnx({'3':3,'4':4})
    # print(r.mget('1','2','3','4'))# [b'1', b'2', b'3', b'4']
    # r.psetex('femn',1000,'Hello')
    # print(r.pttl('femn')) #1000
    # print(r.get('femn')) # b'Hello'

    # r.setex('key1',10,'Hello')
    # print(r.ttl('key1'))#10
    # print(r.get('key1'))# b'Hello'
    print(r.setnx('key2','World'))#True
    print(r.get('key2')) # b'World

    print(r.setrange('key2', 4,'Redis'))# 9 set这个value的长度
    print(r.strlen('key2'))# 9
    print(r.get('key2'))# b'WorlRedis'