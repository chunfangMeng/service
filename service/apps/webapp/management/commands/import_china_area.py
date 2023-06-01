import json

from django.core.management.base import BaseCommand

from apps.webapp.models.webapp_models import ChinaProvinceArea


class Command(BaseCommand):
    help = "导入中国省市区信息"

    def handle(self, *args, **options):
        with open('./assets/ChinaArea.json', 'r') as f:
            source_data = json.loads(f.read())

        for province_item in source_data:
            ChinaProvinceArea.objects.update_or_create(
                area_code=province_item.get('code'),
                defaults={
                    'name': province_item.get('name')
                }
            )
            if province_item.get('cityList') is not None and len(province_item.get('cityList')) > 0:
                for city_item in province_item.get('cityList'):
                    ChinaProvinceArea.objects.update_or_create(
                        area_code=city_item.get('code'),
                        defaults={
                            'name': city_item.get('name'),
                            'parent_code': province_item.get('code')
                        }
                    )
                    if city_item.get('areaList') is not None and len(city_item.get('areaList')) > 0:
                        for area_item in city_item.get('areaList'):
                            ChinaProvinceArea.objects.update_or_create(
                                area_code=area_item.get('code'),
                                defaults={
                                    'name': area_item.get('name'),
                                    'parent_code': city_item.get('code')
                                }
                            )
        print('success')

