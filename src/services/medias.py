import logging
import uuid
import aiofiles
from pathlib import Path

from src.models.users import UserOrm
from src.repositories.medias import MediaRepository
from src.schemas.medias import MediaSchemaAdd
from src.config.base import Config
from src.exceptions.exceptions import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class MediaService:
    """Сервис для управления медиафайлами."""
    def __init__(self, media_repositories: MediaRepository):
        # инициализация сервиса с репозиторием медиа и пути директории.
        self.media_repositories = media_repositories
        self.media_dir = Config.MEDIA_DIR

    async def save_media(self, file, user: UserOrm) -> MediaSchemaAdd:
        """Сохранение медиафайла на сервере и путь в базе данных."""
        logger.info(f"User {user.id} trying to upload media")

        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        file_path = self.media_dir / filename

        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(await file.read())

        url_path = f"/media/{filename}"

        media_id = await self.media_repositories.add_one({"path": url_path})
        if not media_id:
            raise AlreadyExistsError("Media did not load")

        media = await self.media_repositories.find_one(media_id)
        if not media:
            raise NotFoundError("Media not found")

        logger.info(f"User {user.id} upload media {media_id}")
        return MediaSchemaAdd(result=True, media_id=media_id)
