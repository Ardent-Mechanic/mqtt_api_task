from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from utils.mqtt_client_test import client as mqtt_client_test, metric_arr
from core.config import settings

router = APIRouter(tags=["Metric"])


@router.post("/publish/")
async def publish_message(topic: str = settings.mqtt_config.topic,
                          message: str = "{\"id\":802241,\"bs_id\":151124,\"time\""
                          ":1733832653,\"event\":\"period\",\"type\":\""
                          "temperature\",\"value\":24.2,\"mc\":6}"):
    mqtt_client_test.publish(topic, message)
    return {"status": "Message published", "topic": topic, "message": message}


@router.get("/messages/")
async def get_messages():
    return {"messages": metric_arr}
