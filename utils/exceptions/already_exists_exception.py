from rest_framework import status

from .base import WxBaseException
from utils.constants import ErrorConstants


class AlreadyExistsException(WxBaseException):
    def __init__(
        self,
        status=status.HTTP_409_CONFLICT,
        message=ErrorConstants.ErrorParaphrase.BAD_REQUEST,
        error_type=ErrorConstants.BAD_REQUEST,
        http_status=None,
    ):
        super().__init__(
            status=status,
            message=message,
            error_type=error_type,
            http_status=http_status,
        )
