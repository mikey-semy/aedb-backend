from typing import List
import json
from sqlalchemy import select

from app.models.manuals import ManualModel
from app.schemas.manuals import ManualSchema
from app.services.base import BaseService, BaseDataManager

class ManualService(BaseService):
    async def add_manual(self, manual: ManualSchema) -> ManualSchema:
        new_manual = ManualModel(
            manual_text=manual.manual_text,
            answers=manual.answers,
            correct_answers=manual.correct_answers
        )
        return await ManualDataManager(self.session).add_manual(new_manual)
    
    async def add_all_manuals(self) -> None:
        with open('app/data/manuals.json', 'r', encoding='utf-8') as file:
            manuals = json.load(file)

        for manual in manuals:
            manual_data = json.loads(list(manual.values())[0])
            new_manual = ManualModel(
                    name=manual_data.get('name', ''),
                    url=manual_data.get('url', ''),
                    image=manual_data.get('image', ''),
                    category=manual_data.get('category', ''),
                    group=manual_data.get('group', ''),
                )
            await ManualDataManager(self.session).add_manual(new_manual)

    async def get_manuals(self) -> List[ManualSchema]:
        return await ManualDataManager(self.session).get_manuals()

class ManualDataManager(BaseDataManager):
    
    async def add_manual(self, new_manual) -> ManualSchema:
        return await self.add_one(new_manual)
    
    async def get_manuals(self, statement = select(ManualModel)) -> List[ManualSchema]:
        schemas: List[ManualSchema] = []
        models = await self.get_all(statement)
        for model in models:
            schemas.append(ManualSchema(**model.to_dict))
        return schemas

