from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import ModelBase


class MediaOrm(ModelBase):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False)
