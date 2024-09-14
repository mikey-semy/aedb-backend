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
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import MetaData, String, ForeignKey
from sqlalchemy.orm import declared_attr
from app.models.base import SQLModel


class ManualModel(SQLModel):
    """
    Модель для представления инструкции по эксплуатации.

    Attributes:
        id (int): Уникальный идентификатор инструкции.
        title (str): Название инструкции.
        file_url (str): URL для скачивания/открытия файла инструкции.
        cover_image_url (str): URL изображения обложки инструкции.
        category_id (int): ID категории, к которой относится инструкция.
        group_id (int): ID группы, к которой относится инструкция.
    """
    __tablename__ = "manuals"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    title: Mapped[str] = mapped_column("title", String(200))
    file_url: Mapped[str] = mapped_column("file_url")
    cover_image_url: Mapped[str] = mapped_column("cover_image_url")
    #category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    #group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    
    @declared_attr
    def category_id(cls):
        return mapped_column(ForeignKey("category.id", use_alter=True, name="fk_manual_category"))


    @declared_attr
    def group_id(cls):
        return mapped_column(ForeignKey("groups.id", use_alter=True, name="fk_manual_group"))

class CategoryModel(SQLModel):
    """
    Модель для представления категории инструкций.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории.
        logo_url (str): URL логотипа категории.
    """
    __tablename__ = "categories"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("category_name", String(100))
    logo_url: Mapped[str] = mapped_column("logo_url")


class GroupModel(SQLModel):
    """
    Модель для представления группы инструкций.

    Attributes:
        id (int): Уникальный идентификатор группы.
        name (str): Название группы.
        category_id (int): ID категории, к которой относится группа.
    """
    __tablename__ = "groups"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("group_name", String(100))
    #category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    @declared_attr
    def category_id(cls):
        return mapped_column(ForeignKey("category.id", use_alter=True, name="fk_group_category"))
