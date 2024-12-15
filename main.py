import uvicorn
from fastapi import FastAPI

from config import settings
from mqtt_client_test import client as mqtt_client_test, message
import threading

app = FastAPI()


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


# Пример API-метода для публикации сообщений
@app.post("/publish/")
async def publish_message(topic: str = "test/topic", message: str = "Hello, MQTT!"):
    mqtt_client_test.publish(topic, message)
    return {"status": "Message published", "topic": topic, "message": message}


@app.get("/messages/")
async def get_messages():
    return {"messages": message}


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
