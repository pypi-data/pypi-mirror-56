from rest_framework.exceptions import _get_error_details

from .base import BusinessException


class SerializerValidationError(BusinessException):
    old_code = 9015
    old_msg = 'form_invalid'

    message = 'Form invalid'
    code = '020001'

    def __init__(self, detail=None):

        if isinstance(detail, dict):
            self.detail = _get_error_details(detail, 'invalid')

        if isinstance(detail, str):
            self.detail = detail


class DeviceRegisterLimit(BusinessException):
    old_code = 9055
    code = '020103'
    message = 'Devices count has reached the limit of product,' \
              ' please contact sellers!'


class SlaveDeviceBidingLimit(BusinessException):
    message = 'Slave device can no more bind to current central control device'
    code = '020104'


class DeviceUpdateFailed(BusinessException):
    message = 'Device update failed'
    code = '020105'


class DeviceResetFailed(BusinessException):
    message = 'Device reset failed'
    code = '020106'


class DeviceCreateFailed(BusinessException):
    message = 'Device create failed'
    code = '020107'


class DeviceAssociateFailed(BusinessException):
    message = 'Device associate failed'
    code = '020108'


class ProductKeyInvalid(BusinessException):
    old_code = 9002
    old_msg = 'product_key invalid!'

    message = 'Product key invalid'
    code = '020201'


class ProductTypeError(BusinessException):
    message = 'Product type error'
    code = '020202'


class ProductConfigError(BusinessException):
    message = 'Product configuration error'
    code = '020203'


class ProductPreAssignmentFailed(BusinessException):
    message = 'Product pre-assignment failed'
    code = '020204'


class PreAuthFailed(BusinessException):
    message = 'check pre auth failed'
    code = '020301'


class GDCSExceptions(BusinessException):
    msg = 'GDCS error'
    code = '020400'


class DeviceNotYetReport(GDCSExceptions):
    msg = 'current device not yet reported'
    code = '020401'


class GDCSHadExpired(GDCSExceptions):
    msg = 'the GDCS of current device is expired'
    code = '020402'
