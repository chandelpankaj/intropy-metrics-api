class AppException(Exception):
    def __init__(self, message: str, code: str = "app_error", status_code: int = 400, details: dict = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message="Resource not found", details=None):
        super().__init__(message, code="not_found", status_code=404, details=details)
