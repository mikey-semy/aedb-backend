from typing import TypeVar, Generic, Type, Any, List
import logging
from sqlalchemy import select, delete
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.base import SQLModel
from app.schemas.manuals import (
    BaseSchema,
    ManualSchema,
    CategorySchema,
    GroupSchema
    )

M = TypeVar("M", bound=SQLModel)
T = TypeVar("T", bound=BaseSchema)

class SessionMixin:
    """
    Миксин для предоставления экземпляра сессии базы данных.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализирует SessionMixin.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

class BaseService(SessionMixin):
    """
    Базовый класс для сервисов приложения.
    """

class BaseDataManager(SessionMixin, Generic[T]):
    """
    Базовый класс для менеджеров данных с поддержкой обобщенных типов.
    """
    def __init__(self, session:AsyncSession, schema: Type[T]):
        """
        Инициализирует BaseDataManager.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            schema (Type[T]): Тип схемы данных.
        """
        super().__init__(session)
        self.schema = schema

    async def add_one(self, model: Any) -> T:
        """
        Добавляет одну запись в базу данных.

        Args:
            model (Any): Модель для добавления.

        Returns:
            T: Добавленная запись в виде схемы.
        """
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self.schema(**model.to_dict)

    async def update_one(self, model_to_update, updated_model: Any) -> T | None:
        """
        Обновляет одну запись в базе данных.

        Args:
            model_to_update: Модель для обновления.
            updated_model (Any): Обновленная модель.

        Returns:
            T | None: Обновленная запись в виде схемы или None, если запись не найдена.
        """
        if model_to_update:
            updated_model_dict = updated_model.to_dict
            for key, value in updated_model_dict.items():
                if key != "id":
                    setattr(model_to_update, key, value)
        else:
            return None
        await self.session.commit()
        await self.session.refresh(model_to_update)
        return self.schema(**model_to_update.to_dict)

    async def delete_one(self, delete_statement: Executable) -> bool:
        """
        Удаляет одну запись из базы данных.

        Args:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если запись удалена, False в противном случае.
        """
        try:
            delete_statement = delete_statement.limit(1)
            result = await self.session.execute(delete_statement)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при удалении: %s", e)
            return False

    async def delete_all(self, delete_statement: Executable) -> bool:
        """
        Удаляет все записи из базы данных, соответствующие заданному запросу.

        Args:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если записи удалены, False в противном случае.
        """
        try:
            result = await self.session.execute(delete_statement)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при удалении: %s", e)
            return False

    async def get_one(self, select_statement: Executable) -> Any | None:
        """
        Получает одну запись из базы данных.

        Args:
            select_statement (Executable): SQL-запрос для выборки.

        Returns:
            Any | None: Полученная запись или None, если запись не найдена.
        """
        result = await self.session.execute(select_statement)
        return result.scalar()

    async def get_all(self, select_statement: Executable) -> List[Any]:
        """
        Получает все записи из базы данных по заданному запросу.

        Args:
            select_statement (Executable): SQL-запрос для выборки.

        Returns:
            List[Any]: Список полученных записей.
        """
        result = await self.session.execute(select_statement)
        return list(result.unique().scalars().all())

class ManualDataManager(BaseDataManager[ManualSchema]):
    """
    Менеджер данных для работы с руководствами.
    Наследует функциональность от BaseDataManager с использованием ManualSchema.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализирует ManualDataManager.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        super().__init__(session, ManualSchema)

class GroupDataManager(BaseDataManager[GroupSchema]):
    """
    Менеджер данных для работы с группами.
    Наследует функциональность от BaseDataManager с использованием GroupSchema.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализирует GroupDataManager.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        super().__init__(session, GroupSchema)

class CategoryDataManager(BaseDataManager[CategorySchema]):
    """
    Менеджер данных для работы с категориями.
    Наследует функциональность от BaseDataManager с использованием CategorySchema.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализирует CategoryDataManager.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        super().__init__(session, CategorySchema)



class GenericDataManager(BaseDataManager[T]):
    """
    Обобщенный менеджер данных для работы с различными типами схем и моделей.
    """

    def __init__(self, session, schema: Type[T], model: Type[M]):
        """
        Инициализирует GenericDataManager.

        :param session: Сессия базы данных
        :param schema: Тип схемы
        :param model: Тип модели
        """
        super().__init__(session, schema)
        self.model = model

    async def add_item(self, new_item) -> T:
        """
        Добавляет новый элемент в базу данных.

        :param new_item: Новый элемент для добавления
        :return: Добавленный элемент в виде схемы
        """
        return await self.add_one(new_item)

    async def get_item(self, item_id: int) -> T | None:
        """
        Получает объект модели по заданному идентификатору.

        Args:
            item_id (int): Идентификатор объекта для получения.

        Returns:
            T | None: Объект модели или None, если объект не найден.
        """
        statement = select(self.model).where(self.model.id == item_id)
        schema: T = await self.get_one(statement)
        return schema
    
    async def get_items(self, statement=None) -> List[T]:
        """
        Получает список элементов из базы данных.

        :param statement: SQL-выражение для выборки (опционально)
        :return: Список элементов в виде схем
        """
        if statement is None:
            statement = select(self.model)
        schemas: List[T] = []
        models = await self.get_all(statement)
        for model in models:
            schemas.append(self.schema(**model.to_dict))
        return schemas
  
    async def search_items(self, q: str) -> List[T]:
        """
        Выполняет поиск объектов модели по заданной строке.

        Args:
            q (str): Строка для поиска.

        Returns:
            List[T]: Список найденных объектов модели.
        """
        if hasattr(M, 'title'):
            statement = select(self.model).where(self.model.title.ilike(f"%{q}%"))
        elif hasattr(M, 'name'):
            statement = select(self.model).where(self.model.name.ilike(f"%{q}%"))
        else:
            raise AttributeError("Модель не имеет атрибута 'title' или 'name'.")
        return await self.get_items(statement)

    async def update_item(self,
                              item_id: int,
                              updated_item: T) -> T | None:
        """
        Обновляет объект модели по заданному идентификатору.

        Args:
            item_id (int): Идентификатор объекта для обновления.
            updated_item (T): Обновлённый объект модели.

        Returns:
            T | None: Обновлённый объект модели или None, если объект не найден.
        """
        old_item = await self.get_item(item_id)
        schema: T = await self.update_one(old_item, updated_item)
        return schema

    async def delete_item(self, item_id: int) -> bool:
        """
        Удаляет элемент из базы данных.
        :param item_id: Идентификатор элемента
        :return: True, если элемент успешно удален, иначе False
        """
        statement = delete(self.model).where(self.model.id == item_id)
        return await self.delete_one(statement)

    async def delete_items(self) -> bool:
        """
        Удаляет элементы из базы данных.
        :return: True, если элементы успешно удалены, иначе False
        """
        statement = delete(self.model)
        return await self.delete_all(statement)
    
    async def get_by_name(self, name: str):
        statement = select(self.model).where(self.model.name == name)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
