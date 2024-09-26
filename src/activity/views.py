from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .services import get_activity



activity_router = APIRouter(
    tags = ['activity'],
    prefix = "/activity"
)

@activity_router.get("/get_activity/{username}")
async def activity(*, db : Session = Depends(get_db), username : str, page : int = 1, limit : int = 10):
    return await get_activity(db, username, page, limit)
    
    