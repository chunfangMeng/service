from datetime import timedelta
from django_filters import rest_framework

from apps.product.models.product_models import ProductBrand


class BrandFilter(rest_framework.FilterSet):
    created_start_date = rest_framework.DateTimeFilter(field_name='create_at', lookup_expr='gt')
    created_end_date = rest_framework.DateTimeFilter(method='created_end_date_filter')
    update_start_date = rest_framework.DateTimeFilter(field_name='last_update', lookup_expr='gt')
    update_end_date = rest_framework.DateTimeFilter(method='update_end_date_filter')

    def created_end_date_filter(self, queryset, name, value):
        return queryset.filter(create_at__lt=(value + timedelta(days=1)))

    def update_end_date_filter(self, queryset, name, value):
        return queryset.filter(last_update__lt=(value + timedelta(days=1)))

    class Meta:
        model = ProductBrand
        fields = {
            'founder': ['exact'],
            'last_editor': ['exact']
        }
