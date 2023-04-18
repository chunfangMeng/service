import time


class TokenBucket(object):

    def __init__(self, rate, capacity):
        self._rate = rate
        self._capacity = capacity
        self._current_amount = 0
        self._last_consume_time = int(time.time())

    def consume(self, token_amount):
        increment = (int(time.time())) - self._last_consume_time * self._rate
        self._current_amount = min(increment + self._current_amount, self._capacity)
        if token_amount > self._current_amount:
            return False
        self._last_consume_time = int(time.time())
        self._current_amount -= token_amount
        return True
