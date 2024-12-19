# MQTT обработчик
import asyncio

from core.config import settings
from gmqtt import Client as MQTTClient

from crud.metric import put_metrics
from db import db_session


class MQTTHandler:
    def __init__(self):
        self.client = MQTTClient("unique_client_id")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    async def connect(self):
        await self.client.connect(settings.mqtt_config.broker, port=settings.mqtt_config.port)
        await asyncio.Future()  # Держим соединение открытым

    async def on_connect(self, client, flags, rc, properties):
        print(f"Connected with result code {rc}")
        self.client.subscribe(settings.mqtt_config.topic, qos=1)

    async def on_disconnect(self, client, packet, exc=None):
        print("Disconnected")

    async def on_message(self, topic, payload, session=None):
        print(f"Received message: {payload} on topic: {topic}")
        if session is None:
            session = await db_session.session_getter().__anext__()
        await put_metrics(session, payload)


mqtt_handler = MQTTHandler()
