from typing import List, Type, TypeVar
import json
from sqlalchemy import select
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
        print(f"Проверка наличия file_url: {item.get('file_url')}")
        if item.get('file_url'):
            print(f"Был item['cover_image_url']: {item['cover_image_url']}")
            item['cover_image_url'] = PDFCoverExtractor.create_url(item['file_url'])
            print(f"Стал item['cover_image_url']: {item['cover_image_url']}")
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
