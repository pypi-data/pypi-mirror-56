from giz_exceptions.paas.exceptions import BusinessException


class GDCSExceptions(BusinessException):
    message = 'GDCS error'
    code = '020400'


class DeviceNotYetReport(GDCSExceptions):
    message = 'current device not yet reported'
    code = '020401'


class GDCSHadExpired(GDCSExceptions):
    message = 'the GDCS of current device is expired'
    code = '020402'


class GDCSOutOfStock(GDCSExceptions):
    message = 'the GDCS is out of stock'
    code = '020403'
