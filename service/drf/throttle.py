import time

from rest_framework import exceptions
from rest_framework.throttling import SimpleRateThrottle

from libs.redis import RedisClient


class RedisTokenBucketThrottle(SimpleRateThrottle):
    def __init__(self):
        self.redis_client = RedisClient().redis_cli
        self.capacity = 30  # 每分钟最多请求次数
        self.fill_rate = 1 / 20  # 每秒填充 token 数量

    def get_cache_key(self, request, view):
        return self.get_ident(request)

    def get_rate(self):
        return self.capacity, self.fill_rate

    def allow_request(self, request, view):
        cache_key = self.get_cache_key(request, view)
        capacity, fill_rate = self.get_rate()
        timestamp = time.time()

        # 从 Redis 中获取当前的 token 数量和最后填充的时间戳
        token_count = self.redis_client.get(cache_key)
        last_timestamp = self.redis_client.get(f'{cache_key}_timestamp')

        # 计算当前应该有多少个 token
        if token_count is None:
            current_token_count = capacity
        else:
            current_token_count = min(
                int(token_count) + int((timestamp - float(last_timestamp)) * fill_rate),
                capacity,
            )

        # 检查当前的 token 数量是否足够
        if current_token_count <= 0:
            raise exceptions.Throttled(detail='Request was throttled.')

        # 如果 token 数量足够，则减少 token 数量，并更新最后填充的时间戳
        self.redis_client.set(cache_key, current_token_count - 1)
        self.redis_client.set(f'{cache_key}_timestamp', timestamp)

        return True
