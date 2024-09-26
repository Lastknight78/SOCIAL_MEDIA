from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .schema import Post as PostSchema, PostCreate
from .models import Post, Hashtag,post_hashtags
from ..auth.models import User
from ..auth.schema import User as UserSchema
from ..activity.models import Activity
import re
from sqlalchemy import desc

def create_hashtags(db: Session, post: Post):
    regex = r"#\w+"
    matches = re.findall(regex, post.content)

    for match in matches:
        name = match[1:]
        hashtag = db.query(Hashtag).filter(Hashtag.name == name).first()
        if not hashtag:
            hashtag = Hashtag(name=name)
            db.add(hashtag)
        post.hashtags.append(hashtag)

# create post
async def post_create(db: Session, post: PostCreate, user_id: int):
    db_post = Post(
        **post.model_dump(), author_id = user_id
    )
    db.add(db_post)
    db.commit()
    create_hashtags(db, db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

#get_users_post
async def get_users_post(db : Session, user_id : int) -> list[PostSchema]:
    users_posts = (
        db.query(Post)
        .filter(Post.author_id == user_id)
        .order_by(desc(Post.created_dt))
        .all()
        )
    return users_posts

#get_posts_from_hashtags
async def get_post_from_hashtag(db : Session, hashtag_name: str):
    hashtag_post = db.query(Hashtag).filter_by(name = hashtag_name).first()
    if not hashtag_post:
        return None
    return hashtag_post.posts

#get random posts for feeds
async def get_random_posts_for_feeds(db: Session, page : int = 1, limit : int = 10, hashtag: str = None):
    offset = (page - 1) * limit
    total_posts = db.query(Post).count()
    if offset >= total_posts:
        return []
    posts = db.query(Post, User.username).join(User).order_by(desc(Post.created_dt))
    
    if hashtag:
        posts = posts.join(post_hashtags).join(Hashtag).filter(Hashtag.name == hashtag)
    posts = posts.offset(offset).limit(limit).all()
    
    result = []
    for post, username in posts:
        post_dict = post.__dict__
        post_dict["username"] = username
        result.append(post_dict)
    return result

async def get_posts_from_post_id(db:Session, post_id : int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} does not exist")
    return post
    
async def delete_post(db:Session, post_id:int):
    post = await get_posts_from_post_id(db, post_id)
    db.delete(post)
    db.commit()
    
async def like_post(db: Session, post_id : int, user_username : str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "post does not exist")
    user = db.query(User).filter(User.username == user_username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "user does not exist")
    if user in post.liked_by_users:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "you have liked the post already")
    post.liked_by_users.append(user)
    post.likes_count = len(post.liked_by_users)
    
    #like activity
    like_activity = Activity(
        username = post.author.username,
        liked_post_id = post_id,
        username_like = user.username,
        liked_post_image = post.image,
    )
    db.add(like_activity)
    db.commit()
    
    
    

async def unlike_post(db: Session, post_id : id, username : str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "post does not exist")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "user does not exist")
    if user not in post.liked_by_users:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "you have not liked the post before")
    post.liked_by_users.pop(post.liked_by_users.index(user))
    post.likes_count = len(post.liked_by_users)
    db.commit()
    

#users who liked post
async def users_who_liked_post(db:Session, post_id: int) -> list[UserSchema]:
    liked_post = db.query(Post).filter(Post.id == post_id).first()
    if not liked_post:
        return []
    users = liked_post.liked_by_users
    return users
    