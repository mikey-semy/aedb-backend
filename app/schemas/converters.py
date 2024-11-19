from typing import Optional
from app.schemas.base import BaseSchema

class MillShopSchema(BaseSchema):
    """
    Схема для представления цеха.
    
    Attributes:
        id: Уникальный идентификатор цеха
        name: Название цеха
    """
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class ProductionLineSchema(BaseSchema):
    """
    Схема для представления производственной линии.
    
    Attributes:
        id: Уникальный идентификатор линии
        name: Название линии
        mill_shop_id: ID цеха, к которому относится линия
    """
    id: Optional[int] = None
    name: str
    mill_shop_id: int

    class Config:
        from_attributes = True

class LocationSchema(BaseSchema):
    """
    Схема для представления помещения.
    
    Attributes:
        id: Уникальный идентификатор помещения
        name: Название помещения
        production_line_id: ID линии, к которой относится помещение
    """
    id: Optional[int] = None
    name: str
    production_line_id: int

    class Config:
        from_attributes = True

class CabinetSchema(BaseSchema):
    """
    Схема для представления шкафа.
    
    Attributes:
        id: Уникальный идентификатор шкафа
        name: Название шкафа
        location_id: ID помещения, где находится шкаф
    """
    id: Optional[int] = None
    name: str
    location_id: int

    class Config:
        from_attributes = True

class ConverterSchema(BaseSchema):
    """
    Схема для представления преобразователя частоты.
    
    Attributes:
        id: Уникальный идентификатор преобразователя
        cabinet_id: ID шкафа, где установлен преобразователь
        brand: Производитель
        model: Модель
        nominal_current: Номинальный ток
        current_type: Тип тока
        power: Мощность
        input_voltage: Входное напряжение
        output_voltage: Выходное напряжение
    """
    id: Optional[int] = None
    cabinet_id: int
    brand: str
    model: str
    nominal_current: Optional[float]
    current_type: Optional[str]
    power: Optional[float]
    input_voltage: Optional[float]
    output_voltage: Optional[float]

    class Config:
        from_attributes = True

class UnitSchema(BaseSchema):
    """
    Схема для представления агрегата.
    
    Attributes:
        id: Уникальный идентификатор агрегата
        name: Название агрегата
        converter_id: ID преобразователя частоты
    """
    id: Optional[int] = None
    name: str
    converter_id: int

    class Config:
        from_attributes = True
