from typing import List
from app.schemas.base import BaseSchema

class Sensor(BaseSchema):
    name: str
    address: str
    date: str
    status: str
    battery: float
    temperature: float

class SensorData(BaseSchema):
    sensors: List[Sensor]