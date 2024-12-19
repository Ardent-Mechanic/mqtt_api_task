import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from paho import mqtt

from core.config import settings
from db import db_session
from model import Base
from utils.mqtt_client_test import MQTTHandler, mqtt_handler
import threading
from api import router as api_router


#


# Асинхронный контекст для lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    # Действия при старте: подключение к MQTT и создание таблиц в БД
    mqtt_task = asyncio.create_task(mqtt_handler.connect())
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создание всех таблиц в БД
    try:
        yield  # Приложение работает
    finally:
        # Действия при завершении: отключение MQTT и завершение фона
        await mqtt_handler.client.disconnect()
        mqtt_task.cancel()
        await db_session.dispose()  # Закрыть соединения с базой данных


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
