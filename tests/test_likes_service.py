import pytest
from unittest.mock import AsyncMock
from src.services.likes import LikeService
from src.exceptions.exceptions import NotFoundError, PermissionDeniedError
from src.models.users import UserOrm
from src.models.tweets import TweetOrm
from src.models.likes import LikeOrm


@pytest.mark.asyncio
async def test_give_like_success():
    """
    Тестирование 'Лайка' поста.
    """
    like_repo = AsyncMock()
    like_repo.add_one_no_return = AsyncMock()
    user_repo = AsyncMock()
    tweet_repo = AsyncMock()
    tweet_repo.find_one = AsyncMock(return_value=TweetOrm(id=1, content="hi", author_id=2, medias_id=None))

    service = LikeService(like_repo, user_repo, tweet_repo)

    res = await service.give_like(1, UserOrm(id=10, name="u", api_key="k"))
    assert res.result is True
    like_repo.add_one_no_return.assert_awaited_once()


@pytest.mark.asyncio
async def test_remove_like_success():
    """
    Тестирования удаления 'Лайка' с поста.
    """
    like_repo = AsyncMock()
    like_repo.delete_one_by_id = AsyncMock()
    user_repo = AsyncMock()
    tweet_repo = AsyncMock()

    # создание твита с 'Лайком' от пользователя с id=5.
    like = AsyncMock()
    like.author_id = 5
    like.id = 123
    tweet = AsyncMock()
    tweet.likes = [like]
    tweet_repo.find_one = AsyncMock(return_value=tweet)

    service = LikeService(like_repo, user_repo, tweet_repo)

    res = await service.remove_like(1, UserOrm(id=5, name="u", api_key="k"))
    assert res.result is True
    like_repo.delete_one_by_id.assert_awaited_once_with(123)


@pytest.mark.asyncio
async def test_remove_like_not_allowed():
    """
    Тестирование попытки удаления чужого 'Лайка'.
    """
    like_repo = AsyncMock()
    user_repo = AsyncMock()
    tweet_repo = AsyncMock()

    like = AsyncMock()
    like.author_id = 99
    like.id = 123
    tweet = AsyncMock()
    tweet.likes = [like]
    tweet_repo.find_one = AsyncMock(return_value=tweet)

    service = LikeService(like_repo, user_repo, tweet_repo)

    with pytest.raises(PermissionDeniedError):
        await service.remove_like(1, UserOrm(id=1, name="u", api_key="k"))
        