from fastapi import APIRouter
from app.routers.v1 import main, auth, posts, manuals
from app.const import api_prefix

all_routers = APIRouter()

all_routers.include_router(main.router)
all_routers.include_router(auth.router, prefix=api_prefix)
all_routers.include_router(posts.router, prefix=api_prefix)
all_routers.include_router(manuals.router, prefix=api_prefix)
