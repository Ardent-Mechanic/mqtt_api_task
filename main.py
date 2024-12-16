from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from utils.mqtt_client_test import client as mqtt_client_test
import threading
from api import router as api_router

app = FastAPI()

app.include_router(api_router)


# Функция для запуска MQTT клиента в отдельном потоке
def start_mqtt():
    mqtt_client_test.connect(settings.mqtt_config.host, settings.mqtt_config.port, 60)
    mqtt_client_test.loop_forever()


# Запуск MQTT клиента при старте FastAPI
@app.on_event("startup")
def startup_event():
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
