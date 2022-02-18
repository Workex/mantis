from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class ValidationException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=ErrorConstants.ErrorParaphrase.UNPROCESSABLE_ENTITY,
        error_type=ErrorConstants.ErrorParaphrase.UNPROCESSABLE_ENTITY,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
