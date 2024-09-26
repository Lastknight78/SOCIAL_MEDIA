from sqlalchemy.orm import Session
from fastapi import APIRouter, status, HTTPException, Depends
from ..database import get_db
from  .schema import PostCreate, Post as PostSchema
from ..auth.schema import User as UserSchema,TokenData
from ..auth.services import get_current_user
from ..auth.models import User
from .sevices import (post_create, 
                get_users_post, 
                get_post_from_hashtag, 
                get_random_posts_for_feeds, 
                delete_post,
                get_posts_from_post_id,
                like_post,
                unlike_post,
                users_who_liked_post
                )

post_router = APIRouter(
    tags=["posts"],
    prefix= "/post"
)
@post_router.post("/create_post",status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create_post(*,db : Session = Depends(get_db), create_post : PostCreate,current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    user_post = await post_create(db, create_post, user.id)
    return user_post

@post_router.get("/get_user_posts")
async def get_posts(*,db : Session = Depends(get_db), current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    user_posts = await get_users_post(db, user.id)
    return user_posts

@post_router.get("/get_post_from_hashtag/{hashtag_name}")
async def get_posts(*, db : Session = Depends(get_db), hashtag_name : str):
    posts = await get_post_from_hashtag(db, hashtag_name)
    return posts

@post_router.get("/user_feeds")
async def get_post_for_feed(*,db : Session = Depends(get_db), page : int = 1, limit : int = 5, hashtag : str = None):
    return await get_random_posts_for_feeds(db, page, limit, hashtag)
    
@post_router.delete("/delete_post", status_code=status.HTTP_204_NO_CONTENT)
async def post_delete(*,db:Session = Depends(get_db), post_id : int,current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    post = await get_posts_from_post_id(db, post_id)
    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to delete this post"
        )
    await delete_post(db, post_id)
    
@post_router.post("/like_post")
async def user_like_post(*, db:Session = Depends(get_db) ,post_id : int, current_user : TokenData = Depends(get_current_user)):
    await like_post(db,post_id, current_user.token_username)
    return {"successful":"post liked successfully"}

@post_router.post("/unlike_post", status_code=status.HTTP_204_NO_CONTENT)
async def user_like_post(*, db: Session = Depends(get_db), post_id: int, current_user : TokenData = Depends(get_current_user)):
    await unlike_post(db, post_id, current_user.token_username)
    return {"successful":"post unliked successfully"}

@post_router.get("/users_who_liked_a_post/{post_id}", response_model = list[UserSchema])
async def users_post_liked(*, db:Session = Depends(get_db), post_id : int):
    return await users_who_liked_post(db, post_id)


    