from .database import engine, Base
from fastapi import FastAPI
from .auth.models import User, Follows
from .posts.models import Post, post_likes, post_hashtags, Hashtag
from .api import router
Base.metadata.create_all(bind = engine)
app = FastAPI(
    title = "social_media_app",
    description="engine behind social media",
    version = "0.1"
)
app.include_router(router)