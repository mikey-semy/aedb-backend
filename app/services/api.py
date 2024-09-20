from typing import List

from app.services.base import BaseService, GenericDataManager
from app.models.api import MenuItemsModel
from app.schemas.api import MenuItemsSchema

class APIService(BaseService):
    
    def __init__(self, session):
        """
        Инициализирует APIService.

        :param session: Сессия базы данных
        """
        super().__init__(session)
        self.manual_manager = GenericDataManager(session, MenuItemsSchema, MenuItemsModel)

    async def get_menu_items(self) -> List[MenuItemsSchema]:
        """
        Получает список меню.

        :return: Список меню
        """
        return await self.manual_manager.get_items()
