from sqlalchemy import delete as sa_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Follower
from src.domain.repositories import IFollowerRepository
from src.infrastructure.models import FollowerOrm


class FollowerRepository(IFollowerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, follower: Follower) -> None:
        orm = FollowerOrm(
            followed_id=follower.followed_id,
            follower_id=follower.follower_id,
        )
        self._session.add(orm)
        await self._session.flush()

    async def delete(self, follower: Follower) -> None:
        statement = (
            sa_delete(FollowerOrm)
            .where(FollowerOrm.followed_id == follower.followed_id)
            .where(FollowerOrm.follower_id == follower.follower_id)
        )
        await self._session.execute(statement)
        await self._session.flush()

    async def get_by_followed(self, followed_id: int) -> list[Follower]:
        statement = select(FollowerOrm).where(FollowerOrm.followed_id == followed_id)
        result = await self._session.execute(statement)
        orm_followers = result.scalars().all()
        return [
            Follower(followed_id=f.followed_id, follower_id=f.follower_id) for f in orm_followers
        ]

    async def get_by_follower(self, follower_id: int) -> list[Follower]:
        statement = select(FollowerOrm).where(FollowerOrm.follower_id == follower_id)
        result = await self._session.execute(statement)
        orm_followers = result.scalars().all()
        return [
            Follower(followed_id=f.followed_id, follower_id=f.follower_id) for f in orm_followers
        ]
