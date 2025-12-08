from src.models.tweets import TweetOrm
from src.repositories.base import SQLAlchemyRepository


class TweetRepository(SQLAlchemyRepository[TweetOrm]):
    model = TweetOrm
