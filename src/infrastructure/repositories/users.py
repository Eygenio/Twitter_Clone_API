from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User
from src.domain.repositories import IUserRepository
from src.infrastructure.models import UserOrm


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(orm: UserOrm) -> User:
        return User(
            id=orm.id,
            name=orm.name,
            api_key=orm.api_key,
        )

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.get(UserOrm, user_id)
        return self._to_domain(result) if result else None

    async def get_by_api_key(self, api_key: str) -> User | None:
        statement = select(UserOrm).where(UserOrm.api_key == api_key)
        result = await self._session.execute(statement)
        orm_user = result.scalar_one_or_none()
        return self._to_domain(orm_user) if orm_user else None

    async def get_users_by_ids(self, user_ids: list[int]) -> Sequence[User]:
        statement = select(UserOrm).where(UserOrm.id.in_(user_ids))
        result = await self._session.execute(statement)
        return [self._to_domain(u) for u in result.scalars().all()]
