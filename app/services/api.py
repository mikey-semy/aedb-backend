from typing import List

from app.services.base import BaseService
from app.schemas.api import MenuItemsSchema

class APIService(BaseService):
    
    def __init__(self, session):
        """
        Инициализирует APIService.

        :param session: Сессия базы данных
        """
        super().__init__(session)

    async def get_menu_items(self) -> List[MenuItemsSchema]:
        """
        Получает список меню.

        :return: Список меню
        """
        return await MenuItemsSchema.get_all()
