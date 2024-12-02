"""
Модуль для работы с базой данных и сессиями SQLAlchemy.

Этот модуль предоставляет классы и функции для инициализации подключения к базе данных,
создания асинхронных сессий и управления ими с использованием SQLAlchemy.

Основные компоненты:
- DatabaseSession: Класс для настройки подключения к базе данных и создания фабрики сессий.
- SessionContextManager: Контекстный менеджер для управления жизненным циклом сессий.
- get_db_session: Асинхронный генератор для получения сессии базы данных.

Модуль использует асинхронные возможности SQLAlchemy для эффективной работы с базой данных
в асинхронных приложениях.
"""

from typing import Dict, Any, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine
    )
from sqlalchemy.exc import OperationalError
from sqlalchemy import URL
from aiologger import Logger
from app.core.config import config


class DatabaseSession():
    """
    Класс для инициализации и настройки подключения к базе данных и компонентов ORM.
    """
    def __init__(self, settings: Any = config) -> None:
        """
        Инициализирует экземпляр DatabaseSession.

        Args:
            settings (Any): Объект конфигурации. По умолчанию используется глобальный объект config.
        """

        self.dsn = settings.dsn
        self.logger = Logger.with_default_handlers(name="DatabaseSessionLogger")

    async def __get_dsn(self) -> str:
        """
        Получает dsn.

        Args:
            dsn (str): url dsn.

        Returns:
            str: url dsn.
        """
        if not self.dsn:
            await self.logger.error("DSN не установлен. Проверьте конфигурацию.")
            raise ValueError("DSN не установлен. Проверьте конфигурацию.")
        return self.dsn

    async def __create_dsn(self, dsn_params: Dict[str, str]) -> URL:
        """
        Создает объект SQLAlchemy dsn (data source name) для подключения к базе данных.
        
        Аргументы:
            dsn_params (Dict[str, str]): Параметры для создания dsn.
        
            Для создания dsn необходимы следующие параметры:
                DIALECT:             str
                DRIVERNAME:          str
                USERNAME:            str
                PASSWORD:            SecretStr
                HOST:                str
                PORT:                int
                NAME:                str

            Эти параметры необходимо передать следующим образом:
                @property
                def params(self) -> Dict[str, str]:
                    return {
                        "drivername": f"{self.DIALECT}+{self.DRIVERNAME}",
                        "username": self.USERNAME,
                        "password": urllib.parse.quote_plus(self.PASSWORD.get_secret_value()),
                        "host": self.HOST,
                        "port": self.PORT,
                        "database": self.NAME
                    }

        Возвращает:
            URL: Объект SQLAlchemy URL.
        """
        try:
            return URL.create(**dsn_params)
        except Exception as e:
            await self.logger.error("Ошибка при создании DSN: %s", e)
            raise

    async def __create_async_engine(self, dsn: str) -> AsyncEngine:
        """
        Создает асинхронный движок SQLAlchemy.

        Args:
            dsn (str): Строка подключения к базе данных.
            engine_params (Dict[str, bool]): Параметры для создания движка.

        Returns:
            AsyncEngine: Асинхронный движок SQLAlchemy.
        """
        try:
            async_engine = create_async_engine(dsn, echo=True)
            return async_engine
        except Exception as e:
            await self.logger.error(f"Ошибка при создании асинхронного движка: {e}")
            raise

    async def __precreate_async_session_factory(self, async_engine: AsyncEngine) -> AsyncSession:
        """
        Предварительно создает фабрику асинхронных сессий для операций с базой данных.

        Args:
            async_engine (AsyncEngine): Асинхронный движок SQLAlchemy.
            sessionmaker_params (Dict[str, Any]): Параметры для создания сессии.

        Returns:
            AsyncSession: Фабрика асинхронных сессий.
        """
        try:
            async_session_factory = async_sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
                bind=async_engine,
            )
            return async_session_factory
        except Exception as e:
            await self.logger.error("Ошибка при предварительном создании фабрики асинхронных сессий: %s", e)
            raise


    async def create_async_session_factory(self) -> AsyncSession:
        """
        Создает настроенную фабрику сессий.

        Returns:
            AsyncSession: Фабрика асинхронных сессий.
        """
        try:
            dsn = self.__get_dsn()
            async_engine = self.__create_async_engine(dsn)
            session_factory = self.__precreate_async_session_factory(async_engine)
            return session_factory
        except Exception as e:
            await self.logger.error("Ошибка при создании фабрики асинхронных сессий: %s", e)
            raise


class SessionContextManager():
    """
    Контекстный менеджер для управления сессиями базы данных.
    """

    def __init__(self) -> None:
        """
        Инициализирует экземпляр SessionContextManager.
        """
        self.db_session = DatabaseSession(config)
        self.session_factory = self.db_session.create_async_session_factory()
        self.session = None
        self.logger = Logger.with_default_handlers(name="SessionContextManagerLogger")

    async def __aenter__(self) -> 'SessionContextManager':
        """
        Асинхронный метод входа в контекстный менеджер.

        Returns:
            SessionContextManager: Экземпляр текущего контекстного менеджера.
        """
        try:
            self.session = await self.session_factory()
            return self
        except Exception as e:
            await self.logger.error("Ошибка при входе в контекстный менеджер: %s", e)
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Асинхронный метод выхода из контекстного менеджера.

        Args:
            exc_type: Тип исключения, если оно возникло.
            exc_val: Значение исключения, если оно возникло.
            exc_tb: Объект трассировки, если исключение возникло.
        """
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """
        Асинхронно фиксирует изменения в базе данных и закрывает сессию.
        """
        try:
            await self.session.commit()
            await self.session.close()
            self.session = None
        except OperationalError as e:
            await self.logger.error("Ошибка при фиксации изменений: %s", e)
            await self.rollback()

    async def rollback(self) -> None:
        """
        Асинхронно откатывает изменения в базе данных и закрывает сессию.
        """
        try:
            await self.session.rollback()
            await self.session.close()
            self.session = None
        except OperationalError as e:
            await self.logger.error("Ошибка при откате изменений: %s", e)


async def get_db_session() -> AsyncGenerator[Any, None]:
    """
    Асинхронный генератор для получения сессии базы данных.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    Raises 
        Exception: Если возникла ошибка при получении сессии.
    """
    try:
        async with SessionContextManager() as session_manager:
            yield session_manager.session
    except Exception as e:
            await SessionContextManager().logger.error(f"Ошибка при получении сессии S3: {e}")
            raise