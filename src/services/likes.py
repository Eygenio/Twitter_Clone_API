import logging
from src.repositories.likes import LikeRepository
from src.repositories.users import UserRepository
from src.repositories.tweets import TweetRepository
from src.schemas.likes import LikeSchema
from src.models.users import UserOrm
from src.models.tweets import TweetOrm
from src.exceptions.exceptions import NotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)


class LikeService:
    """Сервис для управления 'Лайками' 'Твитов'."""
    def __init__(
            self,
            like_repositories: LikeRepository,
            user_repositories: UserRepository,
            tweet_repositories: TweetRepository
    ):
        # инициализация сервиса с репозиториями 'Лайков', пользователей и 'Твитов'.
        self.like_repositories = like_repositories
        self.user_repositories = user_repositories
        self.tweet_repositories = tweet_repositories

    async def give_like(self, tweet_id: int, user: UserOrm) -> LikeSchema:
        """Добавить 'Лайк' от текущего пользователя user 'Твиту' по id."""
        logger.info(f"User {user.id} trying to give a like tweet {tweet_id}")

        find_tweet = await self.tweet_repositories.find_one(tweet_id)
        if not find_tweet:
            raise NotFoundError("Tweet not found")

        await self.like_repositories.add_one_no_return({
            "tweet_id": tweet_id,
            "author_id": user.id,
            "author_name": user.name
        })

        logger.info(f"User {user.id} give a like tweet {tweet_id}")
        return LikeSchema(result=True)

    async def remove_like(self, tweet_id: int, user: UserOrm) -> LikeSchema:
        """Удаление 'Лайка' от текущего пользователя user 'Твиту' по id."""
        logger.info(f"User {user.id} trying to remove like at tweet {tweet_id}")

        tweet = await self.tweet_repositories.find_one(
            data_id=tweet_id,
            relations=[TweetOrm.likes,]
        )

        if not tweet:
            raise NotFoundError("Tweet not found")

        for like in tweet.likes:
            if like.author_id == user.id:
                await self.like_repositories.delete_one_by_id(like.id)
                return LikeSchema(result=True)

        raise PermissionDeniedError("You cannot remove another user like")
