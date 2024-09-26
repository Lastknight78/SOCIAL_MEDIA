from ..database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from .enums import Gender
from ..posts.models import Post, post_likes
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    Text,
    ForeignKey,
    Enum,
    DateTime,
    Date,
)



class Follows(Base):
    __tablename__ = "follows"
    follower_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    following_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="followers"
    )
    following = relationship(
        "User", foreign_keys=[following_id], back_populates="following"
    )


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    email = Column(String(80), unique=True)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())

    date_of_birth = Column(Date)
    gender = Column(Enum(Gender))
    profile_pic = Column(String(255))
    bio = Column(String(255))
    location = Column(String(255))

    followers = relationship(
        Follows, foreign_keys=[Follows.following_id], back_populates="following"
    )
    following = relationship(
        Follows, foreign_keys=[Follows.follower_id], back_populates="follower"
    )
    liked_posts = relationship(
        Post, secondary=post_likes, back_populates="liked_by_users"
    )
    posts = relationship(Post, back_populates="author")
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
