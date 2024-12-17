import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from paho import mqtt

from core.config import settings
from db import db_session
from model import Base
from utils.mqtt_client_test import client as mqtt_client_test
import threading
from api import router as api_router
#
# app = FastAPI()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # startup
#     async with db_session.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     # shutdown
#
#     print('Closing DB connection')
#     await db_session.dispose()
# Асинхронный контекст для lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: подключаемся к базе данных и MQTT
    print("Starting up...")

    # Создайте подключение к базе данных (не забудьте заменить на ваш код)
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Подключение к MQTT
    # mqtt_client = mqtt.Client()
    # mqtt_client.on_message = on_message
    mqtt_client_test.connect(settings.mqtt_config.host, settings.mqtt_config.port, 60)

    # Запуск MQTT клиента в фоновом потоке
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, mqtt_client_test.loop_forever)

    yield  # Приложение будет работать здесь

    # shutdown: отключение MQTT и базы данных
    print('Shutting down...')
    mqtt_client_test.disconnect()
    await db_session.dispose()  # Закрыть соединения с базой данных

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(api_router)


# Функция для запуска MQTT клиента в отдельном потоке
# def start_mqtt():
#     mqtt_client_test.connect(settings.mqtt_config.host, settings.mqtt_config.port, 60)
#     mqtt_client_test.loop_forever()


# Запуск MQTT клиента при старте FastAPI
# @app.on_event("startup")
# def startup_event():
#     mqtt_thread = threading.Thread(target=start_mqtt)
#     mqtt_thread.daemon = True
#     mqtt_thread.start()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
