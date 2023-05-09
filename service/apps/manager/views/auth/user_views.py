from django.contrib.auth.views import auth_logout
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

from apps.manager.models.user_models import ManagerUser, UserLoginLog
from apps.manager.views.auth.serializers import ManageUserSerializer, UserLoginSerializer
from apps.member.auth_user import AuthContext, AuthClientEnum
from drf.auth import ManageAuthenticate
from drf.response import JsonResponse


class ManageUserView(GenericViewSet):
    """
    后台会员管理
    """
    queryset = ManagerUser.objects.all()
    serializer_class = ManageUserSerializer
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    auth_context = AuthContext(AuthClientEnum(1))

    @action(methods=['post'], detail=False, authentication_classes=[], permission_classes=[])
    def login(self, request):
        token_key, user, message = self.auth_context.auth(request)
        response = JsonResponse(
            data={
                'token': token_key,
                'user_id': user.id
            },
            message=message
        )
        response.set_cookie('token', token_key)
        return response

    @action(methods=['get'], detail=False)
    def info(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(user=request.user).first()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=False)
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        auth_logout(request)
        request.user.auth_token.delete()
        return JsonResponse()


class UserLoginLogView(GenericViewSet):
    """
    用户登录日志
    """
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = UserLoginLog.objects.all().order_by('-create_at')
    serializer_class = UserLoginSerializer

    @action(methods=['get'], detail=False)
    def personal(self, request):
        queryset = self.get_queryset().filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)

