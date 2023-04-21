import json

from django.core.cache import cache
from rest_framework.viewsets import GenericViewSet

from apps.webapp.models.cms_models import Banner
from apps.webapp.views.cms_serializers import ClientBannerSerializer
from drf.response import JsonResponse


class ClientCmsView(GenericViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = ClientBannerSerializer

    def list(self, request):
        all_banner = cache.get(Banner.BANNER_CACHE_KEY)
        if all_banner:
            try:
                return JsonResponse(data=json.loads(all_banner))
            except json.JSONDecodeError:
                pass
        if self.queryset.count() == 0:
            return JsonResponse(data=[])
        banner_data = self.get_serializer(self.queryset, many=True)
        cache.set(Banner.BANNER_CACHE_KEY, json.dumps(banner_data.data), 24 * 60 * 60)
        return JsonResponse(data=banner_data.data)


