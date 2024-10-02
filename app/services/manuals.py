from typing import List, Any
import json
from fastapi import UploadFile
from app.models.manuals import ManualModel, CategoryModel, GroupModel
from app.schemas.manuals import ManualSchema, CategorySchema, GroupSchema
from app.services.base import BaseService, GenericDataManager, T
from app.utils.manuals import PDFCoverExtractor

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

    async def upload_files(self, manuals: list[UploadFile]):
        results = []
        for manual in manuals:
            file_content = await manual.read()
            file_name = manual.filename
            file_url = await self.save_file(file_content, file_name)
            print(f"file_url: {file_url}")
            manual_data = ManualSchema(title=file_name, file_url=file_url)
            result = await self.add_manual(manual_data)
            results.append(result)
        return results

    async def save_file(self, file_content: bytes, file_name: str) -> str:
        file_path = f"media/manuals/{file_name}"
        with open(file_path, "wb") as f:
            f.write(file_content)
        return f"/media/manuals/{file_name}"

    async def add_item(self, item: T, manager: GenericDataManager) -> T:
        """
        Добавляет новый элемент через указанный менеджер.

        :param item: Элемент для добавления
        :param manager: Менеджер данных для использования
        :return: Добавленный элемент
        """

        if item.file_url:

            item.cover_image_url = PDFCoverExtractor.create_url(item.file_url)

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

    async def get_nested_manuals(self) -> List[Any]:
        """
        Получает список всех инструкций, вложенных в категории и группы.

        :return: Список инструкций
        """
        return await self.manual_manager.get_nested_items()
    
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
