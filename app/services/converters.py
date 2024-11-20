from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService, BaseDataManager
from app.schemas.converters import ConverterSchema
from app.models.converters import ConverterModel

class ConverterService(BaseService):
    """
    Сервис для работы с преобразователями частоты.
    """
    def __init__(self, session):
        """
        Инициализирует ConverterService.
        """
        super().__init__(session)

    async def get_converters(self) -> List[ConverterSchema]:
        """
        Возвращает весь списпок преобразователей частоты.
        """
        return await ConvertersDataManager(self.session).get_converters()

class ConvertersDataManager(BaseDataManager):
    """
    Менеджер данных для работы с преобразователями частоты.
    """
    def __init__(self, session: AsyncSession):
        super().__init__(session, ConverterSchema)
    
    async def get_converters(self) -> List[ConverterSchema]:
        """
        Возвращает весь список преобразователей частоты.
        """
        schemas: List[ConverterSchema] = list()
        statement = select(ConverterModel)
        for model in await self.get_all(statement):
            schemas.append(ConverterSchema(**model.to_dict()))
        return []
