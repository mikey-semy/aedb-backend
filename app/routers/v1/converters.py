from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.auth import get_current_user
from app.database.session import get_db_session
from app.schemas.auth import UserSchema
from app.schemas.converters import ConverterSchema
from app.services.converters import ConverterService
from app.const import converters_params

router = APIRouter(**converters_params)

@router.get("/")
async def get_converters() -> List[ConverterSchema]:
    _user: UserSchema = Depends(get_current_user)
    session: Session = Depends(get_db_session)
    return await ConverterService(session).get_converters()

@router.get("/paginated")
async def get_converters_paginated(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session)
) -> dict:
    return await ConverterService(session).get_converters_paginated(page, page_size)

@router.post("/add_all")
async def add_all_data(
    # _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> None:
    """Добавляет все данные из JSON"""
    await ConverterService(session).add_all_converters()