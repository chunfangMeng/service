import base64

from django.http import Http404
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from captcha.views import CaptchaStore, captcha_image
from drf.response import JsonResponse


class CaptchaView(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    @classmethod
    def create_image(cls, request, hash_key):
        captcha_img = captcha_image(request, hash_key)
        base64_obj = base64.b64encode(captcha_img.content)
        return base64_obj.decode('utf-8')

    def list(self, request, *args, **kwargs):
        hash_key = CaptchaStore.generate_key()
        captcha_obj = CaptchaStore.objects.filter(hashkey=hash_key).first()
        if not captcha_obj:
            return JsonResponse(code=4021, message="请稍后再试")
        return JsonResponse(data={
            'hash_key': hash_key,
            'base64_image': CaptchaView.create_image(request, hash_key)
        })

    @action(methods=['get'], detail=False)
    def refresh(self, request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            raise Http404
        new_key = CaptchaStore.pick()
        to_json_response = {
            "hash_key": new_key,
            "base64_image": CaptchaView.create_image(request, new_key)
        }
        return JsonResponse(data=to_json_response)
