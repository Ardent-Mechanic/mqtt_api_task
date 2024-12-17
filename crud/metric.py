import json
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from model.metric_data import MetricData
from schemas import GetMetricData, MetricDataBase
from utils import convert_to_date


async def get_metrics_by_date(
        session: AsyncSession,
        start_date: str,
        end_date: str
) -> Sequence[MetricData]:
    """ Теперт знаю :3 """
    conv_start_date = convert_to_date(start_date)
    conv_end_date = convert_to_date(end_date)
    print(start_date, end_date)
    stmt = select(MetricData).where(and_(MetricData.time >= conv_start_date, MetricData.time <= conv_end_date))
    result = await session.scalars(stmt)
    return result.all()


# Добавить информацию о том что данные отправлены в output
async def put_metrics(
        session: AsyncSession,
        metrics: str
) -> None:
    data = json.loads(metrics)
    metric_info = MetricData(id=data['id'],
                             bs_id=data['bs_id'],
                             time=datetime.fromtimestamp(data['time']),
                             event=data['event'],
                             type=data['type'],
                             value=data['value'],
                             mc=data['mc'])

    session.add(metric_info)
    await session.commit()
