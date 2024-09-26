from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .schema import UserCreate, UserUpdate, TokenData
import os, dotenv
dotenv.load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")

#checking if a user exists
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(User).filter(User.email == email).first()
    return db_user

#creating a user
async def create_user(db:Session, user : UserCreate):
    hash_password = bcrypt_context.hash(user.hashed_password)
    user.hashed_password = hash_password
    db_user = User(
        **user.model_dump()
    )
    db.add(db_user)
    db.commit()
    return db_user

#authenticating the credentials of the user
async def authenticate(db:Session, username : str, password : str):
    db_name = db.query(User).filter(User.username == username).first()
    if not db_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "invalid credentials")
    if not bcrypt_context.verify(password,db_name.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail = "invalid credentials")
    return db_name

#create access token
async def create_access_token(db:Session, username : str, id : int):
    encode = {"username":username, "id":id}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


        
#update_user_credentials
async def update_user(db:Session, db_user: User, update_user: UserUpdate):
    db_user.name = update_user.name
    db_user.bio = update_user.bio
    db_user.date_of_birth = update_user.date_of_birth
    db_user.gender = update_user.gender
    db_user.location = update_user.location
    db_user.profile_pic = update_user.profile_pic
    db.commit()
    
#get_current_user

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("id")
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(token_username = username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oauth2_bearer)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)
