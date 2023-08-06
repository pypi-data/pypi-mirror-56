from rest_framework.response import Response
from rest_framework.views import exception_handler

from .paas.exceptions.base import GizwitsException


def log(context, **kwargs):
    request = context.get('request')
    if request and hasattr(request, 'biz_log'):
        request.biz_log.update(kwargs)


def custom_handler(exc, context):
    """

    异常的处理优先级：
    1. 优先处理自定义异常
    2. 非自定义异常，交由

    :param exc: 异常对象
    :param context: 字典，包含：view、args、kwargs、request
    :return:
    """

    if not isinstance(exc, GizwitsException):

        response = exception_handler(exc, context)

        if response:
            return response

        return

    data = {
        'error_code': exc.old_code or exc.code,
        'error_message': exc.old_msg or exc.message,
        'detail_message': exc.detail,
    }

    log(context, http_status=exc.status, **data)

    return Response(data, status=exc.status)
