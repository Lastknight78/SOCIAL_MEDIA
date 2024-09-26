from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class PostCreate(BaseModel):
    #author_id : int
    content : str | None = None
    image : str | None = None
    location : Optional[str] = None
    
class Post(PostCreate):
    id : int
    created_dt : datetime
    author_id : int
    likes_count : int
    class config:
        from_attributes = True
        
class HashtagSchema(BaseModel):
    id : int
    name : str
    