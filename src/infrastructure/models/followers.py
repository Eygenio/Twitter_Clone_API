from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import ModelBase


class FollowerOrm(ModelBase):
    __tablename__ = "followers"

    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    followed: Mapped["UserOrm"] = relationship(  # noqa: F821
        back_populates="followers", foreign_keys=[followed_id]
    )
    follower: Mapped["UserOrm"] = relationship(  # noqa: F821
        back_populates="following", foreign_keys=[follower_id]
    )
