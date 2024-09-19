from typing import List
from fastapi import APIRouter, Query, Depends
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

@router.get("/search_manuals", response_model=List[ManualSchema])
async def search_questions(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_manuals(q)

@router.get("/search_groups", response_model=List[ManualSchema])
async def search_questions(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_groups(q)

@router.get("/search_categories", response_model=List[ManualSchema])
async def search_questions(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_categories(q)

@router.put("/{manual_id}")
async def put_manual(
    manual_id: int,
    manual: ManualSchema,
    session: Session = Depends(get_db_session)
) -> ManualSchema:
    return await ManualService(session).update_manual(manual_id, manual)

@router.put("/{group_id}")
async def put_group(
    group_id: int,
    group: GroupSchema,
    session: Session = Depends(get_db_session)
) -> GroupSchema:
    return await ManualService(session).update_group(group_id, group)

@router.put("/{category_id}")
async def put_category(
    category_id: int,
    category: CategorySchema,
    session: Session = Depends(get_db_session)
) -> CategorySchema:
    return await ManualService(session).update_category(category_id, category)

# @router.delete("/{manual_id}")
# async def delete_manual(
#     manual_id: int,
#     manual: ManualSchema,
#     session: Session = Depends(get_db_session)
# ) -> ManualSchema:
#     return await ManualService(session).delete_manual(manual_id, manual)

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