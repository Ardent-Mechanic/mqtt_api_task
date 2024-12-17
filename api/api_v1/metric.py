from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from crud.metric import get_metrics_by_date
from db import db_session
from schemas import GetMetricData
from utils.mqtt_client_test import client as mqtt_client_test
from core.config import settings

router = APIRouter(tags=["Metric"])


@router.post("test/publish/")
async def publish_message(topic: str = settings.mqtt_config.topic,
                          message: str = "{\"id\":802241,\"bs_id\":151124,\"time\""
                                         ":1733832653,\"event\":\"period\",\"type\":\""
                                         "temperature\",\"value\":24.2,\"mc\":6}"):
    mqtt_client_test.publish(topic, message)
    return {"status": "Message published", "topic": topic, "message": message}


@router.post("test/get_data/")
async def get_messages(
        session: Annotated[
            AsyncSession,
            Depends(db_session.session_getter),
        ],
        get_metrics_data: GetMetricData
):
    data = await get_metrics_by_date(
        session=session,
        start_date=get_metrics_data.datetime_start,
        end_date=get_metrics_data.datetime_end
    )
    return {"data": data}
