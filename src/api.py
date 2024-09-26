from fastapi import APIRouter
from .auth.views import auth_router
from .posts.views import post_router
from .activity.views import activity_router
from .profiles.views import profile_router
router = APIRouter()
router.include_router(auth_router)
router.include_router(post_router)
router.include_router(activity_router)
router.include_router(profile_router)
