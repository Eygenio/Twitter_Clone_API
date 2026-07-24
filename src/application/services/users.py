import logging

from src.domain.unit_of_work import IUnitOfWork
from src.exceptions.exceptions import NotFoundError
from src.presentation.schemas.users import UserSchemaGet, UserSchemaInfo

logger = logging.getLogger(__name__)


class UsersService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def get_user_info(self, target_user_id: int) -> UserSchemaInfo:
        user = await self.uow.users.get_by_id(target_user_id)
        if not user:
            raise NotFoundError("User not found")

        followers = await self.uow.users.get_users_by_ids(
            [f.follower_id for f in (await self.uow.followers.get_by_followed(target_user_id))]
        )
        following = await self.uow.users.get_users_by_ids(
            [f.followed_id for f in (await self.uow.followers.get_by_follower(target_user_id))]
        )
        if user.id is None:
            raise ValueError("User id is not set")

        return UserSchemaInfo(
            id=user.id,
            name=user.name,
            followers=[UserSchemaGet(id=u.id, name=u.name) for u in followers],
            following=[UserSchemaGet(id=u.id, name=u.name) for u in following],
        )
