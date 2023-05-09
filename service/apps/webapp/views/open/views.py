from django.middleware.csrf import get_token
from rest_framework.viewsets import GenericViewSet

from drf.response import JsonResponse


class CsrfTokenView(GenericViewSet):
    def list(self, request):
        token = get_token(request)
        return JsonResponse(token)
