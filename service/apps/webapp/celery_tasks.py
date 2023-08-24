import json

from apps.manager.models import UserLoginLog
from libs.requests_client import Requests
from service.celery import app


@app.task
def user_bind_ip_area(ip_address: str, login_log_id: int) -> None:
    """
    IP地址绑定地区
    :param ip_address: IP地址
    :param login_log_id: 登录日志ID
    :return:
    """
    sync_requests = Requests()
    address_url = f'http://opendata.baidu.com/api.php?query={ip_address}&co=&resource_id=6006&oe=utf8'
    ip_area = sync_requests.common_request(address_url)
    instance = UserLoginLog.objects.filter(id=login_log_id)
    try:
        ip_area = json.loads(ip_area)
        if ip_area.get('data'):
            instance.ip_area = ip_area.get('data')[0].get('location')
            instance.save(update_fields=['ip_area'])
    except json.JSONDecodeError:
        pass
