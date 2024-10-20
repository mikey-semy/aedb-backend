"""
Модуль base.py содержит базовые классы и типы данных для работы с моделями SQLAlchemy.

Этот модуль предоставляет:
1. SQLModel - базовый класс для определения моделей SQLAlchemy с дополнительными методами.
2. ArrayOfStrings - пользовательский тип данных для работы с массивами строк, 
   обеспечивающий совместимость между различными диалектами баз данных.

Классы:
- SQLModel: Базовый класс для моделей с методами для работы со схемой, именем таблицы и полями.
- ArrayOfStrings: Тип данных для хранения массивов строк, адаптирующийся под разные диалекты SQL.

Модуль обеспечивает удобную работу с моделями данных и их преобразование в различные форматы.
"""
import json
from typing import Any, Dict, List

from sqlalchemy.types import ARRAY, TypeDecorator, Text, JSON
from sqlalchemy.orm import DeclarativeBase

class SQLModel(DeclarativeBase):
    """
    Базовый класс, используемый для определения моделей.

    Предоставляет удобные методы, которые можно использовать для
    преобразования модели в соответствующую схему.
    """
    @classmethod
    def schema(cls) -> str:
        """
        Возвращает имя схемы базы данных, на которую ссылается модель.

        Returns:
            str: Имя схемы базы данных.

        Raises:
            ValueError: Если невозможно идентифицировать схему модели.
        """

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Невозможно идентифицировать схему модели")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """
        Возвращает имя таблицы, на которую ссылается модель.

        Returns:
            str: Имя таблицы.
        """

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """
        Возвращает список имен полей модели.

        Returns:
            List[str]: Список имен полей.
        """

        return cls.__mapper__.selectable.c.keys()
    
    @property
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует экземпляр модели в словарь.

        Returns:
            Dict[str, Any]: Словарь, представляющий модель.
        """

        _dict: Dict[str, Any] = {}
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict

class ArrayOfStrings(TypeDecorator):
    """
    Пользовательский тип данных для работы с массивами строк.

    Этот класс обеспечивает совместимость между различными диалектами баз данных,
    используя ARRAY для PostgreSQL и JSON для других диалектов.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """
        Загружает соответствующую реализацию для конкретного диалекта базы данных.

        Args:
            dialect: Диалект базы данных.

        Returns:
            Реализация типа данных для конкретного диалекта.
        """
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(Text()))
        else:
            return dialect.type_descriptor(JSON())

    def process_bind_param(self, value, dialect):
        """
        Обрабатывает параметр при привязке к базе данных.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        """
        Обрабатывает значение, полученное из базы данных.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.loads(value)

    def process_literal_param(self, value, dialect):
        """
        Обрабатывает литеральный параметр.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        return value

    @property
    def python_type(self):
        return list

