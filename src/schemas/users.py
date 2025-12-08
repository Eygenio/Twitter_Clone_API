from pydantic import BaseModel
from typing import Optional


class UserSchemaGet(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserSchemaInfo(BaseModel):
    id: int
    name: str
    followers: list[UserSchemaGet]
    following: list[UserSchemaGet]

    class Config:
        from_attributes = True


class UserSchemaGetID(BaseModel):
    result: bool
    user: Optional[UserSchemaInfo] = None
