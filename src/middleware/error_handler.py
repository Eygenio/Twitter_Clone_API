import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import AppExceptionError

logger = logging.getLogger("src")


async def app_exception_handler(
    request: Request,
    exc: AppExceptionError,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.error("[%s] %s: %s", request_id, exc.error_type, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.error_type,
            "error_message": exc.message,
            "request_id": request_id,
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None)
    logger.exception("[%s] Unhandled error: %s", request_id, exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "result": False,
            "error_type": "InternalServerError",
            "error_message": "Unexpected server error",
            "request_id": request_id,
        },
    )
