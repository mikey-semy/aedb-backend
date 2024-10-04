from typing import List, Any
from fastapi import APIRouter, Query, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.manuals import ManualSchema, GroupSchema, CategorySchema
from app.services.manuals import ManualService
from app.database.session import get_db_session

router = APIRouter()

@router.get("/nested_manuals", response_model=List[Any])
async def get_nested_manuals(
    session: Session = Depends(get_db_session)
) -> List[Any]:
    return await ManualService(session).get_nested_manuals()

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
async def search_manuals(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_manuals(q)

@router.get("/search_groups", response_model=List[ManualSchema])
async def search_groups(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_groups(q)

@router.get("/search_categories", response_model=List[ManualSchema])
async def search_categories(
    q: str = Query(..., min_length=3),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_categories(q)

@router.put("/manual/{manual_id}")
async def put_manual(
    manual_id: int,
    manual: ManualSchema,
    session: Session = Depends(get_db_session)
) -> ManualSchema:
    return await ManualService(session).update_manual(manual_id, manual)

@router.put("/group/{group_id}")
async def put_group(
    group_id: int,
    group: GroupSchema,
    session: Session = Depends(get_db_session)
) -> GroupSchema:
    return await ManualService(session).update_group(group_id, group)

@router.put("/category/{category_id}")
async def put_category(
    category_id: int,
    category: CategorySchema,
    session: Session = Depends(get_db_session)
) -> CategorySchema:
    return await ManualService(session).update_category(category_id, category)

@router.delete("/manual/{manual_id}")
async def delete_manual(
    manual_id: int,
    session: Session = Depends(get_db_session)
) -> bool:
    return await ManualService(session).delete_manual(manual_id)

@router.delete("/manuals")
async def delete_manuals(
    session: Session = Depends(get_db_session)
) -> bool:
    return await ManualService(session).delete_manuals()

@router.delete("/group/{group_id}")
async def delete_group(
    group_id: int,
    session: Session = Depends(get_db_session)
) -> bool:
    return await ManualService(session).delete_group(group_id)

@router.delete("/category/{category_id}")
async def delete_category(
    category_id: int,
    session: Session = Depends(get_db_session)
) -> bool:
    return await ManualService(session).delete_category(category_id)

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

@router.post("/upload_manual")
async def create_upload_manuals(
    manual: UploadFile,
    session: Session = Depends(get_db_session)):
    return await ManualService(session).upload_file(manual)

@router.post("/add_groups")
async def add_groups(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_groups()

@router.post("/add_categories")
async def add_categories(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_categories()

@router.post("/add_manuals")
async def add_manuals(
    session: Session = Depends(get_db_session)
) -> None:
    await ManualService(session).add_all_manuals()
