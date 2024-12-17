import asyncio

import paho.mqtt.client as mqtt

from core.config import settings
from crud.metric import put_metrics
from db.db_session import db_session


# Callback при подключении
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(settings.mqtt_config.topic)


# Callback при отправке данных
async def process_message(msg: mqtt.MQTTMessage):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")
    session = await db_session.session_getter().__anext__()
    await put_metrics(session=session, metrics=msg.payload.decode())


# Обработчик сообщений (запускает асинк тк сам пахо синхронный)
def on_message(client, userdata, msg):
    asyncio.run(process_message(msg))


# Создание MQTT клиента
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
