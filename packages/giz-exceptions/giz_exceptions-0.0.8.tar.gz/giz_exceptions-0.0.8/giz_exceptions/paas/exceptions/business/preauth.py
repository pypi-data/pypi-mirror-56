from giz_exceptions.paas.exceptions import BusinessException


class PreAuthFailed(BusinessException):
    message = 'check pre auth failed'
    code = '020301'
