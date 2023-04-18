import logging

from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

runtime_logging = logging.getLogger('system_watch')


class RunTimeWatch(object):
    def runtime_watch(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            ret = func(*args, **kwargs)
            runtime = datetime.utcnow() - start_time
            print(f'运行时间：{runtime}')
            return ret
        return wrapper

    runtime_watch = staticmethod(runtime_watch)


class RunTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = datetime.utcnow()

    def process_response(self, request, response):
        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")
        client_ip = ip.split(",")[-1].strip() if ip else ""
        runtime = datetime.utcnow() - request.start_time
        runtime_logging.info({
            'Url': request.path,
            'Method': request.method,
            'UserName': request.user.username if request.user and request.user.username else '',
            'IP': client_ip,
            'TotalSeconds': runtime.total_seconds(),
            'status_code': response.status_code,
            'HTTP_COOKIE': request.META.get('HTTP_COOKIE')
        })
        return response

