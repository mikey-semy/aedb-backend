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
        rools (relationship): формирующие ролики.
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
        id (int): Уникальный идентификатор группы.
        name (str): Название формирующего ролика.
        reel_id (int): ID моталки, к которой относится формирующий ролик.
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
        id (int): Уникальный идентификатор инструкции.

        group_id (int): ID группы, к которой относится инструкция.
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
