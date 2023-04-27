import logging
import traceback

from rest_framework.exceptions import Throttled

from django.conf import settings

from drf.response import JsonResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    logger = logging.getLogger('django')
    if settings.DEBUG:
        traceback_info = traceback.format_exc()
        logger.info(traceback_info)
    if isinstance(exc, Throttled):
        exc.detail = '请求次数太过频繁，请稍后再试'
    return JsonResponse(
        code=exc.status_code if hasattr(exc, 'status_code') else 500,
        message=exc.detail if hasattr(exc, 'detail') else '服务器错误',
        data=[],
        status=exc.status_code if hasattr(exc, 'status_code') else 500
    )
