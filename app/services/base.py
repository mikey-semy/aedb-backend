from typing import TypeVar, Generic, Type, Any, List
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.manuals import BaseSchema, ManualSchema, CategorySchema, GroupSchema

T = TypeVar('T', bound=BaseSchema)
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
        result = await self.session.execute(delete_statement)
        print(result)
        return result.rowcount > 0

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
