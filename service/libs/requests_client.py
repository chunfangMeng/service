import requests

from libs.common import Singleton


class Requests(metaclass=Singleton):
    def __init__(self):
        self.client = requests.Session()

    def common_request(self, url=None, method=None, params=None, data=None, headers=None, timeout=None):
        if headers is None:
            headers = {
                'Content-Type': 'application/json'
            }
        try:
            res = self.client.request(
                url=url,
                method=method,
                params=params,
                data=data,
                headers=headers,
                timeout=timeout
            )
            if headers.get('Content-Type') == 'application/json':
                return res.json()
            return res.text
        except requests.ConnectionError:
            return False
        except requests.ReadTimeout:
            return False