from sqlalchemy.orm import Session
from .models import Activity
#get activity of each users by their username
async def get_activity(db:Session, username : str, page : int = 1, limit : int = 10):
    offset = (page - 1)*limit
    user_activity = db.query(Activity).order_by(Activity.timestamp.desc()).filter(Activity.username == username).offset(offset).limit(limit).all()
    return user_activity