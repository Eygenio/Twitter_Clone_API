from pydantic import BaseModel, ConfigDict


class UserSchemaGet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class UserSchemaInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    followers: list[UserSchemaGet]
    following: list[UserSchemaGet]


class UserSchemaGetID(BaseModel):
    result: bool
    user: UserSchemaInfo | None = None
