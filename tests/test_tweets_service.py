import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.tweets import TweetsService
from src.models.users import UserOrm
from src.schemas.tweets import TweetSchemasCreate
from src.models.tweets import TweetOrm
from src.exceptions.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_add_tweet_success():
    """
    Тестирование успешного добавления 'Твита'.
    """
    tweet_repo = AsyncMock()
    tweet_repo.add_one = AsyncMock(return_value=10)
    user_repo = AsyncMock()
    media_repo = AsyncMock()
    service = TweetsService(tweet_repo, user_repo, media_repo)

    payload = TweetSchemasCreate(tweet_data="hello", tweet_media_ids=None)
    res = await service.add_tweet(UserOrm(id=1, name="a", api_key="k"), payload)
    assert res.result is True
    assert res.tweet_id == 10


@pytest.mark.asyncio
async def test_get_tweets_with_media_and_likes(monkeypatch):
    """
    Тестирование успешного добавления 'Твита' с файлом и 'Лайком'.
    """
    tweet_repo = AsyncMock()
    # создание 'Твита'
    tweet = MagicMock()
    tweet.id = 1
    tweet.content = "text"
    tweet.author = MagicMock(id=2, name="bob")
    tweet.medias_id = [5]
    # добавление 'Лайка'
    like = MagicMock()
    like.author_id = 3
    like.author_name = "ann"
    tweet.likes = [like]

    tweet_repo.find_all = AsyncMock(return_value=[tweet])
    media_repo = AsyncMock()
    media_repo.find_one = AsyncMock(return_value=MagicMock(id=5, path="/media/f.png"))
    user_repo = AsyncMock()
    service = TweetsService(tweet_repo, user_repo, media_repo)

    res = await service.get_tweets(UserOrm(id=1, name="a", api_key="k"), offset=0, limit=10)
    assert res.result is True
    assert len(res.tweets) == 1
    assert res.tweets[0].attachments == ["/media/f.png"]


@pytest.mark.asyncio
async def test_delete_tweet_not_found():
    """
    Тестирование попытки удаление несуществующего 'Твита'.
    """
    tweet_repo = AsyncMock()
    tweet_repo.find_one = AsyncMock(return_value=None)
    media_repo = AsyncMock()
    user_repo = AsyncMock()
    service = TweetsService(tweet_repo, user_repo, media_repo)

    with pytest.raises(NotFoundError):
        await service.delete_tweet(123, UserOrm(id=1, name="a", api_key="k"))
        