import logging
from src.repositories.users import UserRepository
from src.schemas.users import UserSchemaInfo, UserSchemaGetID
from src.models.users import UserOrm
from src.exceptions.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class UsersService:
    """Сервис для управления пользователями."""
    def __init__(self, repositories: UserRepository):
        # инициализация сервиса с репозиторием пользователей.
        self.repositories = repositories

    async def get_user_by_id(self, user_id: int, user: UserOrm) -> UserSchemaGetID:
        """Получение информации о пользователе по user_id с его подписками и его фолловерами."""
        logger.info(f"User {user.id} trying receive info by user {user_id}")

        user = await self.repositories.find_one(
            user_id,
            relations=[UserOrm.followers, UserOrm.following]
        )

        if not user:
            raise NotFoundError("User not found")

        followers_id = [follower.follower_id for follower in user.followers]
        followers = await self.repositories.get_user_by_list(followers_id)

        following_id = [following.followed_id for following in user.following]
        following = await self.repositories.get_user_by_list(following_id)

        info = UserSchemaInfo(
            id=user.id,
            name=user.name,
            followers=followers,
            following=following
        )

        logger.info(f"User {user.id} receive info by user {user_id}")
        return UserSchemaGetID(result=True, user=info)
