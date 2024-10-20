"""
Модуль, содержащий модели данных для настройки скоростей моталки.

Этот модуль определяет следующие модели SQLAlchemy:
- ReelModel: представляет моталку
- RollModel: представляет формирующий ролик моталки
- SpeedModel: представляет параметры скоростей формирующего ролика моталки

Каждая модель наследуется от базового класса SQLModel и определяет 
соответствующие поля и отношения между таблицами базы данных.

Модели используют типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с инструкциями по эксплуатации.
"""
from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import MetaData, String, ForeignKey, DateTime, Float, Integer, Boolean

import pytz


from app.models.base import SQLModel

moscow_tz = pytz.timezone('Europe/Moscow')

class ReelModel(SQLModel):
    """
    Модель для представления категории инструкций.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название моталки.
        rolls (relationship): Формирующие ролики, относящиеся к этой категории.

    Methods:
        __init__(id: int, name: str) -> None: Инициализирует объект ReelModel.
        __repr__() -> str: Возвращает строковое представление объекта ReelModel.
        __str__() -> str: Возвращает строковое представление объекта ReelModel.

    Raises:
        ValueError: Если id или name не являются допустимыми значениями.

    Examples:
        >>> reel = ReelModel(id=1, name="Моталка 1")
        >>> print(reel.name)
        Моталка 1
    """
    __tablename__ = "reels"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("reel_name", String(100))

    rolls: Mapped[List["RollModel"]] = relationship("RollModel", back_populates="reel")

class RollModel(SQLModel):
    """
    Модель для представления формирующих роликов.

    Attributes:
        id (int): Уникальный идентификатор формирующего ролика.
        name (str): Название формирующего ролика.
        reel_id (int): ID моталки, к которой относится формирующий ролик.
        reel (relationship): Моталка, к которой относится формирующий ролик.
        speeds (relationship): Параметры скорости, относящиеся к этому формирующему ролику.

    Methods:
        __init__(id: int, name: str, reel_id: int) -> None: Инициализирует объект RollModel.
        __repr__() -> str: Возвращает строковое представление объекта RollModel.
        __str__() -> str: Возвращает строковое представление объекта RollModel.

    Raises:
        ValueError: Если id, name или reel_id не являются допустимыми значениями.

    Examples:
        >>> roll = RollModel(id=1, name="Формирующий ролик 1", reel_id=1)
        >>> print(roll.name)
        Формирующий ролик 1
    """
    __tablename__ = "rolls"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("roll_name", String(100))
    reel_id: Mapped["int"] = mapped_column(ForeignKey(ReelModel.id, ondelete="CASCADE"))
        
    reel: Mapped["ReelModel"] = relationship("ReelModel", back_populates="rolls")
    speeds: Mapped[List["SpeedModel"]] = relationship("SpeedModel", back_populates="rolls")

class SpeedModel(SQLModel):
    """
    Модель для представления параметров скорости формирующего ролика моталки.

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
        roll (relationship): Формирующий ролик, к которому относится этот параметр скорости.
    """
    __tablename__ = "speeds"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    task: Mapped[float] = mapped_column(Float, nullable=False, comment='50.19')
    tspd: Mapped[int] = mapped_column(Integer, nullable=False, comment='10')
    fspd: Mapped[bool] = mapped_column(Boolean, nullable=False, comment='False')
    bmav: Mapped[int] = mapped_column(Integer, nullable=False, comment='496')
    bemf: Mapped[float] = mapped_column(Float, nullable=False, comment='117.8')
    amav: Mapped[int] = mapped_column(Integer, nullable=False, comment='501')
    aemf: Mapped[float] = mapped_column(Float, nullable=False, comment='119')
    memf: Mapped[float] = mapped_column(Float, nullable=False, comment='118.76')
    corr: Mapped[bool] = mapped_column(Boolean, nullable=False, comment='True')
    created_at: Mapped[datetime] = mapped_column("created_at", default=lambda: datetime.now(moscow_tz))
    updated_at: Mapped[datetime] = mapped_column("updated_at", default=lambda: datetime.now(moscow_tz), onupdate=lambda: datetime.now(moscow_tz))
    roll: Mapped["RollModel"] = relationship("RollModel", back_populates="speeds")
    roll_id: Mapped[int] = mapped_column(ForeignKey(RollModel.id, ondelete="CASCADE"))
