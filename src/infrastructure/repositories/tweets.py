from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Tweet
from src.domain.repositories import ITweetRepository
from src.infrastructure.models.tweets import TweetOrm


class TweetRepository(ITweetRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(orm: TweetOrm) -> Tweet:
        return Tweet(
            id=orm.id,
            content=orm.content,
            author_id=orm.author_id,
            medias_id=orm.medias_id,
        )

    async def get_by_id(self, tweet_id: int) -> Tweet | None:
        result = await self._session.get(TweetOrm, tweet_id)
        return self._to_domain(result) if result else None

    async def get_all(self, offset: int, limit: int) -> Sequence[Tweet]:
        statement = select(TweetOrm).offset(offset).limit(limit).order_by(TweetOrm.id.desc())
        result = await self._session.execute(statement)
        return [self._to_domain(t) for t in result.scalars().all()]

    async def add(self, tweet: Tweet) -> Tweet:
        orm = TweetOrm(
            content=tweet.content,
            author_id=tweet.author_id,
            medias_id=tweet.medias_id,
        )
        self._session.add(orm)
        await self._session.flush()
        tweet.id = orm.id
        return tweet

    async def delete(self, tweet_id: int) -> None:
        orm = await self._session.get(TweetOrm, tweet_id)
        if orm:
            await self._session.delete(orm)
            await self._session.flush()
