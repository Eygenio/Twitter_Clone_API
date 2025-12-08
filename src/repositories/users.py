from src.models.users import UserOrm
from src.repositories.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserOrm]):
    model = UserOrm
