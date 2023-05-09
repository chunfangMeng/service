from rest_framework.viewsets import GenericViewSet

from apps.manager.views.member.serializers import MemberSerializer
from apps.member.models.user_models import UserMember
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin


class MemberView(GenericViewSet, ListModelMixin):
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = UserMember.objects.all().order_by('-id')
    serializer_class = MemberSerializer

