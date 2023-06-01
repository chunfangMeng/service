from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet

from apps.manager.models import ManagerUser
from apps.manager.views.staff.filters import StaffFilter
from apps.manager.views.staff.serializers import ManagerStaffSerializer
from drf.auth import ManageAuthenticate
from drf.mixins import ListModelMixin
from drf.permission import ManagerPermission


class ManagerStaffView(GenericViewSet, ListModelMixin):
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = [ManagerPermission, ]
    queryset = ManagerUser.objects.all().order_by('-id')
    serializer_class = ManagerStaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StaffFilter
