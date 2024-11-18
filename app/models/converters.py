"""
Модуль, содержащий модели данных по преобразователям частоты.

Этот модуль определяет следующие модели SQLAlchemy:
- MillShopModel: представляет цех
- ProductionLineModel: представляет продразделение/группу
- LocationModel: представляет помещение
- CabinetModel: представляет шкаф
- ConverterModel: представляет преобразователь частоты
- UnitModel: представляет агрегат, использующий преобразователь частоты
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SQLModel


class MillShopModel(SQLModel):
    __tablename__ = 'mill_shops'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("name", nullable=False)
    
    production_lines: Mapped[list["ProductionLineModel"]] = relationship(back_populates="mill_shop")
class ProductionLineModel(SQLModel):
    __tablename__ = 'production_lines'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    mill_shop_id: Mapped[int] = mapped_column(ForeignKey("mill_shops.id"), nullable=False)
    name: Mapped[str] = mapped_column("name", nullable=False)

    mill_shop: Mapped["MillShopModel"] = relationship(back_populates="production_lines")
    locations: Mapped[list["LocationModel"]] = relationship(back_populates="production_line")


class LocationModel(SQLModel):
    __tablename__ = 'locations'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    production_line_id: Mapped[int] = mapped_column(ForeignKey("production_lines.id"), nullable=False)
    name: Mapped[str] = mapped_column("name", nullable=False)

    production_line: Mapped["ProductionLineModel"] = relationship(back_populates="locations")
    cabinets: Mapped[list["CabinetModel"]] = relationship(back_populates="location")
    
class CabinetModel(SQLModel):
    __tablename__ = 'cabinets'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    name: Mapped[str] = mapped_column("name", nullable=False)

    location: Mapped["LocationModel"] = relationship(back_populates="cabinets")
    converters: Mapped[list["ConverterModel"]] = relationship(back_populates="cabinet")
    
class ConverterModel(SQLModel):
    __tablename__ = 'converters'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    cabinet_id: Mapped[int] = mapped_column(ForeignKey("cabinets.id"), nullable=False)  # Шкаф, в котором установлен конвертер
    brand: Mapped[str] = mapped_column("brand", nullable=False)                         # Бренд
    model: Mapped[str] = mapped_column("model", nullable=False)                         # Модель
    nominal_current: Mapped[float] = mapped_column("nominal_current", nullable=False)   # Номинальный ток (вых)
    current_type: Mapped[str] = mapped_column("current_type", nullable=False)           # Тип тока
    power: Mapped[float] = mapped_column("power", nullable=False)                       # Мощность
    input_voltage: Mapped[float] = mapped_column("input_voltage", nullable=False)       # Напряжение (питающие)
    output_voltage: Mapped[float] = mapped_column("output_voltage", nullable=False)     # Напряжение (вых)
    
    cabinet: Mapped["CabinetModel"] = relationship(back_populates="converters")
    units: Mapped[list["UnitModel"]] = relationship(back_populates="converter")

class UnitModel(SQLModel):
    __tablename__ = 'units'
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("name", nullable=False)
    converter_id: Mapped[int] = mapped_column(ForeignKey("converters.id"), nullable=False)
    
    converter: Mapped["ConverterModel"] = relationship(back_populates="units")