from src.models.medias import MediaOrm
from src.repositories.base import SQLAlchemyRepository


class MediaRepository(SQLAlchemyRepository[MediaOrm]):
    model = MediaOrm