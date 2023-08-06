import redis


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton

@Singleton
class RedisPool:

    def __init__(self,host,port):
        self.host=host
        self.port=port

    def redis(self):
        pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
        return redis.Redis(connection_pool=pool)
