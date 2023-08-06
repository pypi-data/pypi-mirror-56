from rest_framework.exceptions import _get_error_details

from giz_exceptions.paas.exceptions import BusinessException


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