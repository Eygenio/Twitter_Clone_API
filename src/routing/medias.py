from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.models.users import UserOrm
from src.schemas.medias import MediaSchemaAdd
from src.services.medias import MediaService
from src.repositories.medias import MediaRepository
from src.db.db import get_async_session

router = APIRouter()

medias_router = router


# зависимости для создания сервиса медиафайлов.
def media_service(session: AsyncSession= Depends(get_async_session)):
    return MediaService(MediaRepository(session))


@router.post("/api/medias",
             response_model=MediaSchemaAdd,
             tags=["Media"],
             summary="Загрузка медиафайлов",
             description="Загрузка медиафайлов на сервер."
             )
async def add_media(
        user: UserOrm = Depends(get_current_user),
        file: UploadFile = File(...),
        service: MediaService = Depends(media_service)
):
    return await service.save_media(file, user)
