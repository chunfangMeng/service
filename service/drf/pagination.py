import math

from rest_framework.pagination import PageNumberPagination
from drf.response import JsonResponse


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10000
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        """
        :param data:
        :return:
        """
        return JsonResponse({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })
