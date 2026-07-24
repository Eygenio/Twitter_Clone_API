from abc import ABC, abstractmethod
from collections.abc import Sequence

from src.domain.entities import Follower, Like, Media, Tweet, User


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_api_key(self, api_key: str) -> User | None:
        pass

    @abstractmethod
    async def get_users_by_ids(self, user_ids: list[int]) -> Sequence[User]:
        pass


class ITweetRepository(ABC):
    @abstractmethod
    async def get_by_id(self, tweet_id: int) -> Tweet | None:
        pass

    @abstractmethod
    async def get_all(self, offset: int, limit: int) -> Sequence[Tweet]:
        pass

    @abstractmethod
    async def add(self, tweet: Tweet) -> Tweet:
        pass

    @abstractmethod
    async def delete(self, tweet_id: int) -> None:
        pass


class ILikeRepository(ABC):
    @abstractmethod
    async def add(self, like: Like) -> Like:
        pass

    @abstractmethod
    async def delete(self, like_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_tweet_and_user(
        self,
        tweet_id: int,
        user_id: int,
    ) -> Like | None:
        pass

    @abstractmethod
    async def get_by_tweet_id(self, tweet_id: int) -> list[Like]:
        pass


class IFollowerRepository(ABC):
    @abstractmethod
    async def add(self, follower: Follower) -> None:
        pass

    @abstractmethod
    async def delete(self, follower: Follower) -> None:
        pass

    @abstractmethod
    async def get_by_followed(self, followed_id: int) -> list[Follower]:
        pass

    @abstractmethod
    async def get_by_follower(self, follower_id: int) -> list[Follower]:
        pass


class IMediaRepository(ABC):
    @abstractmethod
    async def add(self, media: Media) -> Media:
        pass

    @abstractmethod
    async def get_by_id(self, media_id: int) -> Media | None:
        pass

    @abstractmethod
    async def delete(self, media_id: int) -> None:
        pass

    @abstractmethod
    async def get_by_ids(self, media_ids: list[int]) -> list[Media]:
        pass
