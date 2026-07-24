from pydantic import BaseModel


class FollowerSchema(BaseModel):
    result: bool
