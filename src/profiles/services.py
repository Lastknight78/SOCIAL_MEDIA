from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..auth.services import existing_user
from ..auth.models import Follows, User
from ..activity.models import Activity
#follow
async def follow(db:Session, follower : str, following : str):
    db_follower = await existing_user(db, follower, "")
    db_following = await existing_user(db, following, "")
    if not db_follower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "you are not a user")
    if not db_following:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "this user does not exist")
    db_follow = (
        db.query(Follows).
        filter_by(follower_id = db_follower.id, following_id = db_following.id)
        .first())
    if db_follow:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "you are already following this user")
    db_follow = Follows(follower_id = db_follower.id, following_id = db_following.id)
    db.add(db_follow)
    db.commit()
    db_follower.following_count += 1
    db_following.follower_count += 1
    
    follow_activity = Activity(
        username = following,
        followed_username = db_follower.username,
        followed_user_pic = db_follower.profile_pic,
    )
    db.add(follow_activity)
    db.commit()
    
#unfollow
async def unfollow(db:Session, follower : str, following : str):
    db_follower = await existing_user(db, follower, "")
    db_following = await existing_user(db, following, "")
    if not db_follower:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "you are not a user")
    if not db_following:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "this user does not exist")
    db_follow = (
        db.query(Follows).
        filter(Follows.follower_id == db_follower.id, Follows.following_id == db_following.id)
        .first())
    if not db_follow:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "you don't follow this user")
    db.delete(db_follow)
    db_follower.following_count -= 1
    db_following.follower_count -= 1
    db.commit()
    
#get followers
async def followers(db:Session, user_id : int):
    subquery = db.query(Follows.follower_id).filter(Follows.following_id == user_id).subquery()
    db_followers = db.query(User.username, User.name, User.profile_pic).filter(User.id.in_(subquery)).all()
    if not db_followers:
        raise HTTPException(status_code=404, detail="No followers found")

    followers = [
        {
            "username": follower.username,
            "name": follower.name,
            "profile_pic": follower.profile_pic
        }
        for follower in db_followers
    ]
    return followers

#get following
async def following(db:Session, user_id : int):
    subquery = db.query(Follows.following_id).filter(Follows.follower_id == user_id).subquery()
    db_following = db.query(User.username, User.name, User.profile_pic).filter(User.id.in_(subquery)).all()
    if not db_following:
        raise HTTPException(status_code=404, detail="you are not following anybody yet")

    following = [
        {
            "username": follower.username,
            "name": follower.name,
            "profile_pic": follower.profile_pic
        }
        for follower in db_following
    ]
    return following