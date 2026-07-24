import logging
import uuid
from pathlib import Path

import aiofiles  # type: ignore[import-untyped]
from fastapi import UploadFile

from src.config.settings import settings
from src.domain.entities import Media
from src.domain.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)


class MediaService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def save_media(self, file: UploadFile) -> Media:
        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        file_path = settings.media_dir / filename

        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(await file.read())

        url_path = f"/media/{filename}"
        media = Media(path=url_path)
        media = await self.uow.media.add(media)

        logger.info("Media %s uploaded", media.id)
        return media
