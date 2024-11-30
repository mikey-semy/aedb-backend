from typing import List, Any
import json
from fastapi import Depends, UploadFile

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.manuals import ManualModel, CategoryModel, GroupModel
from app.schemas.manuals import (
    ManualSchema,
    CategorySchema,
    GroupSchema,
    CategoryNestedSchema,
    ManualListItemSchema,
    ManualNestedSchema,
    CategoryNestedSchema,
    GroupNestedSchema,
    ManualFileSchema
)
from aioboto3 import Session
from app.cloud.session import get_s3_session

from app.services.base import CategoryDataManager, BaseService, GenericDataManager, T


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
        new_item = manager.model(**item.model_dump())
        return await manager.add_item(new_item)


    async def add_manual(self,
                         manual: ManualFileSchema, 
                         file: UploadFile,
                         session: Session = Depends(get_s3_session)
                         ) -> ManualSchema:
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

    async def get_list_manuals(self) -> List[ManualListItemSchema]:
        """
        Получает плоский список всех инструкций.

        :return: Список инструкций
        """
        statement = (
            select(ManualModel, CategoryModel, GroupModel)
            .join(GroupModel, ManualModel.group_id == GroupModel.id)
            .join(CategoryModel, GroupModel.category_id == CategoryModel.id)
        )
        result = await self.session.execute(statement)
        manuals_list = []
        for manual, category, group in result:
            manual_item = ManualListItemSchema(
                category_name=category.name,
                group_name=group.name,
                manual_name=manual.title,
                manual_url=manual.file_url,
            )
            manuals_list.append(manual_item)

        return manuals_list

    async def get_nested_manuals(self) -> List[CategoryNestedSchema]:
        """
        Получает список всех инструкций, вложенных в категории и группы.

        :return: Список инструкций
        """
    
        statement = select(CategoryModel).options(
                            joinedload(CategoryModel.groups)
                            .joinedload(GroupModel.manuals)
                        )
        category_manager = CategoryDataManager(self.session)
        categories = await category_manager.get_all(statement)
        result: List[Any] = []
        for category in categories:
            category_dict = category.to_dict
            category_dict['groups'] = [
                GroupNestedSchema(
                    **group.to_dict,
                    manuals=[
                        ManualNestedSchema(**manual.to_dict) for manual in group.manuals
                    ]
                ) for group in category.groups
            ]      
            result.append(CategoryNestedSchema(**category_dict))
        return result
    
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

    async def get_groups_by_category(self, category_id: int) -> List[GroupSchema]:
        """
        Получает список элементов из базы данных с родительским id.

        :param category_id: ID родительской категории
        :return: Список элементов в виде схем
        """
        statement = select(GroupModel).where(GroupModel.category_id == category_id)
        groups = await self.group_manager.get_all(statement)
    
        return [GroupSchema(**group.to_dict) for group in groups]
    
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

    async def delete_manuals(self) -> bool:
        return await self.manual_manager.delete_items()
    