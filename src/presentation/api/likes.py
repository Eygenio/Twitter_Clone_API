from fastapi import APIRouter

from src.presentation.dependencies import CurrentUserDep, LikeServiceDep
from src.presentation.schemas.likes import LikeSchema

router = APIRouter(prefix="/api/tweets", tags=["likes"])


@router.post("/{id}/likes", response_model=LikeSchema)
async def give_like(
    id: int,
    user: CurrentUserDep,
    service: LikeServiceDep,
) -> LikeSchema:
    await service.give_like(id, user)
    return LikeSchema(result=True)


@router.delete("/{id}/likes", response_model=LikeSchema)
async def remove_like(
    id: int,
    user: CurrentUserDep,
    service: LikeServiceDep,
) -> LikeSchema:
    await service.remove_like(id, user)
    return LikeSchema(result=True)
