from fastapi import APIRouter, File, UploadFile

from src.presentation.dependencies import CurrentUserDep, MediaServiceDep
from src.presentation.schemas.medias import MediaSchemaAdd

router = APIRouter(prefix="/api", tags=["media"])


@router.post("/medias", response_model=MediaSchemaAdd)
async def add_media(
    user: CurrentUserDep,
    service: MediaServiceDep,
    file: UploadFile = File(...),
) -> MediaSchemaAdd:
    media = await service.save_media(file)
    return MediaSchemaAdd(result=True, media_id=media.id)
