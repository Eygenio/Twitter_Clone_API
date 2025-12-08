from fastapi import status


class AppException(Exception):
    """Базовый класс для ошибок серверного уровня."""
    error_type: str = "AppException"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppException):
    error_type = "NotFoundError"
    status_code = status.HTTP_404_NOT_FOUND


class PermissionDeniedError(AppException):
    error_type = "PermissionDeniedError"
    status_code = status.HTTP_403_FORBIDDEN


class AlreadyExistsError(AppException):
    error_type = "AlreadyExistError"
    status_code = status.HTTP_409_CONFLICT


class ValidationError(AppException):
    error_type = "ValidationError"
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
