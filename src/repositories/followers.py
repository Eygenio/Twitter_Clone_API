from src.models.followers import FollowerOrm
from src.repositories.base import SQLAlchemyRepository


class FollowerRepository(SQLAlchemyRepository[FollowerOrm]):
    model = FollowerOrm