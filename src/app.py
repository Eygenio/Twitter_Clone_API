from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging.config

from src.config.logging_config import LOGGING_CONFIG
from src.middleware.error_handler import app_exception_handler, global_exception_handler
from src.middleware.request_id import RequestIDMiddleware
from src.exceptions.exceptions import AppException
from src.config.base import Config
from src.db.db import create_tables
from src.routing.likes import likes_router
from src.routing.tweets import tweets_router
from src.routing.users import users_router
from src.routing.followers import followers_router
from src.routing.medias import medias_router

# конфигурация логирования приложения.
logging.config.dictConfig(LOGGING_CONFIG)

# создание основного приложения FastAPI
app = FastAPI(
    title="Twitter Clone API",
    version="1.0.0",
    description="Public API v1"
)

# создание таблиц базы данных при старте приложения.
@app.on_event("startup")
async def on_startup():
    await create_tables()

# добавления middleware для отслеживания запросов.
app.add_middleware(RequestIDMiddleware)

# регистрация обработчиков исключений.
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# подключение маршрутов API.
app.include_router(likes_router)
app.include_router(tweets_router)
app.include_router(users_router)
app.include_router(followers_router)
app.include_router(medias_router)

# создание директории media, если ее нет.
Config.MEDIA_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
