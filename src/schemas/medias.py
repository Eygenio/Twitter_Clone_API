from pydantic import BaseModel


class MediaRead(BaseModel):
    path: str

    class Config:
        from_attributes = True


class MediaSchemaAdd(BaseModel):
    result: bool
    media_id: int
