from typing import Optional
from app.schemas.base import BaseSchema

class StorageLocationSchema(BaseSchema):
    """
    Схема для представления места хранения.
    
    Attributes:
        id: Уникальный идентификатор места
        name: Название места
        place: Место на складе
        used_place: Используемое место
        new_place: Новое место
    """
    id: Optional[int] = None
    name: str
    place: Optional[str]
    used_place: Optional[str] 
    new_place: Optional[str]

    class Config:
        from_attributes = True

class StorageEquipmentSchema(BaseSchema):
    """
    Схема для представления оборудования на складе.
    
    Attributes:
        id: Уникальный идентификатор оборудования
        group: Группа оборудования
        name: Название
        specs: Характеристики
        qty: Количество
        install: Место установки
        number: Номер
        notes: Примечания
        created_at: Дата создания
        updated_at: Дата обновления
        location_id: ID места хранения
    """
    id: Optional[int] = None
    group: str
    name: Optional[str]
    specs: Optional[str]
    qty: int
    install: Optional[str]
    number: Optional[str]
    notes: Optional[str]
    location_id: int

    class Config:
        from_attributes = True
