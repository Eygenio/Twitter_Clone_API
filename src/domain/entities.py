from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str
    api_key: str


class Tweet(BaseModel):
    id: int | None = None
    content: str
    author_id: int
    medias_id: list[int] | None = None
    created_at: datetime | None = None


class Like(BaseModel):
    id: int | None = None
    tweet_id: int
    author_id: int
    author_name: str


class Media(BaseModel):
    id: int | None = None
    path: str


class Follower(BaseModel):
    followed_id: int
    follower_id: int
