from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db_session
router = APIRouter()

@router.get("/api/menu-items", response_model=List[MenuItemsSchema])
async def get_menu_items(
    session: Session = Depends(get_db_session)
) -> List[MenuItemsSchema]:
    return await MenuItemsService(session).get_menu_items()