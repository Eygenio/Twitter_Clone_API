from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.repositories.followers import FollowerRepository
from src.models.users import UserOrm
from src.schemas.followers import FollowerSchema
from src.services.followers import FollowerService
from src.repositories.users import UserRepository
from src.db.db import get_async_session

router = APIRouter()

followers_router = router


# зависимости для создания сервиса 'Фолловеров'.
def follower_service(session: AsyncSession = Depends(get_async_session)):
    return FollowerService(FollowerRepository(session), UserRepository(session))


@router.post("/api/users/{id}/follow",
             response_model=FollowerSchema,
             tags=["Follower"],
             summary="Подписаться на пользователя",
             description="Подписаться на пользователя с указанным ID."
             )
async def subscribe(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: FollowerService = Depends(follower_service)
):
    return await service.subscribe(id, user)


@router.delete("/api/users/{id}/follow",
               response_model=FollowerSchema,
               tags=["Follower"],
               summary="Отписаться от пользователя",
               description="Отписаться от пользователя с указанным ID."
               )
async def unsubscribe(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: FollowerService = Depends(follower_service)
):
    return await service.unsubscribe(id, user)
