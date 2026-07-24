from fastapi import APIRouter

from src.presentation.dependencies import CurrentUserDep, FollowerServiceDep
from src.presentation.schemas.followers import FollowerSchema

router = APIRouter(prefix="/api/users", tags=["followers"])


@router.post("/{id}/follow")
async def follow_user(
    id: int,
    user: CurrentUserDep,
    service: FollowerServiceDep,
) -> FollowerSchema:
    await service.subscribe(id, user)
    return FollowerSchema(result=True)


@router.delete("/{id}/follow")
async def unfollow_user(
    id: int,
    user: CurrentUserDep,
    service: FollowerServiceDep,
) -> FollowerSchema:
    await service.unsubscribe(id, user)
    return FollowerSchema(result=True)
