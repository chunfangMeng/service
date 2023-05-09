import requests

from libs.common import Singleton


class Requests(metaclass=Singleton):
    def __init__(self):
        self.client = requests.Session()

    def get(self, url, headers=None, timeout=2):
        if headers is None:
            headers = {
                'Content-Type': 'application/json'
            }
        with self.client as client:
            res = client.get(url, headers=headers, timeout=timeout)
            if headers is None:
                return res.json()
            return res.text
