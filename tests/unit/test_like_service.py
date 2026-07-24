from typing import cast
from unittest.mock import MagicMock

import pytest

from src.application.services.likes import LikeService
from src.domain.entities import Like, Tweet, User
from src.exceptions.exceptions import PermissionDeniedError


@pytest.mark.asyncio
async def test_give_like_success(
    like_service: LikeService,
    mock_uow: MagicMock,
    sample_user: User,
    sample_tweet: Tweet,
) -> None:
    mock_uow.tweets.get_by_id.return_value = sample_tweet
    mock_uow.likes.get_by_tweet_and_user.return_value = None

    async def add_like_side_effect(like: Like) -> Like:
        like.id = 10
        return like

    mock_uow.likes.add.side_effect = add_like_side_effect

    if sample_tweet.id is None:
        raise ValueError("User ID is not set")
    like = await like_service.give_like(sample_tweet.id, sample_user)

    assert like.tweet_id == sample_tweet.id
    assert like.author_id == sample_user.id
    mock_uow.likes.add.assert_called_once()


@pytest.mark.asyncio
async def test_give_like_already_exists(
    like_service: LikeService,
    mock_uow: MagicMock,
    sample_user: User,
    sample_tweet: Tweet,
) -> None:
    mock_uow.tweets.get_by_id.return_value = sample_tweet
    mock_uow.likes.get_by_tweet_and_user.return_value = Like(
        tweet_id=sample_tweet.id, author_id=sample_user.id, author_name=sample_user.name
    )
    with pytest.raises(PermissionDeniedError):
        await like_service.give_like(cast(int, sample_tweet.id), sample_user)


@pytest.mark.asyncio
async def test_remove_like_success(
    like_service: LikeService,
    mock_uow: MagicMock,
    sample_user: User,
    sample_tweet: Tweet,
) -> None:
    if sample_user.id is None:
        raise ValueError("User ID is not set")
    if sample_tweet.id is None:
        raise ValueError("Tweet ID is not set")
    existing_like = Like(
        id=10, tweet_id=sample_tweet.id, author_id=sample_user.id, author_name=sample_user.name
    )
    mock_uow.likes.get_by_tweet_and_user.return_value = existing_like
    await like_service.remove_like(sample_tweet.id, sample_user)
    mock_uow.likes.delete.assert_called_once_with(existing_like.id)
