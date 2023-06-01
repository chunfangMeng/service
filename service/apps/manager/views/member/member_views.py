from rest_framework.viewsets import GenericViewSet

from apps.manager.views.member.serializers import MemberSerializer
from apps.member.models.user_models import UserMember
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin
from drf.permission import ManagerPermission
from drf.response import JsonResponse


class MemberView(GenericViewSet, ListModelMixin):
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = [ManagerPermission, ]
    permission_list = ['member_view', ]
    queryset = UserMember.objects.all().order_by('-id')
    serializer_class = MemberSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data)

