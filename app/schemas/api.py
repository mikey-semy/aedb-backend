from typing import Optional
from app.schemas.base import BaseSchema

class MenuItemsSchema(BaseSchema):
    """
    Схема для представления меню.

    Attributes:
        id: Уникальный идентификатор.
        title: Название.
        url: URL.
    """
    id: Optional[int] = None
    title: str
    url: str
    
    class Config:
        from_attributes = True