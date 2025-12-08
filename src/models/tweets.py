from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import ModelBase


class TweetOrm(ModelBase):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    medias_id: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True, default=list)

    author: Mapped["UserOrm"] = relationship(
        back_populates="tweets",
        foreign_keys=[author_id]
    )
    likes: Mapped[list["LikeOrm"]] = relationship(
        back_populates="tweet",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
