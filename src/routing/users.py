from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.models.users import UserOrm
from src.schemas.users import UserSchemaGetID
from src.services.users import UsersService
from src.repositories.users import UserRepository
from src.db.db import get_async_session

router = APIRouter()

users_router = router


# зависимость для создания сервиса пользователей.
def get_user_service(session: AsyncSession = Depends(get_async_session)):
    return UsersService(UserRepository(session))


@router.get("/api/users/me",
            response_model=UserSchemaGetID,
            tags=["User"],
            summary="Получение информации о текущем пользователе",
            description="Возвращает информацию о текущем пользователе, соответствующую API-ключу"
            )
async def get_me(
        user: UserOrm = Depends(get_current_user),
        service: UsersService = Depends(get_user_service)
):
    return await service.get_user_by_id(user.id, user)


@router.get("/api/users/{id}",
            response_model=UserSchemaGetID,
            tags=["User"],
            summary="Получение информации о текущем пользователе по ID",
            description="Возвращает информацию о текущем пользователе с указанным ID."
            )
async def get_user_by_id(
        id: int,
        user: UserOrm = Depends(get_current_user),
        service: UsersService = Depends(get_user_service)
):
    return await service.get_user_by_id(id, user)
