from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.unit_of_work import IUnitOfWork
from src.infrastructure.repositories.followers import FollowerRepository
from src.infrastructure.repositories.likes import LikeRepository
from src.infrastructure.repositories.medias import MediaRepository
from src.infrastructure.repositories.tweets import TweetRepository
from src.infrastructure.repositories.users import UserRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = UserRepository(session)
        self.tweets = TweetRepository(session)
        self.likes = LikeRepository(session)
        self.followers = FollowerRepository(session)
        self.media = MediaRepository(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
