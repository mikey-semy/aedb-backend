from typing import Any, AsyncGenerator
from aioboto3 import Session
from botocore.exceptions import ClientError
from aiologger import Logger
from app.core.config import config

class S3Session():
    """
    Класс для управления сессией S3 с использованием aioboto3.
    """
    
    def __init__(self, settings: Any = config) -> None:
        """
        Инициализация S3Session.

        :param settings: Конфигурация AWS, содержащая параметры доступа.
        """
        self.region_name=settings.aws_region
        self.endpoint_url=settings.aws_endpoint
        self.access_key_id=settings.aws_access_key_id
        self.secret_access_key=settings.aws_secret_access_key
        self.logger = Logger.with_default_handlers(name="S3SessionLogger")
    
    def __get_s3_params(self) -> dict:
        """
        Получение параметров для создания клиента S3.

        :return: Словарь с параметрами для клиента S3.
        """
        return {
            "region_name": self.region_name,
            "endpoint_url": self.endpoint_url,
            "aws_access_key_id": self.access_key_id,
            "aws_secret_access_key": self.secret_access_key,
        }
        
    async def create_async_session_factory(self) -> Any:
        """
        Создание асинхронного клиента S3.

        :return: Асинхронный клиент S3.
        :raises ClientError: Если возникла ошибка при создании клиента.
        """
        try:
            session = Session()
            return await session.client('s3', **self.__get_s3_params())
        except ClientError as e:
            await self.logger.error(f"Ошибка при создании клиента S3: {e}")
            raise
    
class SessionContextManager:
    """
    Инициализация SessionContextManager.
    """
    
    def __init__(self):
        self.s3_session = S3Session(config)
        self.session = None
        self.logger = Logger.with_default_handlers(name="SessionContextManagerLogger")

    async def __aenter__(self):
        """
        Вход в контекстный менеджер.

        :return: Экземпляр SessionContextManager с активной сессией S3.
        """
        self.session = await self.s3_session.create_async_session_factory()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Выход из контекстного менеджера.

        :param exc_type: Тип исключения, если оно возникло.
        :param exc_val: Значение исключения, если оно возникло.
        :param exc_tb: Объект трассировки, если исключение возникло.
        """
        await self.close_client()
        
    async def close_client(self):
        """
        Закрытие клиента S3.

        Обнуляет ссылку на сессию, чтобы освободить ресурсы.
        """
        if self.session :
            self.session = None
    
    async def get_s3_session(self) -> AsyncGenerator[Any, None]:
        """
        Получение асинхронной сессии S3.

        :yield: Асинхронный клиент S3.
        :raises ClientError: Если возникла ошибка при получении сессии.
        """
        try:
            async with self as session_manager:
                yield session_manager.session
        except Exception as e:
            await self.logger.error(f"Ошибка при получении сессии S3: {e}")
            raise
