from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from core.config import settings

import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# Создание логгеров
logger_db = logging.getLogger("db")  # Логгер основного приложения


class DataBaseSession:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
    ) -> None:
        # Создаем асинхронный движок с использованием aiomysql
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session  # Передача управления вызывающему коду
            except Exception as e:
                await session.rollback()  # Откат транзакции в случае ошибки
                logger_db.error(f"Error getting session: {e}")
            finally:
                await session.close()  # Корректное закрытие сессии


# Пример строки подключения для aiomysql
db_session = DataBaseSession(
    url=settings.db.url,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
