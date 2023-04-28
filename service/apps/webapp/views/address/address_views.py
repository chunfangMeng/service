import json

from rest_framework.viewsets import GenericViewSet

from apps.webapp.models.webapp_models import ChinaProvinceArea
from apps.webapp.views.address.serializers import ChinaAddressAreaSerializer
from django.core.cache import cache
from drf.response import JsonResponse


class ProvincesAreaView(GenericViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = ChinaProvinceArea.objects.all().order_by('id')
    serializer_class = ChinaAddressAreaSerializer
    all_address_cache_key = 'ALL_CHINA_ADDRESS'

    def list(self):
        try:
            all_china_address = json.loads(cache.get(self.all_address_cache_key, '{}'))
            if all_china_address:
                return JsonResponse(all_china_address)
        except Exception as e:
            print(e)
        all_data = self.get_serializer(
            self.queryset, many=True
        ).data
        city_group = {}
        area_group = {}
        all_china_address = []
        for item in all_data:
            # 省
            if item.get('area_code') == item.get('parent_code') or item.get('parent_code') is None:
                all_china_address.append({
                    'area_code': item.get('area_code'),
                    'name': item.get('name'),
                })
            else:
                # 市
                if item.get('parent_code') not in city_group.keys():
                    city_group[item.get('parent_code')] = [{
                        'area_code': item.get('area_code'),
                        'name': item.get('name'),
                        'parent_code': item.get('parent_code')
                    }]
                else:
                    city_group.get(item.get('parent_code')).append({
                        'area_code': item.get('area_code'),
                        'name': item.get('name'),
                        'parent_code': item.get('parent_code')
                    })
                # 区
                if item.get('parent_code') not in [province.get('area_code') for province in all_china_address]:
                    area_group.setdefault(item.get('parent_code'), []).append({
                        'area_code': item.get('area_code'),
                        'name': item.get('name'),
                        'parent_code': item.get('parent_code')
                    })
        for province_item in all_china_address:
            if city_group.get(province_item.get('area_code')) is not None:
                province_item.setdefault('child', city_group.get(province_item.get('area_code')))
                for city_item in province_item.get('child'):
                    city_item.setdefault('child', area_group.get(city_item.get('area_code')))
        cache.set(self.all_address_cache_key, json.dumps(all_china_address), 24 * 60 * 60 * 7)
        return JsonResponse(all_china_address)

