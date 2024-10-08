from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from app.settings import settings


class Base(MappedAsDataclass, AsyncAttrs, DeclarativeBase):
    """Базовый класс моделей базы данных."""


engine = create_async_engine(settings.SQLITE_DSN)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
