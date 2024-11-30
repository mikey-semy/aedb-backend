from typing import Optional, List
from fastapi import UploadFile
from app.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    """
    Схема для представления категории инструкций.

    Attributes:
        id: Уникальный идентификатор категории.
        name: Название категории.
        logo_url: URL логотипа категории.
    """
    id: Optional[int] = None
    name: str
    logo_url: str
    class Config:
        from_attributes = True

class GroupSchema(BaseSchema):
    """
    Схема для представления группы инструкций.

    Attributes:
        id: Уникальный идентификатор группы.
        name: Название группы.
        category_id: ID категории, к которой относится группа.
    """
    id: Optional[int] = None
    name: str
    category_id: int
    class Config:
        from_attributes = True

class ManualSchema(BaseSchema):
    """
    Схема для представления инструкции.

    Attributes:
        id: Уникальный идентификатор инструкции.
        title: Название инструкции.
        file_url: URL для доступа к файлу инструкции.
        cover_image_url: URL изображения обложки инструкции.
        category_id: ID категории, к которой относится инструкция.
        group_id: ID группы, к которой относится инструкция.
    """
    id: Optional[int] = None
    title: str
    file_url: str
    group_id: int
    class Config:
        from_attributes = True

class ManualFileSchema(BaseSchema):
    """
    Схема для представления инструкции, загруженной из файла.

    Attributes:
        id: Уникальный идентификатор инструкции.
        title: Название инструкции.
        file: Файл инструкции.
        category_id: ID категории, к которой относится инструкция.
        group_id: ID группы, к которой относится инструкция.
    """
    id: Optional[int] = None
    title: str
    file: UploadFile
    category_id: int
    group_id: int
    class Config:
        from_attributes = True
        
class ManualNestedSchema(BaseSchema):
    id: Optional[int] = None
    title: str
    file_url: str
    group_id: int

class GroupNestedSchema(BaseSchema):
    id: Optional[int] = None
    name: str
    manuals: List[ManualNestedSchema]

class CategoryNestedSchema(BaseSchema):
    id: Optional[int] = None
    name: str
    logo_url: str
    groups: List[GroupNestedSchema]

class ManualListItemSchema(BaseSchema):
    """
    Схема для представления элемента списка инструкций.

    Attributes:
        category_name: Название категории
        group_name: Название группы
        manual_name: Название инструкции.
        manual_url: Ссылка на инструкцию.
    """
    category_name: str
    group_name: str
    manual_name: str
    manual_url: str
