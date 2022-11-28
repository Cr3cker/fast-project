from apis.version1 import route_general_pages
from apis.version1 import route_users
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(
    route_general_pages.general_pages_router, prefix="", tags=["general_pages"]
)
api_router.include_router(route_users.router,prefix="/users", tags=["users"])
