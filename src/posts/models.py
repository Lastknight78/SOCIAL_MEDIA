from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
#association table
post_hashtags = Table(
    "post_hashtags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("hashtag_id", Integer, ForeignKey("hashtags.id")),
)
#association table
post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("post_id", Integer, ForeignKey("posts.id")),
)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500))
    image = Column(String(500))
    location = Column(String(500))
    created_dt = Column(DateTime, default=datetime.utcnow())
    likes_count = Column(Integer, default=0)

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("auth.models.User", back_populates="posts")

    hashtags = relationship("Hashtag", secondary=post_hashtags, back_populates="posts")

    liked_by_users = relationship(
        "auth.models.User", secondary=post_likes, back_populates="liked_posts"
    )


class Hashtag(Base):
    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

    posts = relationship("Post", secondary=post_hashtags, back_populates="hashtags")