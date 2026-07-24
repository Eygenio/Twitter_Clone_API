from sqlalchemy import ARRAY, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import ModelBase


class TweetOrm(ModelBase):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    medias_id: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True, default=list)

    author: Mapped["UserOrm"] = relationship(  # noqa: F821
        back_populates="tweets",
        foreign_keys=[author_id],
    )
    likes: Mapped[list["LikeOrm"]] = relationship(  # noqa: F821
        back_populates="tweet", cascade="all, delete-orphan", passive_deletes=True
    )
