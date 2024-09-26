from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from .enums import Gender

class UserBase(BaseModel):
    email : EmailStr
    username : str
    
class UserCreate(UserBase):
    hashed_password : str
    
class UserUpdate(BaseModel):
    name : str
    date_of_birth : Optional[date] = None
    gender : Optional[Gender] = None
    bio : Optional[str] = None
    location : Optional[str] = None
    profile_pic : Optional[str] = None
class User(UserBase):
    id : int
    created_at : datetime
    class Config:
        from_attributes = True
        
class TokenData(BaseModel):
    token_username : Optional[str] = None
        