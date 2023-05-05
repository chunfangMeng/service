from rest_framework.exceptions import APIException


class TokenDoesNotExist(APIException):
    status_code = 401
    default_detail = 'Token已失效'
    default_code = 'Token not valid'


class RequestParamsError(APIException):
    status_code = 421
    default_detail = '参数错误'
    default_code = 'params error'

    def __init__(self, message: str):
        self.detail = message
        super().__init__(message)


class ApiNotFoundError(APIException):
    status_code = 404
    default_detail = '资源不存在或已被删除'
    default_code = '404 Not Found'

    def __init__(self, message: str):
        self.detail = message
        super().__init__(message)
