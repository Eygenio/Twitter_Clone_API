from unittest.mock import MagicMock

import pytest

from src.application.services.followers import FollowerService
from src.domain.entities import Follower, User
from src.exceptions.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_subscribe_success(
    follower_service: FollowerService,
    mock_uow: MagicMock,
    sample_user: User,
) -> None:
    if sample_user.id is None:
        raise ValueError("User ID is not set")
    target_id = sample_user.id + 1
    target_user = User(id=target_id, name="target", api_key="key")
    mock_uow.users.get_by_id.return_value = target_user

    await follower_service.subscribe(target_id, sample_user)

    mock_uow.followers.add.assert_called_once()
    added_follower: Follower = mock_uow.followers.add.call_args[0][0]
    assert added_follower.followed_id == target_id
    assert added_follower.follower_id == sample_user.id


@pytest.mark.asyncio
async def test_subscribe_user_not_found(
    follower_service: FollowerService,
    mock_uow: MagicMock,
    sample_user: User,
) -> None:
    mock_uow.users.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        await follower_service.subscribe(999, sample_user)


@pytest.mark.asyncio
async def test_unsubscribe_success(
    follower_service: FollowerService,
    mock_uow: MagicMock,
    sample_user: User,
) -> None:
    if sample_user.id is None:
        raise ValueError("User ID is not set")
    target_id = sample_user.id + 1
    target_user = User(id=target_id, name="target", api_key="key")
    mock_uow.users.get_by_id.return_value = target_user

    await follower_service.unsubscribe(target_id, sample_user)
    mock_uow.followers.delete.assert_called_once()
