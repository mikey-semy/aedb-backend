from typing import Optional, List
from pydantic import datetime
from app.schemas.base import BaseSchema


class ReelSchema(BaseSchema):
    """
    Схема для представления моталки.

    Attributes:
        id (int): Уникальный идентификатор моталки.
        name (str): Название моталки.
    """
    id: Optional[int] = None
    name: str
    class Config:
        from_attributes = True

class RollSchema(BaseSchema):
    """
    Схема для представления формирующих роликов моталки.

    Attributes:
        id (int): Уникальный идентификатор формирующего ролика.
        name (str): Название формирующего ролика.
        reel_id (int): ID моталки, к которой относится формирующий ролик.
    """
    id: Optional[int] = None
    name: str
    reel_id: int
    class Config:
        from_attributes = True

class SpeedSchema(BaseSchema):
    """
    Схема для представления параметров скорости формирующего ролика моталки.

    Attributes:
        id (int): Уникальный идентификатор параметра скорости.
        task (float): Задача, для которой определяется параметр скорости.
        tspd (int): Текущая скорость.
        fspd (bool): Флаг, указывающий на то, что скорость является фиксированной.
        bmav (int): Базовая скорость.
        bemf (float): Базовый электромагнитный момент.
        amav (int): Активная скорость.
        aemf (float): Активный электромагнитный момент.
        memf (float): Максимальный электромагнитный момент.
        corr (bool): Флаг, указывающий на то, что скорость является корректированной.
        created_at (datetime): Дата и время создания параметра скорости.
        updated_at (datetime): Дата и время последнего обновления параметра скорости.
    """
    id: Optional[int] = None
    task: float
    tspd: int
    fspd: bool
    bmav: int
    bemf: float
    amav: int
    aemf: float
    memf: float
    corr: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SpeedNestedSchema(BaseSchema):
    id: Optional[int] = None
    task: float
    tspd: int
    fspd: bool
    bmav: int
    bemf: float
    amav: int
    aemf: float
    memf: float
    corr: bool
    created_at: datetime
    updated_at: datetime
    roll_id: int

class RollNestedSchema(BaseSchema):
    id: Optional[int] = None
    name: str
    speeds: List[SpeedNestedSchema]

class ReelNestedSchema(BaseSchema):
    id: Optional[int] = None
    name: str
    rolls: List[RollNestedSchema]
