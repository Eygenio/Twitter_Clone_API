import logging

from src.domain.entities import Tweet, User
from src.domain.unit_of_work import IUnitOfWork
from src.exceptions.exceptions import NotFoundError, PermissionDeniedError
from src.presentation.schemas.likes import LikeSchemaGet
from src.presentation.schemas.tweets import TweetSchemaGet, TweetSchemaGetAll
from src.presentation.schemas.users import UserSchemaGet

logger = logging.getLogger(__name__)


class TweetsService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_tweet(
        self,
        user: User,
        tweet_data: str,
        media_ids: list[int] | None = None,
    ) -> Tweet:
        if user.id is None:
            raise ValueError("User ID is not set")
        tweet = Tweet(
            content=tweet_data,
            author_id=user.id,
            medias_id=media_ids or [],
        )
        tweet = await self.uow.tweets.add(tweet)
        logger.info("Tweet %s created by user %s", tweet.id, user.id)
        return tweet

    async def get_tweets(self, offset: int, limit: int) -> list[Tweet]:
        return list(await self.uow.tweets.get_all(offset, limit))

    async def delete_tweet(self, tweet_id: int, user: User) -> None:
        tweet = await self.uow.tweets.get_by_id(tweet_id)
        if not tweet:
            raise NotFoundError("Tweet not found")
        if tweet.author_id != user.id:
            raise PermissionDeniedError("You cannot delete another user tweet")
        await self.uow.tweets.delete(tweet_id)
        logger.info("Tweet %s deleted by user %s", tweet_id, user.id)

    async def get_tweets_full(self, offset: int, limit: int) -> TweetSchemaGetAll:
        tweets = await self.uow.tweets.get_all(offset, limit)
        result_tweets: list[TweetSchemaGet] = []

        for tweet in tweets:
            author = await self.uow.users.get_by_id(tweet.author_id)
            author_schema = UserSchemaGet(id=author.id, name=author.name) if author else None

            if tweet.id is None:
                raise ValueError("Tweet ID is not set")
            likes = await self.uow.likes.get_by_tweet_id(tweet.id)
            likes_schema = [
                LikeSchemaGet(user_id=like.author_id, name=like.author_name) for like in likes
            ]

            attachments: list[str] = []
            if tweet.medias_id:
                medias = await self.uow.media.get_by_ids(tweet.medias_id)
                attachments = [media.path for media in medias]

            result_tweets.append(
                TweetSchemaGet(
                    id=tweet.id,
                    content=tweet.content,
                    attachments=attachments,
                    author=author_schema,
                    likes=likes_schema,
                )
            )
        return TweetSchemaGetAll(result=True, tweets=result_tweets)
