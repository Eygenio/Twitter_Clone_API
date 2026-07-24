import logging

from src.domain.entities import Follower, User
from src.domain.unit_of_work import IUnitOfWork
from src.exceptions.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class FollowerService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def subscribe(self, target_user_id: int, current_user: User) -> None:
        target = await self.uow.users.get_by_id(target_user_id)
        if not target:
            raise NotFoundError("User not found to subscribe")

        follower = Follower(followed_id=target_user_id, follower_id=current_user.id)
        await self.uow.followers.add(follower)
        logger.info("User %s subscribed to %s", current_user.id, target_user_id)

    async def unsubscribe(self, target_user_id: int, current_user: User) -> None:
        target = await self.uow.users.get_by_id(target_user_id)
        if not target:
            raise NotFoundError("User not found to unsubscribe")

        follower = Follower(followed_id=target_user_id, follower_id=current_user.id)
        await self.uow.followers.delete(follower)
        logger.info("User %s unsubscribed from %s", current_user.id, target_user_id)
