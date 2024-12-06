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
    # _user: UserSchema = Depends(get_current_user),
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

@router.delete("/converters/{converter_id}", response_model=bool)
async def delete_converter(converter_id: int, session: Session = Depends(get_db_session)):
    deleted = await ConverterService(session).delete_converter(converter_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Converter not found")
    return deleted

@router.delete("/cabinets/{cabinet_id}", response_model=bool)
async def delete_cabinet(cabinet_id: int, session: Session = Depends(get_db_session)):
    deleted = await ConverterService(session).delete_cabinet(cabinet_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return deleted

@router.delete("/production_lines/{production_line_id}", response_model=bool)
async def delete_production_line(production_line_id: int, session: Session = Depends(get_db_session)):
    deleted = await ConverterService(session).delete_production_line(production_line_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Production line not found")
    return deleted

@router.delete("/locations/{location_id}", response_model=bool)
async def delete_location(location_id: int, session: Session = Depends(get_db_session)):
    deleted = await ConverterService(session).delete_location(location_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Location not found")
    return deleted

@router.delete("/units/{unit_id}", response_model=bool)
async def delete_unit(unit_id: int, session: Session = Depends(get_db_session)):
    deleted = await ConverterService(session).delete_unit(unit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Unit not found")
    return deleted

@router.delete("/delete_all")
async def delete_all_data(session: Session = Depends(get_db_session)):
    """Удаляет все данные из всех таблиц."""
    result = await ConverterService(session).delete_all_data()
    return result