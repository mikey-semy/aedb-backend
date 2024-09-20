from typing import List, Type, TypeVar, Any
import json
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from app.models.manuals import ManualModel, CategoryModel, GroupModel
from app.schemas.manuals import ManualSchema, CategorySchema, GroupSchema
from app.services.base import BaseService, BaseDataManager
from app.utils.manuals import PDFCoverExtractor

T = TypeVar("T", ManualSchema, CategorySchema, GroupSchema)
M = TypeVar("M", ManualModel, CategoryModel, GroupModel)

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
        statement = select(self.model).where(self.model.id == item_id)
        schema: T = await self.get_one(statement)
        return schema

    async def get_items_joined(self, statement=None) -> List[Any]:
        if statement is None:
            statement = select(CategoryModel).options(
                            joinedload(CategoryModel.groups)
                            .joinedload(GroupModel.manuals)
                        )
        result: List[Any] = []
        categories = await self.get_all(statement)
        for category in categories:
            category_dict = category.to_dict
            category_dict['groups'] = [
                GroupSchema(
                    **group.to_dict,
                    manuals=[
                        ManualSchema(**manual.to_dict) for manual in group.manuals
                    ]
                ) for group in category.groups
            ]
            result.append(CategorySchema(**category_dict))
        return result

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

class ManualService(BaseService):
    """
    Сервис для работы с инструкциями, категориями и группами.
    """
    def __init__(self, session):
        """
        Инициализирует ManualService.

        :param session: Сессия базы данных
        """
        super().__init__(session)
        self.manual_manager = GenericDataManager(session, ManualSchema, ManualModel)
        self.category_manager = GenericDataManager(session, CategorySchema, CategoryModel)
        self.group_manager = GenericDataManager(session, GroupSchema, GroupModel)

    async def add_item(self, item: T, manager: GenericDataManager) -> T:
        """
        Добавляет новый элемент через указанный менеджер.

        :param item: Элемент для добавления
        :param manager: Менеджер данных для использования
        :return: Добавленный элемент
        """

        if item.get('file_url'):

            item['cover_image_url'] = PDFCoverExtractor.create_url(item['file_url'])

        new_item = manager.model(**item.model_dump())
        return await manager.add_item(new_item)

    async def add_manual(self, manual: ManualSchema) -> ManualSchema:
        """
        Добавляет новую инструкцию.

        :param manual: Инструкция для добавления
        :return: Добавленная инструкция
        """
        return await self.add_item(manual, self.manual_manager)

    async def add_category(self, category: CategorySchema) -> CategorySchema:
        """
        Добавляет новую категорию.

        :param category: Категория для добавления
        :return: Добавленная категория
        """
        return await self.add_item(category, self.category_manager)

    async def add_group(self, group: GroupSchema) -> GroupSchema:
        """
        Добавляет новую группу.

        :param group: Группа для добавления
        :return: Добавленная группа
        """
        return await self.add_item(group, self.group_manager)

    async def add_all_items(self, file_path: str, manager: GenericDataManager) -> None:
        """
        Добавляет все элементы из JSON-файла.

        :param file_path: Путь к JSON-файлу
        :param manager: Менеджер данных для использования
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            items = json.load(file)
        for item in items:

            if item.get('file_url'):

                item['cover_image_url'] = PDFCoverExtractor.create_url(item['file_url'])

            new_item = manager.model(**item)
            await manager.add_item(new_item)

    async def add_all_manuals(self) -> None:
        """Добавляет все инструкции из JSON-файла."""
        await self.add_all_items('app/data/manuals/manuals.json', self.manual_manager)

    async def add_all_categories(self) -> None:
        """Добавляет все категории из JSON-файла."""
        await self.add_all_items('app/data/manuals/categories.json', self.category_manager)

    async def add_all_groups(self) -> None:
        """Добавляет все группы из JSON-файла."""
        await self.add_all_items('app/data/manuals/groups.json', self.group_manager)

    async def get_manuals_joined(self) -> List[Any]:
        """
        Получает список всех инструкций c категориями и группами.

        :return: Список инструкций
        """
        return await self.manual_manager.get_items_joined()
    
    async def get_manuals(self) -> List[ManualSchema]:
        """
        Получает список всех инструкций.

        :return: Список инструкций
        """
        return await self.manual_manager.get_items()

    async def get_categories(self) -> List[CategorySchema]:
        """
        Получает список всех категорий.

        :return: Список категорий
        """
        return await self.category_manager.get_items()

    async def get_groups(self) -> List[GroupSchema]:
        """
        Получает список всех групп.

        :return: Список групп
        """
        return await self.group_manager.get_items()

    async def search_manuals(self, q: str) -> List[ManualSchema]:
        return await self.manual_manager.search_items(q)

    async def search_categories(self, q: str) -> List[CategorySchema]:
        return await self.category_manager.search_items(q)

    async def search_groups(self, q: str) -> List[GroupSchema]:
        return await self.group_manager.search_items(q)

    async def update_manual(self, item_id: int, updated_item: ManualSchema) -> ManualSchema:
        updated_item = self.manual_manager.model(**updated_item.model_dump())
        return await self.manual_manager.update_item(item_id, updated_item)

    async def update_category(self, item_id: int, updated_item: CategorySchema) -> CategorySchema:
        updated_item = self.category_manager.model(**updated_item.model_dump())
        return await self.category_manager.update_item(item_id, updated_item)

    async def update_group(self, item_id: int, updated_item: GroupSchema) -> GroupSchema:
        updated_item = self.group_manager.model(**updated_item.model_dump())
        return await self.group_manager.update_item(item_id, updated_item)

    async def delete_manual(self, item_id: int) -> bool:
        return await self.manual_manager.delete_item(item_id)

    async def delete_category(self, item_id: int) -> bool:
        return await self.category_manager.delete_item(item_id)

    async def delete_group(self, item_id: int) -> bool:
        return await self.group_manager.delete_item(item_id)
