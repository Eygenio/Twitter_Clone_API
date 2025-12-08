import pytest
from unittest.mock import AsyncMock

from src.services.followers import FollowerService
from src.exceptions.exceptions import NotFoundError
from src.models.users import UserOrm


@pytest.mark.asyncio
async def test_subscribe_success():
    """
    Mock пользовательский репозиторий для возврата пользователя при вызове find_one.
    """
    user_repo = AsyncMock()
    user_repo.find_one = AsyncMock(return_value=UserOrm(id=2, name="bob", api_key="k"))

    follower_repo = AsyncMock()
    follower_repo.add_one_no_return = AsyncMock()

    service = FollowerService(follower_repo, user_repo)

    result = await service.subscribe(user_id=2, user=UserOrm(id=1, name="alice", api_key="a"))
    assert result.result is True
    follower_repo.add_one_no_return.assert_awaited_once()


@pytest.mark.asyncio
async def test_subscribe_user_not_found():
    """
    Mock пользовательский репозиторий для возврата None (пользователь не найден).
    """
    user_repo = AsyncMock()
    user_repo.find_one = AsyncMock(return_value=None)

    follower_repo = AsyncMock()

    service = FollowerService(follower_repo, user_repo)

    with pytest.raises(NotFoundError):
        await service.subscribe(user_id=99, user=UserOrm(id=1, name="alice", api_key="a"))
        