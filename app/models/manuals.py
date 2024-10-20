"""
Модуль, содержащий модели данных для работы с инструкциями по эксплуатации.

Этот модуль определяет следующие модели SQLAlchemy:
- ManualModel: представляет инструкцию по эксплуатации
- CategoryModel: представляет категорию инструкций
- GroupModel: представляет группу инструкций

Каждая модель наследуется от базового класса SQLModel и определяет 
соответствующие поля и отношения между таблицами базы данных.

Модели используют типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с инструкциями по эксплуатации.
"""
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from app.models.base import SQLModel

class CategoryModel(SQLModel):
    """
    Модель для представления категории инструкций.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории.
        logo_url (str): URL логотипа категории.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("category_name", String(100))
    logo_url: Mapped[str] = mapped_column("logo_url", default="/media/manuals/default-logo.png")

    groups: Mapped[List["GroupModel"]] = relationship("GroupModel", back_populates="category")

class GroupModel(SQLModel):
    """
    Модель для представления группы инструкций.

    Attributes:
        id (int): Уникальный идентификатор группы.
        name (str): Название группы.
        category_id (int): ID категории, к которой относится группа.
    """
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("group_name", String(100))
    category_id: Mapped["int"] = mapped_column(ForeignKey(CategoryModel.id, ondelete="CASCADE"))
    
    category: Mapped["CategoryModel"] = relationship("CategoryModel", back_populates="groups")
    manuals: Mapped[List["ManualModel"]] = relationship("ManualModel", back_populates="groups")

class ManualModel(SQLModel):
    """
    Модель для представления инструкции по эксплуатации.

    Attributes:
        id (int): Уникальный идентификатор инструкции.
        title (str): Название инструкции.
        file_url (str): URL для скачивания/открытия файла инструкции.
        cover_image_url (str): URL изображения обложки инструкции.
        group_id (int): ID группы, к которой относится инструкция.
    """
    __tablename__ = "manuals"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    title: Mapped[str] = mapped_column("title", String(200))
    file_url: Mapped[str] = mapped_column("file_url", String)
    groups: Mapped["GroupModel"] = relationship("GroupModel", back_populates="manuals")
    group_id: Mapped[int] = mapped_column(ForeignKey(GroupModel.id, ondelete="CASCADE"))
