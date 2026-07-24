from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Like
from src.domain.repositories import ILikeRepository
from src.infrastructure.models import LikeOrm


class LikeRepository(ILikeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(orm: LikeOrm) -> Like:
        return Like(
            id=orm.id,
            tweet_id=orm.tweet_id,
            author_id=orm.author_id,
            author_name=orm.author_name,
        )

    async def add(self, like: Like) -> Like:
        orm = LikeOrm(
            tweet_id=like.tweet_id,
            author_id=like.author_id,
            author_name=like.author_name,
        )
        self._session.add(orm)
        await self._session.flush()
        like.id = orm.id
        return like

    async def delete(self, like_id: int) -> None:
        orm = await self._session.get(LikeOrm, like_id)
        if orm:
            await self._session.delete(orm)
            await self._session.flush()

    async def get_by_tweet_and_user(
        self,
        tweet_id: int,
        user_id: int,
    ) -> Like | None:
        statement = select(LikeOrm).where(
            LikeOrm.tweet_id == tweet_id,
            LikeOrm.author_id == user_id,
        )
        result = await self._session.execute(statement)
        orm_like = result.scalar_one_or_none()
        return self._to_domain(orm_like) if orm_like else None

    async def get_by_tweet_id(self, tweet_id: int) -> list[Like]:
        statement = select(LikeOrm).where(LikeOrm.tweet_id == tweet_id)
        result = await self._session.execute(statement)
        return [self._to_domain(like) for like in result.scalars().all()]
