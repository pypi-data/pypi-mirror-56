from giz_exceptions.paas.exceptions import BusinessException


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
