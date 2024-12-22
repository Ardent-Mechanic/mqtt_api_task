import json
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from model.metric_data import MetricData
from utils import convert_to_date

import logging.config

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger_db = logging.getLogger("db")  # Логгер основного приложения
logger_main = logging.getLogger("main")


async def get_metrics_by_date(
        session: AsyncSession,
        start_date: str,
        end_date: str
) -> Sequence[MetricData]:
    try:
        try:
            logger_main.debug("INSERTING")
            conv_start_date = convert_to_date(start_date)
            conv_end_date = convert_to_date(end_date)
        except Exception as e:
            logger_main.error(f"Error converting date: {e}")
        logger_main.debug(f"{conv_start_date} {conv_end_date}")
        stmt = select(MetricData).where(and_(MetricData.time >= conv_start_date, MetricData.time <= conv_end_date))
        result = await session.scalars(stmt)
        return result.all()
    except Exception as e:
        await session.rollback()  # Откат транзакции в случае ошибки
        logger_db.error(f"Error inserting data: {e}")


# Добавить информацию о том что данные отправлены в output
async def put_metrics(
        session: AsyncSession,
        metrics: str
) -> None:
    try:
        logger_main.debug("INSERTING")
        data = json.loads(metrics)
        try:
            metric_info = MetricData(topic_id=data['id'],
                                     bs_id=data['bs_id'],
                                     time=datetime.utcfromtimestamp(data['time']),
                                     event=data['event'],
                                     type=data['type'],
                                     value=data['value'],
                                     mc=data['mc'])
        except Exception as e:
            logger_main.error(f"Validation error: {e}")
        session.add(metric_info)
        await session.commit()
    except Exception as e:
        await session.rollback()  # Откат транзакции в случае ошибки
        logger_db.error(f"Error getting data: {e}")
