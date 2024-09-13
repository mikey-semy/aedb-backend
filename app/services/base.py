from typing import Any, List
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.manuals import ManualSchema

class SessionMixin:
    """Provides instance of database session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

class BaseService(SessionMixin):
    """Base class for application services."""

class BaseDataManager(SessionMixin):

    async def add_one(self, model: Any) -> ManualSchema:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return ManualSchema(**model.to_dict)

    async def update_one(self, model_to_update, updated_model: Any) -> ManualSchema | None:
        if model_to_update:
            updated_model_dict = updated_model.to_dict
            for key, value in updated_model_dict.items():
                if key != "id":
                    setattr(model_to_update, key, value)
        else:
            return None
        await self.session.commit()
        await self.session.refresh(model_to_update)
        return ManualSchema(**model_to_update.to_dict)

    async def get_one(self, select_statement: Executable) -> Any | None:
        result = await self.session.execute(select_statement)
        return result.scalar()

    async def get_all(self, select_statement: Executable) -> List[Any]:
        result = await self.session.execute(select_statement)
        return list(result.scalars())
