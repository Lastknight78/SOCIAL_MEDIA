from fastapi import Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi import APIRouter
from ..auth.services import get_current_user
from ..auth.schema import TokenData
from ..auth.models import User
from .services import follow, unfollow, followers, following

profile_router = APIRouter(
    tags=['profile'],
    prefix= "/profile"
)

@profile_router.post("/follow/{username}", status_code=status.HTTP_200_OK)
async def follow_func(*, db: Session = Depends(get_db),username : str,current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    if user.username == username:
        return {"error" : "you cannot follow yourself"}
    await follow(db, user.username, username)
    return {"success": f"you are already following {username}"}

@profile_router.post("/unfollow/{username}", status_code=status.HTTP_200_OK)
async def unfollow_func(*, db: Session = Depends(get_db),username : str,current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    if user.username == username:
        return {"error" : "you cannot unfollow yourself"}
    await unfollow(db, user.username, username)
    return {"success" : f"you have successfully unfollowed {username}"}
    
@profile_router.get("/followers/{user_id}")
async def get_followers_func(*, db:Session = Depends(get_db),current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    return await followers(db, user.id)

@profile_router.get("/following/{user_id}")
async def get_following_func(*, db:Session = Depends(get_db),current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    return await following(db, user.id)
    