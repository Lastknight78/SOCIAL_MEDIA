from pydantic import BaseModel

class activities(BaseModel):
    username : str
    liked_post_id : int
    username_like : str
    liked_post_image : str
    class config:
        from_attributes = True
