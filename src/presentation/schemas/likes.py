from pydantic import BaseModel, ConfigDict


class LikeSchema(BaseModel):
    result: bool


class LikeSchemaGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    name: str
