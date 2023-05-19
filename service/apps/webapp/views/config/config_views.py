from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet

from apps.webapp.models import CurrencyConfig
from apps.webapp.views.config.filters import CurrencyConfigFilter
from apps.webapp.views.config.serializers import CurrencySerializer
from drf.auth import ManageAuthenticate
from drf.response import JsonResponse


class CurrencyView(GenericViewSet):
    """货币配置"""
    authentication_classes = [ManageAuthenticate, ]
    permission_classes = []
    queryset = CurrencyConfig.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = CurrencyConfigFilter

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_obj = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer_obj.data)
