from pydantic import BaseModel


class AppConfig(BaseModel):
    title: str = "Twitter Clone API"
    version: str = "1.0.0"
    description: str = "Public API v1"

    host: str
    port: int
