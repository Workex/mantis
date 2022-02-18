from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class UnauthorizedException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_401_UNAUTHORIZED,
        message=ErrorConstants.ErrorParaphrase.UNAUTHORIZED,
        error_type=ErrorConstants.ErrorParaphrase.UNAUTHORIZED,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
