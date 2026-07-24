import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.config.logging_config import LOGGING_CONFIG
from src.config.settings import settings
from src.db.db import create_tables
from src.exceptions.exceptions import AppExceptionError
from src.middleware.error_handler import app_exception_handler, global_exception_handler
from src.middleware.request_id import RequestIDMiddleware
from src.presentation.api.followers import router as followers_router
from src.presentation.api.likes import router as likes_router
from src.presentation.api.medias import router as medias_router
from src.presentation.api.tweets import router as tweets_router
from src.presentation.api.users import router as users_router

logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await create_tables()
    settings.media_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title=settings.app.title,
    version=settings.app.version,
    description=settings.app.description,
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(AppExceptionError, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(likes_router)
app.include_router(tweets_router)
app.include_router(users_router)
app.include_router(followers_router)
app.include_router(medias_router)

settings.media_dir.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
