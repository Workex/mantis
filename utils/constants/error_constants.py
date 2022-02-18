class ErrorConstants:
    BAD_REQUEST = "BAD_REQUEST"
    NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    NOT_FOUND = "NOT_FOUND"
    NOT_MODIFIED = "NOT_MODIFIED"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    FORBIDDEN = "FORBIDDEN"

    class ErrorParaphrase:
        BAD_REQUEST = "Bad request"
        NOT_ALLOWED = "Method not Allowed"
        NOT_FOUND = "Entity not found"
        NOT_MODIFIED = "Record not modified"
        UNPROCESSABLE_ENTITY = (
            "Validation Error, request body is not proper as type defined"
        )
        UNAUTHORIZED = "Not authorized"
        RUNTIME_ERROR = "Run Time Error!!"
        FORBIDDEN = "FORBIDDEN"
