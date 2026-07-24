from pydantic import BaseModel, ConfigDict

from src.presentation.schemas.likes import LikeSchemaGet
from src.presentation.schemas.users import UserSchemaGet


class TweetSchemasCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] | None = None


class TweetSchemaAdd(BaseModel):
    result: bool
    tweet_id: int


class TweetSchemaDelete(BaseModel):
    result: bool


class TweetSchemaGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    attachments: list[str]
    author: UserSchemaGet
    likes: list[LikeSchemaGet]


class TweetSchemaGetAll(BaseModel):
    result: bool
    tweets: list[TweetSchemaGet]
