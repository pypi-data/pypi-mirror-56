from rest_framework import status


class GizwitsException(Exception):
    status = status.HTTP_400_BAD_REQUEST
    code = 'xxxxxx'
    old_code = None  # 兼容 gwapi 的错误码
    old_msg = None  # 兼容 gwapi 的错误信息
    message = 'Not specified'
    description = '机智云的错误大类'
    detail = None

    def __init__(self, detail=None, code=None, message=None) -> None:
        """

        :param code: 特殊情况下，需要修改 code
        :param message: 特殊情况下，需要修改 message
        :param detail: 错误的详细信息
        """
        self.detail = detail

        if code is not None:
            self.code = code

        if message is not None:
            self.message = message


class SystemException(GizwitsException):
    status = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = '00xxxx'
    description = '系统性错误，如依赖服务报错'


class DataException(GizwitsException):
    status = status.HTTP_400_BAD_REQUEST
    code = '01xxxx'
    description = '数据性错误'


class BusinessException(GizwitsException):
    status = status.HTTP_400_BAD_REQUEST
    code = '02xxxx'
    description = '业务性错误'
