import logging

from src.models.users import UserOrm
from src.repositories.followers import FollowerRepository
from src.repositories.users import UserRepository
from src.schemas.followers import FollowerSchema
from src.exceptions.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class FollowerService:
    """Сервис для управления подписками на пользователей."""
    def __init__(
            self,
            follower_repositories: FollowerRepository,
            user_repositories: UserRepository
    ):
        # инициализация сервиса с репозиториями подписок и пользователей.
        self.follower_repositories = follower_repositories
        self.user_repositories = user_repositories

    async def subscribe(self, user_id: int, user: UserOrm) -> FollowerSchema:
        """Подписка текущего пользователя user на пользователя по id."""
        logger.info(f"User {user.id} trying to subscribe to {user_id}")

        find_user = await self.user_repositories.find_one(user_id)
        if not find_user:
            raise NotFoundError("User not found to subscribe")

        await self.follower_repositories.add_one_no_return(
            {
                "followed_id": user_id,
                "follower_id": user.id
            }
        )

        logger.info(f"User {user.id} subscribe to {user_id}")
        return FollowerSchema(result=True)

    async def unsubscribe(self, user_id: int, user:UserOrm) -> FollowerSchema:
        """Отписка текущего пользователя user от пользователя по id."""
        logger.info(f"User {user.id} trying to unsubscribe at {user_id}")

        find_user = await self.user_repositories.find_one(user_id)
        if not find_user:
            raise NotFoundError(f"User not found to unsubscribe")

        await self.follower_repositories.delete_one_no_return(
            {
                "followed_id": user_id,
                "follower_id": user.id
            }
        )

        logger.info(f"User {user.id} unsubscribe at user {user_id}")
        return FollowerSchema(result=True)
