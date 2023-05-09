import redis

from django.conf import settings

from libs.common import Singleton


class RedisClient(metaclass=Singleton):
    def __init__(self):
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.redis_cli = redis.StrictRedis(connection_pool=pool)

