import logging

from src.domain.entities import Like, User
from src.domain.unit_of_work import IUnitOfWork
from src.exceptions.exceptions import NotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)


class LikeService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def give_like(self, tweet_id: int, user: User) -> Like:
        tweet = await self.uow.tweets.get_by_id(tweet_id)
        if not tweet:
            raise NotFoundError("Tweet not found")
        if user.id is None:
            raise ValueError("User ID is not set")
        existing = await self.uow.likes.get_by_tweet_and_user(tweet_id, user.id)
        if existing:
            raise PermissionDeniedError("You already liked this tweet")

        like = Like(
            tweet_id=tweet_id,
            author_id=user.id,
            author_name=user.name,
        )
        like = await self.uow.likes.add(like)
        logger.info("User %s liked tweet %s", user.id, tweet_id)
        return like

    async def remove_like(self, tweet_id: int, user: User) -> None:
        if user.id is None:
            raise ValueError("User ID is not set")
        like = await self.uow.likes.get_by_tweet_and_user(tweet_id, user.id)
        if not like:
            raise NotFoundError("Like not found")
        if like.author_id != user.id:
            raise PermissionDeniedError("You cannot remove another user like")
        if like.id is None:
            raise ValueError("Like ID is not set")
        await self.uow.likes.delete(like.id)
        logger.info("User %s removed like from tweet %s", user.id, tweet_id)
