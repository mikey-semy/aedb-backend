import json
from typing import Any, Dict, List
from sqlalchemy import Text
from sqlalchemy.types import ARRAY, TypeDecorator, Text, JSON
from sqlalchemy.orm import DeclarativeBase

class SQLModel(DeclarativeBase):
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """
    
    @classmethod
    def schema(cls) -> str:
        """Return name of database schema the model refers to."""

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """Return name of the table the model refers to."""

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        return cls.__mapper__.selectable.c.keys()
    @property
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to a dictionary."""

        _dict: Dict[str, Any] = {}
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict

class ArrayOfStrings(TypeDecorator):
    
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(Text()))
        else:
            return dialect.type_descriptor(JSON())

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.loads(value)