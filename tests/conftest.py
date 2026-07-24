from collections.abc import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker
from starlette.testclient import TestClient

from src.app import app
from src.application.services.followers import FollowerService
from src.application.services.likes import LikeService
from src.application.services.medias import MediaService
from src.application.services.tweets import TweetsService
from src.application.services.users import UsersService
from src.domain.entities import Tweet, User
from src.domain.unit_of_work import IUnitOfWork
from src.presentation.dependencies import get_uow

fake = Faker()


@pytest.fixture
def health_url() -> str:
    return "/health"


@pytest.fixture
def tweets_url() -> str:
    return "/api/tweets"


@pytest.fixture
def users_url() -> str:
    return "/api/users"


@pytest.fixture(autouse=True)
def override_get_uow_for_e2e() -> Generator[None]:
    mock_uow = MagicMock(spec=IUnitOfWork)
    mock_uow.users = AsyncMock()
    mock_uow.tweets = AsyncMock()
    mock_uow.likes = AsyncMock()
    mock_uow.media = AsyncMock()
    mock_uow.followers = AsyncMock()

    async def _override() -> AsyncGenerator:
        yield mock_uow

    app.dependency_overrides[get_uow] = _override
    yield
    app.dependency_overrides.pop(get_uow, None)


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_user() -> User:
    return User(
        id=fake.random_int(1, 100),
        name=fake.user_name(),
        api_key=fake.uuid4(),
    )


@pytest.fixture
def sample_tweet() -> Tweet:
    return Tweet(
        id=fake.random_int(1, 100),
        content=fake.sentence(),
        author_id=fake.random_int(1, 100),
    )


@pytest.fixture
def mock_uow() -> IUnitOfWork:
    uow = MagicMock(spec=IUnitOfWork)
    uow.users = AsyncMock()
    uow.tweets = AsyncMock()
    uow.likes = AsyncMock()
    uow.media = AsyncMock()
    uow.followers = AsyncMock()
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    return uow


@pytest.fixture
def follower_service(mock_uow: IUnitOfWork) -> FollowerService:
    return FollowerService(mock_uow)


@pytest.fixture
def like_service(mock_uow: IUnitOfWork) -> LikeService:
    return LikeService(mock_uow)


@pytest.fixture
def tweet_service(mock_uow: IUnitOfWork) -> TweetsService:
    return TweetsService(mock_uow)


@pytest.fixture
def user_service(mock_uow: IUnitOfWork) -> UsersService:
    return UsersService(mock_uow)


@pytest.fixture
def media_service(mock_uow: IUnitOfWork) -> MediaService:
    return MediaService(mock_uow)
