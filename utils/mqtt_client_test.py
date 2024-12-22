# MQTT обработчик
import asyncio
from typing import Any

from core.config import settings
from gmqtt import Client as MQTTClient

from crud.metric import put_metrics
from db import db_session

import asyncio
from gmqtt import Client as MQTTClient
from fastapi_mqtt import FastMQTT, MQTTConfig

import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# Создание логгеров
logger_mqtt = logging.getLogger("gmqtt")  # Логгер основного приложения

mqtt_config = MQTTConfig(
    host=settings.mqtt_config.host,
    port=1883,
    keepalive=60,
)

fast_mqtt = FastMQTT(config=mqtt_config)


@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    logger_mqtt.info(f"Connected: {client}, {flags}, {rc}, {properties}")


@fast_mqtt.subscribe(settings.mqtt_config.topic, qos=1)
async def home_message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    logger_mqtt.info(f"Received message: {client}, {topic}, {payload.decode()}, {qos},")


@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    async for session in db_session.session_getter():  # Используем session_getter
        try:
            data = payload.decode().split("}")[0] + "}"
            await put_metrics(session, data)  # Обработка данных
        except Exception as e:
            logger_mqtt.error(f"Error processing message: {e}")


@fast_mqtt.subscribe(settings.mqtt_config.topic, qos=2)
async def message_to_topic_with_high_qos(
        client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any
):
    logger_mqtt.info(
        f"Received message to specific topic and QoS=2: {client}, {topic}, {payload.decode()}, {qos}, {properties}"
    )


@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    logger_mqtt.info(f"Disconnected: {client}, {packet}")


@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties: Any):
    logger_mqtt.info(f"subscribed: {client}, {mid}, {qos}, {properties}")
