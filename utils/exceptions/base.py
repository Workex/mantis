class WxBaseException(Exception):
    status: int
    http_status: int
    message: str
    error_type: str
    meta: dict

    def __init__(
            self,
            status: int,
            message: str,
            error_type: str,
            meta: dict = dict,
            http_status=None,
    ):
        self.status = status
        self.message = message
        self.error_type = error_type
        self.http_status = http_status
        if meta:
            self.meta = meta

    def __str__(self):
        return f"[{self.status}]<{self.error_type}>\t{self.message}"
