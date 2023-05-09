import inspect
import sys

from abc import abstractmethod
from datetime import datetime, timedelta
from enum import Enum

import pytz
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.manager.models.user_models import ManagerUser, UserLoginLog
from apps.webapp.celery_tasks import user_bind_ip_area
from drf.exceptions import RequestParamsError


class AuthClientEnum(Enum):
    MEMBER = 0
    MANAGER = 1


class UserAuthenticate:
    @classmethod
    def auth_user(cls, request):
        username = request.data.get('username')
        password = request.data.get('password')
        hash_key = request.data.get('hash_key')
        captcha_code = request.data.get('check_code')
        if not username:
            raise RequestParamsError('用户名不能为空')
        if not password:
            raise RequestParamsError('密码不能为空')
        if not hash_key or not captcha_code:
            raise RequestParamsError('验证码不能为空')
        captcha_obj = CaptchaStore.objects.filter(hashkey=hash_key).first()
        if not captcha_obj:
            raise RequestParamsError('请刷新验证码后再试')
        now_date = timezone.now()
        if captcha_obj.expiration < now_date:
            raise RequestParamsError('验证码已过期')
        if captcha_obj.challenge.upper() != captcha_code.upper():
            raise RequestParamsError('验证码错误')
        user_obj = authenticate(request, username=username, password=password)
        if not user_obj:
            raise RequestParamsError('用户名或者密码错误')
        login(request, user_obj)
        token, created = Token.objects.get_or_create(user=user_obj)
        utc_now = datetime.utcnow()
        if token.created < (utc_now - timedelta(hours=24 * 7)).replace(tzinfo=pytz.timezone('UTC')):
            token.delete()
            token, created = Token.objects.get_or_create(user=user_obj)
        return token.key, user_obj

    def logout(self, request):
        request.user.auth_token.delete()
        logout(request)

    @abstractmethod
    def auth(self, request):
        pass


class UserMemberAuth(UserAuthenticate):
    """
    前台登陆逻辑
    """
    CLIENT_CODE = AuthClientEnum(0)

    def auth(self, request):
        token_key, user = self.auth_user(request)
        return token_key, user, '登陆成功'


class UserManagerAuth(UserAuthenticate):
    """
    后台登陆逻辑
    """
    CLIENT_CODE = AuthClientEnum(1)

    def auth(self, request):
        token_key, user = self.auth_user(request)
        manager_user = ManagerUser.objects.filter(user=user).first()
        if not manager_user:
            return None, None, '该账号无法登陆后台管理系统'
        return token_key, user, '登陆成功'


class AuthContext(object):
    CLIENT_SELECTOR = {}
    ip_area_url = ''

    def __init__(self, client=UserMemberAuth.CLIENT_CODE):
        for name, _class in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if issubclass(_class, UserAuthenticate) and hasattr(_class, 'CLIENT_CODE'):
                self.CLIENT_SELECTOR.update({_class.CLIENT_CODE: _class})
        self.auth_class = self.CLIENT_SELECTOR.get(client)
        self.client = client

    def auth(self, request):
        token_key, user, message = self.auth_class().auth(request)
        # 记录登录日志
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip_address:
            ip_address = request.META.get('REMOTE_ADDR', "")
        login_log_object = UserLoginLog.objects.create(
            user=user,
            client=self.client.value,
            ip_address=ip_address,
        )
        user_bind_ip_area.delay(ip_address, login_log_object.id)
        return token_key, user, message

    def user_logout(self, request):
        self.auth_class().logout(request)
