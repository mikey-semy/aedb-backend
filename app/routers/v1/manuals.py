from typing import List, Any
from fastapi import APIRouter, Query, Depends, UploadFile
from sqlalchemy.orm import Session
from app.schemas.auth import UserSchema
from app.schemas.manuals import (
    ManualSchema,
    GroupSchema,
    CategorySchema,
)
from app.services.manuals import ManualService
from app.services.auth import get_current_user
from app.database.session import get_db_session
from app.const import manual_params

router = APIRouter(**manual_params)

@router.get("/nested", response_model=List[Any])
async def get_nested_manuals(
    # _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> List[Any]:
    return await ManualService(session).get_nested_manuals()

@router.get("/", response_model=List[ManualSchema])
async def get_manuals(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> List[ManualSchema]:
    return await ManualService(session).get_manuals()

@router.get("/groups/{category_id}", response_model=List[GroupSchema])
async def get_groups_by_category(
    category_id: int,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> List[GroupSchema]:
    return await ManualService(session).get_groups_by_category(category_id)

@router.get("/groups", response_model=List[GroupSchema])
async def get_groups(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> List[GroupSchema]:
    return await ManualService(session).get_groups()

@router.get("/categories", response_model=List[CategorySchema])
async def get_categories(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> List[CategorySchema]:
    return await ManualService(session).get_categories()

@router.get("/search", response_model=List[ManualSchema])
async def search_manuals(
    q: str = Query(..., min_length=3),
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_manuals(q)

@router.get("/search_groups", response_model=List[ManualSchema])
async def search_groups(
    q: str = Query(..., min_length=3),
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_groups(q)

@router.get("/search_categories", response_model=List[ManualSchema])
async def search_categories(
    q: str = Query(..., min_length=3),
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session)):
    return await ManualService(session).search_categories(q)

@router.put("/{manual_id}")
async def put_manual(
    manual_id: int,
    manual: ManualSchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session)
) -> ManualSchema:
    return await ManualService(session).update_manual(manual_id, manual)

@router.put("/group/{group_id}")
async def put_group(
    group_id: int,
    group: GroupSchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> GroupSchema:
    return await ManualService(session).update_group(group_id, group)

@router.put("/category/{category_id}")
async def put_category(
    category_id: int,
    category: CategorySchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CategorySchema:
    return await ManualService(session).update_category(category_id, category)

@router.delete("/{manual_id}")
async def delete_manual(
    manual_id: int,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> bool:
    return await ManualService(session).delete_manual(manual_id)

@router.delete("/")
async def delete_manuals(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> bool:
    return await ManualService(session).delete_manuals()

@router.delete("/group/{group_id}")
async def delete_group(
    group_id: int,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> bool:
    return await ManualService(session).delete_group(group_id)

@router.delete("/category/{category_id}")
async def delete_category(
    category_id: int,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> bool:
    return await ManualService(session).delete_category(category_id)

@router.post("/group")
async def post_group(
    group: GroupSchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> GroupSchema:
    return await ManualService(session).add_group(group)

@router.post("/category")
async def post_category(
    category: CategorySchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> CategorySchema:
    return await ManualService(session).add_category(category)

@router.post("/")
async def post_manual(
    manual: ManualSchema,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> ManualSchema:
    return await ManualService(session).add_manual(manual)

@router.post("/upload")
async def create_upload_manuals(
    manual: UploadFile,
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
    ):
    return await ManualService(session).upload_file(manual)

@router.post("/add_groups")
async def add_groups(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> None:
    """Adds all groups from JSON file."""
    await ManualService(session).add_all_groups()

@router.post("/add_categories")
async def add_categories(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> None:
    """Adds all categories from JSON file."""
    await ManualService(session).add_all_categories()

@router.post("/add_all")
async def add_manuals(
    _user: UserSchema = Depends(get_current_user),
    session: Session = Depends(get_db_session),
) -> None:
    """Adds all manuals from JSON file."""
    await ManualService(session).add_all_manuals()
