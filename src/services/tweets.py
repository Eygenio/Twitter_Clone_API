import logging
from pathlib import Path
from typing import List
import aiofiles.os as aios

from src.config.base import Config
from src.models.users import UserOrm
from src.repositories.tweets import TweetRepository
from src.repositories.users import UserRepository
from src.repositories.medias import MediaRepository
from src.schemas.likes import LikeSchemaGet
from src.schemas.tweets import (TweetSchemasCreate,
                                TweetSchemaAdd,
                                TweetSchemaGet,
                                TweetSchemaGetAll,
                                TweetSchemaDelete)
from src.schemas.users import UserSchemaGet
from src.models.tweets import TweetOrm
from src.exceptions.exceptions import NotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)


class TweetsService:
    """Сервис для управления 'Твитами'."""
    def __init__(
            self,
            tweet_repositories: TweetRepository,
            user_repositories: UserRepository,
            media_repositories: MediaRepository
    ):
        # инициализация сервиса с репозиториями 'Твитов', пользователей и медиафайлами.
        self.tweet_repositories = tweet_repositories
        self.user_repositories = user_repositories
        self.media_repositories = media_repositories

    async def add_tweet(self, user: UserOrm, data: TweetSchemasCreate) -> TweetSchemaAdd:
        """Добавления нового 'Твита' от пользователя user с возможностью добавления медиафайлов."""
        logger.info(f"User {user.id} trying to add tweet")

        tweet_id = await self.tweet_repositories.add_one({
            "content": data.tweet_data,
            "author_id": user.id,
            "medias_id": data.tweet_media_ids,
        })

        logger.info(f"User {user.id} add tweet {tweet_id}")

        if data.tweet_media_ids:
            for media_id in data.tweet_media_ids:
                logger.info(f"User {user.id} trying to add media {media_id} to tweet {tweet_id}")

        return TweetSchemaAdd(result=True, tweet_id=tweet_id)

    async def get_tweets(self, user: UserOrm, offset: int, limit: int) -> TweetSchemaGetAll:
        """Получение списка 'Твитов' с информацией о 'Лайках', авторах и медиафайлах."""
        logger.info(f"User {user.id} trying to get all tweets")

        tweets = await self.tweet_repositories.find_all(
            relations=[TweetOrm.author, TweetOrm.likes],
            offset=offset,
            limit=limit
        )

        logger.info(f"User {user.id} received all tweets with relations")

        out: List[TweetSchemaGet] = []
        for tweet in tweets:
            attachments = []
            if tweet.medias_id:
                for media_id in tweet.medias_id:
                    media = await self.media_repositories.find_one(media_id)
                    if not media:
                        raise NotFoundError(f"Media {media_id} not found")
                    attachments.append(media.path)

            author = (UserSchemaGet(id=int(tweet.author.id), name=str(tweet.author.name),) if tweet.author else None)
            likes = [LikeSchemaGet(user_id=like.author_id, name=like.author_name) for like in tweet.likes]

            out.append(TweetSchemaGet(
                id=tweet.id,
                content=tweet.content,
                attachments=attachments,
                author=author,
                likes = likes
            ))

        logger.info(f"User {user.id} received all tweets with relations in list")
        return TweetSchemaGetAll(result=True, tweets=out)

    async def delete_tweet(self, tweet_id: int, user: UserOrm):
        """Удаление 'Твита' и медиафайлов по id, с проверкой соответствия user = автор."""
        logger.info(f"User {user.id} trying to delete tweet {tweet_id}")

        tweet = await self.tweet_repositories.find_one(tweet_id)
        if not tweet:
            raise NotFoundError("Tweet not found")

        if tweet.author_id != user.id:
            raise PermissionDeniedError("You cannot delete another user tweet")

        if tweet.medias_id:
            for media_id in tweet.medias_id:
                logger.info(f"User {user.id} trying to delete media {media_id}")

                media = await self.media_repositories.find_one(media_id)
                if not media:
                    raise NotFoundError("Media not found")

                file_disk_path = Config.MEDIA_DIR / Path(media.path).name
                if await aios.path.exists(file_disk_path):
                    await aios.remove(file_disk_path)
                else:
                    raise NotFoundError("File not found")

                await self.media_repositories.delete_one_by_id(media_id)
                logger.info(f"User {user.id} delete media{media_id}")

        await self.tweet_repositories.delete_one_by_id(tweet_id)

        logger.info(f"Tweet {tweet_id} deleted by user {user.id}")
        return TweetSchemaDelete(result=True)
