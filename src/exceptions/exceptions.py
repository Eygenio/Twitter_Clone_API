from fastapi import status


class AppExceptionError(Exception):
    error_type: str = "AppExceptionError"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppExceptionError):
    error_type = "NotFoundError"
    status_code = status.HTTP_404_NOT_FOUND


class PermissionDeniedError(AppExceptionError):
    error_type = "PermissionDeniedError"
    status_code = status.HTTP_403_FORBIDDEN


class AlreadyExistsError(AppExceptionError):
    error_type = "AlreadyExistError"
    status_code = status.HTTP_409_CONFLICT


class ValidationError(AppExceptionError):
    error_type = "ValidationError"
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
