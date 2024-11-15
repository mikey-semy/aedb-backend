from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.const import post_params
from app.database.session import get_db_session

from app.schemas.auth import UserSchema
from app.schemas.posts import PostSchema
from app.services.auth import get_current_user
from app.services.posts import PostService

router = APIRouter(**post_params)

@router.get("/", response_model=PostSchema)
async def get_post(
    post_id: int,
    _user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> PostSchema:
    return PostService(session).get_post(post_id)

@router.get("/", response_model=List[PostSchema])
async def get_posts(
    _user: UserSchema = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session)
) -> List[PostSchema]:

    return PostService(session).get_posts()