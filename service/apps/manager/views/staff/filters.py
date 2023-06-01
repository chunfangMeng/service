from datetime import timedelta

from django_filters import rest_framework
from django.db.models import Q

from apps.manager.models import ManagerUser


class StaffFilter(rest_framework.FilterSet):
    create_start_date = rest_framework.DateTimeFilter(field_name='user__date_joined', lookup_expr='gt')
    create_end_date = rest_framework.DateTimeFilter(method='created_end_date_filter')
    keyword = rest_framework.CharFilter(method='keyword_filter')

    def created_end_date_filter(self, queryset, _, value):
        return queryset.filter(user__date_joined__lt=(value + timedelta(days=1)))

    def keyword_filter(self, queryset, _, value):
        return queryset.filter(Q(job_number__icontains=value) |
                               Q(nickname__icontains=value) | Q(user__username__icontains=value))

    class Meta:
        model = ManagerUser
        fields = {}
