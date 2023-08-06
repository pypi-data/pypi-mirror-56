from giz_exceptions.paas.exceptions import BusinessException


class GDCSExceptions(BusinessException):
    msg = 'GDCS error'
    code = '020400'


class DeviceNotYetReport(GDCSExceptions):
    msg = 'current device not yet reported'
    code = '020401'


class GDCSHadExpired(GDCSExceptions):
    msg = 'the GDCS of current device is expired'
    code = '020402'


class GDCSOutOfStock(GDCSExceptions):
    msg = 'the GDCS is out of stock'
    code = '020403'
