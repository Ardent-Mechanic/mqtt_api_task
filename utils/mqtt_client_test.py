import asyncio

import paho.mqtt.client as mqtt

from core.config import settings
from crud.metric import put_metrics
from db.db_session import db_session

# MQTT_BROKER = "dev.rvts.ru"  # Адрес вашего брокера
# MQTT_PORT = 1883  # Порт брокера
# MQTT_TOPIC = "sensor/802241/data"  # Тема для подписки/публикации


# Типо база данных
metric_arr = []


# Callback при подключении
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(settings.mqtt_config.topic)


async def process_message(msg: mqtt.MQTTMessage):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")
    # Здесь вы можете добавить обработку данных, например, сохранение в базу данных
    # await save_data_to_db(msg.payload.decode())
    session = await db_session.session_getter().__anext__()
    print(type(session))
    await put_metrics(session=session, metrics=msg.payload.decode())


# Обработчик сообщений
def on_message(client, userdata, msg):
    asyncio.run(process_message(msg))

    # put_metrics(session=db_session.session_getter(), metrics=msg.payload.decode())


# Создание MQTT клиента
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
