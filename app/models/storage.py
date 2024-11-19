from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SQLModel

class StorageLocationModel(SQLModel):
    __tablename__ = 'locations'
    
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    place: Mapped[Optional[str]] = mapped_column(default=None)
    used_place: Mapped[Optional[str]] = mapped_column(default=None)
    new_place: Mapped[Optional[str]] = mapped_column(default=None)

    equipment: Mapped[list["StorageEquipmentModel"]] = relationship(back_populates="location")
    
class StorageEquipmentModel(SQLModel):
    __tablename__ = 'equipment'

    id: Mapped[Optional[int]] = mapped_column(primary_key=True, index=True)
    group: Mapped[str]
    name: Mapped[Optional[str]] = mapped_column(default=None)
    specs: Mapped[Optional[str]] = mapped_column(default=None)
    qty: Mapped[int]
    install: Mapped[Optional[str]] = mapped_column(default=None)
    number: Mapped[Optional[str]] = mapped_column(default=None)
    notes: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column("created_at", default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column("updated_at", default=datetime.now, onupdate=datetime.now)
    
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), nullable=False)
    location: Mapped["StorageLocationModel"] = relationship(back_populates="equipment")
