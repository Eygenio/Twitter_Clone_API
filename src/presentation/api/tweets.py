from fastapi import APIRouter, Query

from src.presentation.dependencies import CurrentUserDep, TweetsServiceDep
from src.presentation.schemas.tweets import (
    TweetSchemaAdd,
    TweetSchemaDelete,
    TweetSchemaGetAll,
    TweetSchemasCreate,
)

router = APIRouter(prefix="/api", tags=["tweets"])


@router.post("/tweets", response_model=TweetSchemaAdd)
async def create_tweet(
    payload: TweetSchemasCreate,
    user: CurrentUserDep,
    service: TweetsServiceDep,
) -> TweetSchemaAdd:
    tweet = await service.add_tweet(user, payload.tweet_data, payload.tweet_media_ids)
    return TweetSchemaAdd(result=True, tweet_id=tweet.id)


@router.get("/tweets", response_model=TweetSchemaGetAll)
async def get_tweets(
    user: CurrentUserDep,
    service: TweetsServiceDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
) -> TweetSchemaGetAll:
    return await service.get_tweets_full(offset, limit)


@router.delete("/tweets/{id}", response_model=TweetSchemaDelete)
async def delete_tweet(
    id: int,
    user: CurrentUserDep,
    service: TweetsServiceDep,
) -> TweetSchemaDelete:
    await service.delete_tweet(id, user)
    return TweetSchemaDelete(result=True)
