from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.models.base import ModelBase


class UserOrm(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    api_key: Mapped[str] = mapped_column(unique=True)

    followers: Mapped[list["FollowerOrm"]] = relationship(
        back_populates="followed",
        foreign_keys="FollowerOrm.followed_id",
        cascade="all, delete-orphan"
    )
    following: Mapped[list["FollowerOrm"]] = relationship(
        back_populates="follower",
        foreign_keys="FollowerOrm.follower_id",
        cascade="all, delete-orphan"
    )
    tweets: Mapped[list["TweetOrm"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )
    likes: Mapped[list["LikeOrm"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
