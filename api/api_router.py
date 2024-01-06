from fastapi import APIRouter

from api.links import link_router
from api.users import auth_router, user_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router, tags=["auth"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(link_router, prefix="/link", tags=["link"])
