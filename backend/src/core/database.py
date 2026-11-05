import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from src.core.config import get_settings

logger = logging.getLogger("turalimpia.database")

settings = get_settings()

_url = settings.database_url_async if hasattr(settings, "database_url_async") else settings.database_url
if _url.startswith("postgresql://"):
    _url = _url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif _url.startswith("postgresql+psycopg2://"):
    _url = _url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)

_is_pg = "asyncpg" in _url
_connect_args = {}
_engine_kwargs = {}

if _is_pg:
    _connect_args["statement_cache_size"] = 0
    logger.info("PostgreSQL detectado: statement_cache_size=0 configurado.")

engine = create_async_engine(
    _url,
    echo=settings.debug,
    connect_args=_connect_args,
    **_engine_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def crear_tablas() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)