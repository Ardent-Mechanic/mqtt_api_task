from typing import Any

from core.config import settings

from crud.metric import put_metrics
from db import db_session

from gmqtt import Client as MQTTClient
from fastapi_mqtt import FastMQTT, MQTTConfig

import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger_mqtt = logging.getLogger("gmqtt")

mqtt_config = MQTTConfig(
    host=settings.mqtt.host,
    port=settings.mqtt.port,
    keepalive=60,
)

fast_mqtt = FastMQTT(config=mqtt_config)


@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    logger_mqtt.info(f"Connected: flag={flags}, rc={rc}, properties={properties}")


@fast_mqtt.subscribe(settings.mqtt.topic, qos=1)
async def home_message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    logger_mqtt.info(f"Received message: topic={topic}, data={payload.decode()}, qos={qos}")


@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    async for session in db_session.session_getter():  # Используем session_getter
        try:
            data = payload.decode().split("}")[0] + "}"
            await put_metrics(session, data)  # Обработка данных
        except Exception as e:
            logger_mqtt.error(f"Error processing message: {e}")


@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    logger_mqtt.info(f"Disconnected: {client}, packet={packet}")


@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties: Any):
    logger_mqtt.info(f"subscribed: {settings.mqtt.topic}, mid={mid}, qos={qos}, properties={properties}")
