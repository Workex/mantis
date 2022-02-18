from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class NotAllowedException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
        message=ErrorConstants.ErrorParaphrase.NOT_ALLOWED,
        error_type=ErrorConstants.NOT_ALLOWED,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
