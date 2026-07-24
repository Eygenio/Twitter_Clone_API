from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import async_session_maker
from src.infrastructure.repositories.followers import FollowerRepository
from src.infrastructure.repositories.likes import LikeRepository
from src.infrastructure.repositories.medias import MediaRepository
from src.infrastructure.repositories.tweets import TweetRepository
from src.infrastructure.repositories.users import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def users(self) -> UserRepository:
        return UserRepository(self._session)

    @property
    def tweets(self) -> TweetRepository:
        return TweetRepository(self._session)

    @property
    def likes(self) -> LikeRepository:
        return LikeRepository(self._session)

    @property
    def media(self) -> MediaRepository:
        return MediaRepository(self._session)

    @property
    def followers(self) -> FollowerRepository:
        return FollowerRepository(self._session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()


@asynccontextmanager
async def get_uow() -> AsyncIterator[UnitOfWork]:
    async with async_session_maker() as session:
        uow = UnitOfWork(session)
        try:
            yield uow
            await uow.commit()
        except Exception:
            await uow.rollback()
            raise
        finally:
            await uow.close()
