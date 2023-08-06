from giz_exceptions.paas.exceptions import BusinessException


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
