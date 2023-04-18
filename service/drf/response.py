from rest_framework.response import Response


class JsonResponse(Response):
    def __init__(self, data=None, code=200, message='success', status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        res = {
            'code': code,
            'message': message,
            'data': []
        }
        if data:
            res['data'] = data
        if kwargs:
            res.update(kwargs)
        super().__init__(data=res, status=status, template_name=template_name, headers=headers,
                         exception=exception, content_type=content_type)
