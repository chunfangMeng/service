from django.db.models import Q
from django_filters import rest_framework

from apps.webapp.models.webapp_models import CurrencyConfig


class CurrencyConfigFilter(rest_framework.FilterSet):
    keyword = rest_framework.CharFilter(method='filter_keyword')

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(Q(abbreviation__icontains=value) | Q(name__icontains=value) | Q(code__icontains=value))

    class Meta:
        model = CurrencyConfig
        fields = ('keyword', )
