from fastapi import APIRouter
from app.schemas.sensors import SensorData
from app.const import sensors_params


router = APIRouter(**sensors_params)


@router.post("/receive_data")
async def receive_data(sensor_data: SensorData):
    # Обработка полученных данных
    print(sensor_data)
    return {"message": sensor_data}