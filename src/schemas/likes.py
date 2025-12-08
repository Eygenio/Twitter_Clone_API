from pydantic import BaseModel


class LikeSchema(BaseModel):
    result: bool


class LikeSchemaGet(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True
