from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.models.users import UserOrm
from src.schemas.tweets import TweetSchemaAdd, TweetSchemasCreate, TweetSchemaGetAll, TweetSchemaDelete
from src.services.tweets import TweetsService
from src.repositories.tweets import TweetRepository
from src.repositories.users import UserRepository
from src.repositories.medias import MediaRepository
from src.db.db import get_async_session

router = APIRouter()

tweets_router = router


# зависимости для создания сервиса 'Твитов'.
def tweet_service(session: AsyncSession = Depends(get_async_session)):
    return TweetsService(TweetRepository(session), UserRepository(session), MediaRepository(session))


@router.post("/api/tweets",
             response_model=TweetSchemaAdd,
             tags=["Tweet"],
             summary="Добавление 'Твита'.",
             description="Создание нового 'Твита' с возможностью прикрепления медиафайла."
             )
async def add_tweet(
        payload: TweetSchemasCreate,
        user: UserOrm = Depends(get_current_user),
        service: TweetsService = Depends(tweet_service)
):
    return await service.add_tweet(user, payload)


@router.get("/api/tweets",
            response_model=TweetSchemaGetAll,
            tags=["Tweet"],
            summary="Получение списка всех 'Твитов'.",
            description="Возвращает список всех 'Твитов' с информацией о лайках и медиафайлах,"
                        " возможно использовать пагинацию. "
            )
async def get_tweets(
        user: UserOrm = Depends(get_current_user),
        service: TweetsService = Depends(tweet_service),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1)
):
    return await service.get_tweets(user, offset, limit)


@router.delete("/api/tweets/{id}",
               response_model=TweetSchemaDelete,
               tags=["Tweet"],
               summary="Удаление 'Твита' по ID",
               description="Удаление 'Твита' по его ID, также удаляет медиафайлы, информацию о 'Лайках'."
                           "Доступно только автору 'Твита'."
               )
async def delete_tweet(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: TweetsService = Depends(tweet_service)
):
    return await service.delete_tweet(id, user)
