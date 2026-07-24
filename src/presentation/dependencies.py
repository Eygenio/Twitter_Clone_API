from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from src.application.services.followers import FollowerService
from src.application.services.likes import LikeService
from src.application.services.medias import MediaService
from src.application.services.tweets import TweetsService
from src.application.services.users import UsersService
from src.db.db import async_session_maker
from src.domain.entities import User
from src.domain.unit_of_work import IUnitOfWork
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork


async def get_uow() -> AsyncGenerator[IUnitOfWork]:
    session = async_session_maker()
    uow = SQLAlchemyUnitOfWork(session)
    try:
        yield uow
        await uow.commit()
    except Exception:
        await uow.rollback()
        raise
    finally:
        await session.close()


async def get_current_user(
    api_key: str | None = Header(None),
    uow: IUnitOfWork = Depends(get_uow),
) -> User:
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key header required",
        )
    user = await uow.users.get_by_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return user


def get_follower_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> FollowerService:
    return FollowerService(uow)


def get_like_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> LikeService:
    return LikeService(uow)


def get_tweet_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> TweetsService:
    return TweetsService(uow)


def get_user_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> UsersService:
    return UsersService(uow)


def get_media_service(
    uow: IUnitOfWork = Depends(get_uow),
) -> MediaService:
    return MediaService(uow)


FollowerServiceDep = Annotated[FollowerService, Depends(get_follower_service)]
LikeServiceDep = Annotated[LikeService, Depends(get_like_service)]
TweetsServiceDep = Annotated[TweetsService, Depends(get_tweet_service)]
UsersServiceDep = Annotated[UsersService, Depends(get_user_service)]
MediaServiceDep = Annotated[MediaService, Depends(get_media_service)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
