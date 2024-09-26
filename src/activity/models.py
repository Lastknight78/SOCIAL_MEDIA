from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)  
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow())

    liked_post_id = Column(Integer)
    username_like = Column(String(255))
    liked_post_image = Column(String(255))

    followed_username = Column(String(255))
    followed_user_pic = Column(String(255))