import django_filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from apps.member.auth_user import AuthContext
from apps.member.models.user_models import UserMember
from apps.member.views.serializers import MemberSerializer
from drf.auth import UserBaseAuthenticate
from drf.exceptions import RequestParamsError
from drf.mixins import CreateModelMixin, RetrieveModelMixin
from drf.response import JsonResponse
from drf.throttle import RedisTokenBucketThrottle


class MemberView(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = UserMember.objects.all().order_by('-id')
    serializer_class = MemberSerializer
    authentication_classes = [UserBaseAuthenticate]
    # throttle_classes = [RedisTokenBucketThrottle, ]
    auth_context = AuthContext()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    @action(methods=['get'], detail=False)
    def info(self, request):
        instance = self.queryset.filter(user=request.user).first()
        if not instance:
            raise RequestParamsError('请先进行登录')
        serializer = self.get_serializer(instance)
        return JsonResponse(data=serializer.data)

    @action(methods=['post'], detail=False, authentication_classes=[], permission_classes=[])
    def login(self, request):
        token_key, user, message = self.auth_context.auth(request)
        response = JsonResponse(data={'token': token_key}, message=message)
        response.set_cookie('token', token_key)
        return response


