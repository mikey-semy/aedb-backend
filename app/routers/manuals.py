from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.manuals import ManualSchema, GroupSchema, CategorySchema
from app.services.manuals import ManualService
from app.database.session import get_db_session

router = APIRouter()

@router.get("/manuals", response_model=List[ManualSchema])
async def get_manuals(
    session: Session = Depends(get_db_session)
) -> List[ManualSchema]:
    return await ManualService(session).get_manuals()

@router.get("/groups", response_model=List[GroupSchema])
async def get_groups(
    session: Session = Depends(get_db_session)
) -> List[GroupSchema]:
    return await ManualService(session).get_groups()

@router.get("/categories", response_model=List[CategorySchema])
async def get_categories(
    session: Session = Depends(get_db_session)
) -> List[CategorySchema]:
    return await ManualService(session).get_categories()

@router.post("/group")
async def post_group(
    group: GroupSchema,
    session: Session = Depends(get_db_session)
) -> GroupSchema:
    return await ManualService(session).add_group(group)

@router.post("/category")
async def post_category(
    category: CategorySchema,
    session: Session = Depends(get_db_session)
) -> CategorySchema:
    return await ManualService(session).add_category(category)

@router.post("/manual")
async def post_manual(
    manual: ManualSchema,
    session: Session = Depends(get_db_session)
) -> ManualSchema:
    return await ManualService(session).add_manual(manual)

@router.post("/add_all_groups")
async def add_all_groups(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_groups()

@router.post("/add_all_categories")
async def add_all_categories(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_categories()

@router.post("/add_all_manuals")
async def add_all_manuals(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_manuals()