import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.medias import MediaService
from src.models.users import UserOrm
from src.exceptions.exceptions import AlreadyExistsError, NotFoundError
from pathlib import Path
import aiofiles


@pytest.mark.asyncio
async def test_save_media_success(tmp_path, monkeypatch):
    """
    Тестирование успешного сохранения файла.
    """
    class FakeUpload:

        filename = "picture.png"
        async def read(self):
            return b"12345"

    media_repo = AsyncMock()
    media_repo.add_one = AsyncMock(return_value=1)
    media_repo.find_one = AsyncMock(return_value=MagicMock(id=1, path="/media/picture.png"))

    from src.config.base import Config
    monkeypatch.setattr(Config, "MEDIA_DIR", tmp_path)

    service = MediaService(media_repo)
    res = await service.save_media(FakeUpload(), UserOrm(id=1, name="u", api_key="k"))

    assert res.result is True
    assert res.media_id == 1


@pytest.mark.asyncio
async def test_save_media_already_exists(monkeypatch):
    """
    Тестирование случая, когда файл уже существует.
    """
    class FakeUpload:

        filename = "picture.png"
        async def read(self):
            return b"12345"

    media_repo = AsyncMock()
    media_repo.add_one = AsyncMock(return_value=None)  # simulate fail

    from src.config.base import Config
    monkeypatch.setattr(Config, "MEDIA_DIR", Path("/tmp"))

    service = MediaService(media_repo)
    with pytest.raises(AlreadyExistsError):
        await service.save_media(FakeUpload(), UserOrm(id=1, name="u", api_key="k"))
