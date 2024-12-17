from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime


# Базовая схема
class MetricDataBase(BaseModel):
    id: int
    bs_id: int
    time: datetime
    event: str
    type: str
    value: float
    mc: int

    class Config:
        from_attributes = True


class GetMetricData(BaseModel):
    datetime_start: str
    datetime_end: str
