from src.models.likes import LikeOrm
from src.repositories.base import SQLAlchemyRepository


class LikeRepository(SQLAlchemyRepository[LikeOrm]):
    model = LikeOrm