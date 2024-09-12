'''
This module provides functionality for initializing and setting up database connections
and ORM components using SQLAlchemy with asynchronous support.

Note:
 - dsn
https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.engine.dsn.create

 - create_async_engine_params:
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.create_async_engine

 - session_maker_params: 
https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.__init__

'''
from typing import Dict, Any
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine
    )
from sqlalchemy import URL
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


    def __get_dsn(self, dsn: str) -> str:
        """
        Получает dsn.

        Args:
            dsn (str): url dsn.

        Returns:
            str: url dsn.
        """
        return dsn

    def __create_dsn(self, dsn_params: Dict[str, str]) -> URL:
        """
        Create a SQLAlchemy dsn (data source name) object for database connection.
        """
        dsn = URL.create(**dsn_params)

        return dsn

    def __create_async_engine(self, dsn: str) -> AsyncEngine:
        """
        Создает асинхронный движок SQLAlchemy.

        Args:
            dsn (str): Строка подключения к базе данных.
            engine_params (Dict[str, bool]): Параметры для создания движка.

        Returns:
            AsyncEngine: Асинхронный движок SQLAlchemy.
        """
        async_engine = create_async_engine(dsn, echo=True)

        return async_engine

    def __precreate_async_session_factory(self, async_engine: AsyncEngine) -> AsyncSession:
        """
        Предварительно создает фабрику асинхронных сессий для операций с базой данных.

        Args:
            async_engine (AsyncEngine): Асинхронный движок SQLAlchemy.
            sessionmaker_params (Dict[str, Any]): Параметры для создания сессии.

        Returns:
            AsyncSession: Фабрика асинхронных сессий.
        """
        async_session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
            bind=async_engine,
        )
        return async_session_factory


    def create_async_session_factory(self) -> AsyncSession:
        """
        Создает настроенную фабрику сессий.

        Returns:
            AsyncSession: Фабрика асинхронных сессий.
        """

        dsn = self.__get_dsn(self.dsn)

        async_engine = self.__create_async_engine(dsn)

        session_factory = self.__precreate_async_session_factory(async_engine)

        return session_factory
    

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

    async def __aenter__(self) -> 'SessionContextManager':
        """
        Асинхронный метод входа в контекстный менеджер.

        Returns:
            SessionContextManager: Экземпляр текущего контекстного менеджера.
        """
        self.session = self.session_factory()
        return self

    async def __aexit__(self, *args: object) -> None:
        """
        Асинхронный метод выхода из контекстного менеджера.

        Args:
            *args: Аргументы, передаваемые при выходе из контекста.
        """
        await self.rollback()

    async def commit(self) -> None:
        """
        Асинхронно фиксирует изменения в базе данных и закрывает сессию.
        """
        await self.session.commit()
        await self.session.close()
        self.session = None

    async def rollback(self) -> None:
        """
        Асинхронно откатывает изменения в базе данных и закрывает сессию.
        """
        await self.session.rollback()
        await self.session.close()
        self.session = None


async def get_db_session():
    """
    Асинхронный генератор для получения сессии базы данных.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    """
    async with SessionContextManager() as session_manager:
        yield session_manager.session
