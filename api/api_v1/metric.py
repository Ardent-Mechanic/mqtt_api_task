from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from crud.metric import get_metrics_by_date
from db import db_session

from schemas import GetMetricData, MetricDataCreate
from core.config import settings
from utils.mqtt_client_test import mqtt_handler

router = APIRouter(tags=["Metric"])


@router.post("test/publish/", summary="Публикация сообщения в MQTT", tags=["SEND"])
async def publish_message(message: MetricDataCreate,
                          session: Annotated[
                              AsyncSession,
                              Depends(db_session.session_getter),
                          ],
                          topic: str = settings.mqtt_config.topic,

                          ):
    """
    Метод сделан для отладки, так как в указанный топик не приходят данные.

    Публикация сообщения в указанный топик MQTT-брокера.

    - **topic**: Топик для публикации (по умолчанию из настроек).
    - **message**: Сообщение в формате строки, которое будет отправлено.
    """
    await mqtt_handler.on_message(settings.mqtt_config.topic, message.data, session=session)
    return {"status": "Message published", "topic": topic, "message": message}


@router.post("test/get_data/", summary="Получение данных по времени", tags=["GET"])
async def get_messages(
        session: Annotated[
            AsyncSession,
            Depends(db_session.session_getter),
        ],
        get_metrics_data: GetMetricData
):
    """
       Получение данных метрик за определённый временной период.

       - **datetime_start**: Начальная дата и время
       - **datetime_end**: Конечная дата и время

       Возвращает список метрик, удовлетворяющих диапазону дат.
       """
    data = await get_metrics_by_date(
        session=session,
        start_date=get_metrics_data.datetime_start,
        end_date=get_metrics_data.datetime_end
    )
    return {"data": data}
