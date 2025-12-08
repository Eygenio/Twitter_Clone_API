from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.repositories.likes import LikeRepository
from src.repositories.tweets import TweetRepository
from src.repositories.users import UserRepository
from src.models.users import UserOrm
from src.services.likes import LikeService
from src.schemas.likes import LikeSchema
from src.db.db import get_async_session

router = APIRouter()

likes_router = router


# зависимости для создания сервиса 'Лайков'.
def like_service(session: AsyncSession = Depends(get_async_session)):
    return LikeService(LikeRepository(session), UserRepository(session), TweetRepository(session))


@router.post("/api/tweets/{id}/likes",
             response_model=LikeSchema,
             tags=["Like"],
             summary="Поставить 'Лайк' 'Твиту'.",
             description="Добавление 'Лайка' 'Твиту' с указанным ID."
             )
async def give_like(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: LikeService = Depends(like_service)
):
    return await service.give_like(id, user)


@router.delete("/api/tweets/{id}/likes",
               response_model=LikeSchema,
               tags=["Like"],
               summary="Убрать 'Лайк' 'Твиту'.",
               description="Удаление 'Лайка' у 'Твита' с указанным ID."
               )
async def remove_like(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: LikeService = Depends(like_service),
):
    return await service.remove_like(id, user)
