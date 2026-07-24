from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Media
from src.domain.repositories import IMediaRepository
from src.infrastructure.models import MediaOrm


class MediaRepository(IMediaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(orm: MediaOrm) -> Media:
        return Media(
            id=orm.id,
            path=orm.path,
        )

    async def add(self, media: Media) -> Media:
        orm = MediaOrm(path=media.path)
        self._session.add(orm)
        await self._session.flush()
        media.id = orm.id
        return media

    async def get_by_id(self, media_id: int) -> Media | None:
        result = await self._session.get(MediaOrm, media_id)
        return self._to_domain(result) if result else None

    async def delete(self, media_id: int) -> None:
        orm = await self._session.get(MediaOrm, media_id)
        if orm:
            await self._session.delete(orm)
            await self._session.flush()

    async def get_by_ids(self, media_ids: list[int]) -> list[Media]:
        if not media_ids:
            return []
        statement = select(MediaOrm).where(MediaOrm.id.in_(media_ids))
        result = await self._session.execute(statement)
        return [self._to_domain(m) for m in result.scalars().all()]
