from rest_framework.exceptions import Throttled

from drf.response import JsonResponse


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    exception_class = exc.__class__.__name__
    filename = exc.__traceback__.tb_frame.f_code.co_filename
    lineno = exc.__traceback__.tb_lineno
    print(f'{exception_class} at {filename}:{lineno}')
    if isinstance(exc, Throttled):
        exc.detail = '请求次数太过频繁，请稍后再试'
    return JsonResponse(
        code=exc.status_code if hasattr(exc, 'status_code') else 500,
        message=exc.detail if hasattr(exc, 'detail') else '服务器错误',
        data=[],
        status=exc.status_code if hasattr(exc, 'status_code') else 500
    )
