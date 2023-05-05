from django.contrib.auth.views import auth_logout
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.authtoken.models import Token

from apps.manager.models.user_models import ManagerUser
from apps.manager.views.auth.serializers import ManageUserSerializer
from apps.member.auth_user import AuthContext, AuthClientEnum
from drf.auth import ManageAuthenticate
from drf.response import JsonResponse


class ManageUserView(GenericViewSet):
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
