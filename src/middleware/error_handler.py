import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from src.exceptions.exceptions import AppException

logger = logging.getLogger("src")


async def app_exception_handler(request: Request, exc: AppException):
    request_id = getattr(request.state, "request_id", None)

    logger.error(f"[{request_id}] {exc.error_type}: {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": False,
            "error_type": exc.error_type,
            "error_message": exc.message,
            "request_id": request_id
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)

    logger.exception(f"[{request_id}] Unhandled error: {exc} ")

    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": "InternalServerError",
            "error_message": "Unexpected server error",
            "request_id": request_id
        }
    )
