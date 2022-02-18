from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class NotFoundException(WxBaseException):
    def __init__(
            self,
            status=status.HTTP_404_NOT_FOUND,
            message=ErrorConstants.ErrorParaphrase.NOT_FOUND,
            error_type=ErrorConstants.NOT_FOUND,
            http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
