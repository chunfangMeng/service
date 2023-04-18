from rest_framework.exceptions import APIException


class TokenDoesNotExist(APIException):
    status_code = 401
    default_detail = 'Token已失效'
    default_code = 'Token not valid'


class RequestParamsError(APIException):
    status_code = 421
    default_detail = '参数错误'
    default_code = 'params error'
