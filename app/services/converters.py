from typing import List
import json
from math import ceil
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService, BaseDataManager, GenericDataManager
from app.schemas.converters import ( CabinetSchema, LocationSchema, ProductionLineSchema, UnitSchema, ConverterSchema, MillShopSchema )
from app.models.converters import ConverterModel, MillShopModel, ProductionLineModel, LocationModel, CabinetModel, UnitModel

class ConverterService(BaseService):
    """
    Сервис для работы с преобразователями частоты.
    """
    def __init__(self, session):
        """
        Инициализирует ConverterService.
        """
        super().__init__(session)
        self.millshop_manager = GenericDataManager(session, MillShopSchema, MillShopModel)
        self.production_line_manager = GenericDataManager(session, ProductionLineSchema, ProductionLineModel)
        self.location_manager = GenericDataManager(session, LocationSchema, LocationModel)
        self.cabinet_manager = GenericDataManager(session, CabinetSchema, CabinetModel)
        self.converter_manager = GenericDataManager(session, ConverterSchema, ConverterModel)
        self.unit_manager = GenericDataManager(session, UnitSchema, UnitModel)


    async def get_converters(self) -> List[ConverterSchema]:
        """
        Возвращает весь списпок преобразователей частоты.
        """
        return await ConvertersDataManager(self.session).get_converters()
    
    async def get_converters_paginated(self, page: int, page_size: int) -> dict:
        offset = (page - 1) * page_size
        statement = select(ConverterModel).offset(offset).limit(page_size)
        result = await self.session.execute(statement)
        converters = result.scalars().all()

        # Получаем общее количество
        count_stmt = select(func.count()).select_from(ConverterModel)
        total = await self.session.scalar(count_stmt)

        return {
            "items": [ConverterSchema.model_validate(c, from_attributes=True) for c in converters],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": ceil(total / page_size)
        }
        
    async def add_all_converters(self) -> None:
        """Добавляет все данные последовательно"""
        await self.add_mill_shops('app/data/drivers/drivers.json')
        await self.add_production_lines('app/data/drivers/drivers.json')
        await self.add_locations('app/data/drivers/drivers.json')
        await self.add_cabinets('app/data/drivers/drivers.json')
        await self.add_converters('app/data/drivers/drivers.json')
        await self.add_units('app/data/drivers/drivers.json')
        
    async def add_mill_shops(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        mill_shops = {item["mill_shop"] for item in data["converters"]}
        for shop in mill_shops:
            existing = await self.millshop_manager.get_by_name(shop)
            if not existing:
                new_shop = MillShopModel(name=shop)
                await self.millshop_manager.add_item(new_shop)

    async def add_production_lines(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        prod_lines = {(item["mill_shop"], item["production_line"]) for item in data["converters"]}
        for shop_name, line_name in prod_lines:
            shop = await self.millshop_manager.get_by_name(shop_name)
            if shop:
                
                new_line = ProductionLineModel(name=line_name, mill_shop_id=shop.id)
                await self.production_line_manager.add_item(new_line)

    async def add_locations(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        locations = {(item["production_line"], item["location"]) for item in data["converters"]}
        for line_name, loc_name in locations:
            line = await self.production_line_manager.get_by_name(line_name)
            if line:

                new_location = LocationModel(name=loc_name, production_line_id=line.id)
                await self.location_manager.add_item(new_location)

    async def add_cabinets(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        cabinets = {(item["location"], item["cabinet"]) for item in data["converters"]}
        
        for loc_name, cab_name in cabinets:
        # Добавим фильтр по production_line для уникальности локации
            if not cab_name:  # Пропускаем если имя пустое
                continue
            statement = select(LocationModel).where(LocationModel.name == loc_name)
            result = await self.session.execute(statement)
            location = result.first()

            if location:

                new_cabinet = CabinetModel(
                    name=cab_name, 
                    location_id=location[0].id
                )
                await self.cabinet_manager.add_item(new_cabinet)

    async def add_converters(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data["converters"]:
            statement = select(CabinetModel).where(CabinetModel.name == item["cabinet"])
            result = await self.session.execute(statement)
            cabinet = result.first()
            
            if cabinet:
                new_converter = ConverterModel(
                    cabinet_id=cabinet[0].id,
                    brand=item["converter"],
                    model=item["converter_type"] or "",
                    nominal_current=None,  # Добавь нужные поля из JSON
                    current_type=None,
                    power=None,
                    input_voltage=None,
                    output_voltage=None
                )
                await self.converter_manager.add_item(new_converter)

    async def add_units(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data["converters"]:
            if not item["unit"]:  # Пропускаем если unit пустой
                continue
        
            statement = select(ConverterModel).where(ConverterModel.brand == item["converter"])
            result = await self.session.execute(statement)
            converter = result.first()
            
            if converter:

                new_unit = UnitModel(
                    name=item["unit"],
                    converter_id=converter[0].id
                )
                await self.unit_manager.add_item(new_unit)
                
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
        return schemas

    async def add_all_converters(self) -> None:
        """Добавляет все данные последовательно"""
        await self.add_all_converters()
    
    async def delete_converter(self, converter_id: int) -> bool:
        """Удаляет преобразователь по ID."""
        return await self.converter_manager.delete_item(converter_id)

    async def delete_cabinet(self, cabinet_id: int) -> bool:
        """Удаляет шкаф по ID."""
        return await self.cabinet_manager.delete_item(cabinet_id)

    async def delete_production_line(self, production_line_id: int) -> bool:
        """Удаляет производственную линию по ID."""
        return await self.production_line_manager.delete_item(production_line_id)

    async def delete_location(self, location_id: int) -> bool:
        """Удаляет локацию по ID."""
        return await self.location_manager.delete_item(location_id)

    async def delete_unit(self, unit_id: int) -> bool:
        """Удаляет единицу измерения по ID."""
        return await self.unit_manager.delete_item(unit_id)

    async def delete_all_converters(self) -> bool:
        """Удаляет все преобразователи."""
        return await self.converter_manager.delete_items()

    async def delete_all_cabinets(self) -> bool:
        """Удаляет все шкафы."""
        return await self.cabinet_manager.delete_items()

    async def delete_all_production_lines(self) -> bool:
        """Удаляет все производственные линии."""
        return await self.production_line_manager.delete_items()

    async def delete_all_locations(self) -> bool:
        """Удаляет все локации."""
        return await self.location_manager.delete_items()

    async def delete_all_units(self) -> bool:
        """Удаляет все единицы измерения."""
        return await self.unit_manager.delete_items()

    async def delete_all_data(self) -> dict:
        """Удаляет все данные из всех таблиц."""
        results = {
            "converters": await self.delete_all_converters(),
            "cabinets": await self.delete_all_cabinets(),
            "production_lines": await self.delete_all_production_lines(),
            "locations": await self.delete_all_locations(),
            "units": await self.delete_all_units(),
        }
        return results