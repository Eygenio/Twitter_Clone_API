from fastapi import APIRouter

from src.presentation.dependencies import CurrentUserDep, UsersServiceDep
from src.presentation.schemas.users import UserSchemaGetID

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserSchemaGetID)
async def get_me(
    user: CurrentUserDep,
    service: UsersServiceDep,
) -> UserSchemaGetID:
    if user.id is None:
        raise ValueError("User ID is not set")
    info = await service.get_user_info(user.id)
    return UserSchemaGetID(result=True, user=info)


@router.get("/{id}", response_model=UserSchemaGetID)
async def get_user_by_id(
    id: int,
    user: CurrentUserDep,
    service: UsersServiceDep,
) -> UserSchemaGetID:
    info = await service.get_user_info(id)
    return UserSchemaGetID(result=True, user=info)
