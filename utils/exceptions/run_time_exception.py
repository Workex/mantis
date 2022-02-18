from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class RunTimeException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
        message=ErrorConstants.ErrorParaphrase.RUNTIME_ERROR,
        error_type=ErrorConstants.RUNTIME_ERROR,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
