from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .models import User
from .schema import UserCreate,UserUpdate,User as UserSchema, TokenData
from .services import (
    create_access_token,
    update_user,
    authenticate,
    existing_user,
    create_user, get_current_user
    )

auth_router = APIRouter(
    tags=['auth'],
    prefix='/auth'
)
@auth_router.post("/signup")
async def signup(*, db : Session = Depends(get_db), user : UserCreate):
    db_user = await existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
    db_user = await create_user(db, user)
    access_token = await create_access_token(db, db_user.username, db_user.id)
    return {
        "access token":access_token,
        "token_type" : "bearer",
        "id" : db_user.id,
        "username" : db_user.username
    }
@auth_router.post("/login")
async def login(*, db : Session = Depends(get_db), form_date : OAuth2PasswordRequestForm = Depends()) :
    db_user = await authenticate(db, form_date.username, form_date.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "invalid username or password")
    access_token = await create_access_token(db, db_user.username, db_user.hashed_password)
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
    
@auth_router.get("/profile",status_code= status.HTTP_200_OK, response_model = UserSchema)
async def get_user(*, db : Session = Depends(get_db),current_user : TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    return user

@auth_router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def updates(*, db : Session = Depends(get_db), username : str,current_user : TokenData = Depends(get_current_user), user_update : UserUpdate):
    user = db.query(User).filter(User.username == current_user.token_username).first()
    if user.username != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you are not authorized to update this user")
    await update_user(db, user, user_update)

