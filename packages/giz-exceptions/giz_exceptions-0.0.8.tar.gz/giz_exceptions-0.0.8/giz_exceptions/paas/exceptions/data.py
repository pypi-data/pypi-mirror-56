from rest_framework import status

from .base import DataException


class DeviceNotFound(DataException):
    status = status.HTTP_404_NOT_FOUND

    old_code = 9014
    old_msg = 'device not found!'

    message = 'Device not found'
    code = '010101'


class DeviceDisabled(DataException):
    old_code = 9023
    old_msg = 'device is disabled!'

    message = 'Device is disabled'
    code = '010102'


class ProductNotFound(DataException):
    status = status.HTTP_404_NOT_FOUND
    message = 'Product not found'
    code = '010201'


class ProductProvisionDoesNotExists(DataException):
    message = 'Product provision does not exists'
    code = '010202'


class ProductMultipleRecord(DataException):
    message = 'Multiple product found'
    code = '010203'
