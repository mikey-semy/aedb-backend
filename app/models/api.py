from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import MetaData, String

from app.models.base import SQLModel

class MenuItemsModel(SQLModel):
    """
    Модель для представления категории инструкций.

    Attributes:
        id (int): Уникальный идентификатор.
        title (str): Название.
        url (str): URL.
    """
    __tablename__ = "menu"

    metadata = MetaData()

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    title: Mapped[str] = mapped_column("title", String(100))
    url: Mapped[str] = mapped_column("url", default="#")

