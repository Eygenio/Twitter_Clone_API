from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.models.base import ModelBase


class LikeOrm(ModelBase):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("tweet_id", "author_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author_name: Mapped[str] = mapped_column()

    tweet: Mapped["TweetOrm"] = relationship(back_populates="likes")  # noqa: F821
    user: Mapped["UserOrm"] = relationship(back_populates="likes")  # noqa: F821
