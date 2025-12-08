from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import ModelBase


class FollowerOrm(ModelBase):
    __tablename__ = "followers"

    followed_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    followed: Mapped["UserOrm"] = relationship(
        back_populates="followers",
        foreign_keys=[followed_id]
    )
    follower: Mapped["UserOrm"] = relationship(
        back_populates="following",
        foreign_keys=[follower_id]
    )
