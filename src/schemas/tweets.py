from pydantic import BaseModel

from src.schemas.users import UserSchemaGet
from src.schemas.likes import LikeSchemaGet


class TweetSchemasCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None = None


class TweetSchemaAdd(BaseModel):
    result: bool
    tweet_id: int


class TweetSchemaDelete(BaseModel):
    result: bool


class TweetSchemaGet(BaseModel):
    id: int
    content: str
    attachments: list[str]
    author: UserSchemaGet
    likes: list[LikeSchemaGet]

    class Config:
        from_attributes = True


class TweetSchemaGetAll(BaseModel):
    result: bool
    tweets: list[TweetSchemaGet]
