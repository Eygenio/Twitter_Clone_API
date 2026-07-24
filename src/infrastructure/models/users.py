from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import ModelBase


class UserOrm(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column(unique=True)

    followers: Mapped[list["FollowerOrm"]] = relationship(  # noqa: F821
        back_populates="followed",
        foreign_keys="FollowerOrm.followed_id",
        cascade="all, delete-orphan",
    )
    following: Mapped[list["FollowerOrm"]] = relationship(  # noqa: F821
        back_populates="follower",
        foreign_keys="FollowerOrm.follower_id",
        cascade="all, delete-orphan",
    )
    tweets: Mapped[list["TweetOrm"]] = relationship(  # noqa: F821
        back_populates="author", cascade="all, delete-orphan"
    )
    likes: Mapped[list["LikeOrm"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
