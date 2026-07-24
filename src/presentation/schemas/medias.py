from pydantic import BaseModel, ConfigDict


class MediaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    path: str


class MediaSchemaAdd(BaseModel):
    result: bool
    media_id: int
