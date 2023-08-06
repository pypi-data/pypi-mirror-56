from .base import SystemException


class ServiceInternalError(SystemException):
    message = 'Service internal processing exception'
    description = '服务内部处理异常'
    code = '000007'



