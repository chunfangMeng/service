import pytz

from datetime import datetime, timedelta
from django.conf import settings

from apps.manager.models import ManagerUser
from drf.exceptions import TokenDoesNotExist
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


class UserBaseAuthenticate(authentication.SessionAuthentication):

    @classmethod
    def verify_token(cls, token_obj):
        utc_now = datetime.utcnow()
        valid_date = (utc_now + timedelta(hours=24 * int(settings.REST_TOKEN_VALID_DAY))).replace(
            tzinfo=pytz.timezone('UTC')
        )
        if token_obj.created > valid_date:
            raise exceptions.AuthenticationFailed('请重新登陆')

    def authenticate(self, request):
        print(dir(request))
        print(request.META)
        print(request._request.user)
        user = getattr(request._request, 'user', None)
        if user and user.is_active:
            if not hasattr(user, 'auth_token') or user.auth_token is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(user.auth_token)
            self.enforce_csrf(request)
            return user, None
        token_key = request.META.get('HTTP_AUTHORIZATION')
        print('token>>>', token_key, request.META.get('HTTP_COOKIE'))
        if not token_key:
            raise exceptions.AuthenticationFailed('token不能为空')
        try:
            token_obj = Token.objects.get(key=token_key.split(' ')[1])
            if token_obj is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(token_obj)
            self.verify_manager(token_obj.user)
            request.user = token_obj.user
        except Token.DoesNotExist:
            raise TokenDoesNotExist('token无效')
        return token_obj.user, None


class ManageAuthenticate(UserBaseAuthenticate):

    @classmethod
    def verify_manager(cls, user):
        manager_user = ManagerUser.objects.filter(user=user).first()
        if not manager_user:
            raise exceptions.AuthenticationFailed('账号异常')

    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if user and user.is_active:
            if not hasattr(user, 'auth_token') or user.auth_token is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(user.auth_token)
            self.verify_manager(user)
            self.enforce_csrf(request)
            return user, None
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            raise exceptions.AuthenticationFailed('token不能为空')
        try:
            token_obj = Token.objects.get(key=token_key.split(' ')[1])
            if token_obj is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(token_obj)
            self.verify_manager(token_obj.user)
            request.user = token_obj.user
        except Token.DoesNotExist:
            raise TokenDoesNotExist('token无效')
        return token_obj.user, None


class MemberUserAuthenticate(UserBaseAuthenticate):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)
        if user and user.is_active:
            if not hasattr(user, 'auth_token') or user.auth_token is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(user.auth_token)
            self.verify_manager(user)
            self.enforce_csrf(request)
            return user, None
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if not token_key:
            raise exceptions.AuthenticationFailed('token不能为空')
        try:
            token_obj = Token.objects.get(key=token_key.split(' ')[1])
            if token_obj is None:
                raise exceptions.AuthenticationFailed('请重新登陆')
            self.verify_token(token_obj)
            self.verify_manager(token_obj.user)
            request.user = token_obj.user
        except Token.DoesNotExist:
            raise TokenDoesNotExist('token无效')
        return token_obj.user, None
