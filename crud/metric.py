import json
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from model.metric_data import MetricData


# async def get_metrics_by_date(
#         session: AsyncSession,
#         start_date: str,
#         end_date: str
# ) -> GetMetricData:
#     """Не знаю как сравниваются даты ( """
#     s_date = convert_to_date(start_date)
#     e_date = convert_to_date(end_date)
#     stmt = select(MetricDataBase).where(and_(MetricDataBase.time >= s_date, MetricDataBase.time <= e_date))
#     result = await session.scalars(stmt)
#     return result.one()


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

    # print(metric)
    session.add(metric_info)
    await session.commit()
