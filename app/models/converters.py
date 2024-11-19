from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SQLModel

class MillShopModel(SQLModel):
    __tablename__ = 'mill_shops'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    
    production_lines: Mapped[list["ProductionLineModel"]] = relationship(back_populates="mill_shop")

class ProductionLineModel(SQLModel):
    __tablename__ = 'production_lines'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True) 
    mill_shop_id: Mapped[int] = mapped_column(ForeignKey("mill_shops.id"))
    name: Mapped[str]

    mill_shop: Mapped["MillShopModel"] = relationship(back_populates="production_lines")
    locations: Mapped[list["LocationModel"]] = relationship(back_populates="production_line")

class LocationModel(SQLModel):
    __tablename__ = 'locations'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    production_line_id: Mapped[int] = mapped_column(ForeignKey("production_lines.id"))
    name: Mapped[str]

    production_line: Mapped["ProductionLineModel"] = relationship(back_populates="locations")
    cabinets: Mapped[list["CabinetModel"]] = relationship(back_populates="location")

class CabinetModel(SQLModel):
    __tablename__ = 'cabinets'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    name: Mapped[str]

    location: Mapped["LocationModel"] = relationship(back_populates="cabinets")
    converters: Mapped[list["ConverterModel"]] = relationship(back_populates="cabinet")

class ConverterModel(SQLModel):
    __tablename__ = 'converters'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cabinet_id: Mapped[int] = mapped_column(ForeignKey("cabinets.id"))
    brand: Mapped[str]
    model: Mapped[str]
    nominal_current: Mapped[Optional[float]]
    current_type: Mapped[Optional[str]]
    power: Mapped[Optional[float]]
    input_voltage: Mapped[Optional[float]]
    output_voltage: Mapped[Optional[float]]

    cabinet: Mapped["CabinetModel"] = relationship(back_populates="converters")
    units: Mapped[list["UnitModel"]] = relationship(back_populates="converter")

class UnitModel(SQLModel):
    __tablename__ = 'units'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    converter_id: Mapped[int] = mapped_column(ForeignKey("converters.id"))
    
    converter: Mapped["ConverterModel"] = relationship(back_populates="units")
