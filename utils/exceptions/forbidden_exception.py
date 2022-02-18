from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class ForbiddenException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_403_FORBIDDEN,
        message=ErrorConstants.ErrorParaphrase.FORBIDDEN,
        error_type=ErrorConstants.ErrorParaphrase.FORBIDDEN,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
