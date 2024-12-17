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
    value: str
    mc: int

    class Config:
        from_attributes = True


class GetMetricData(BaseModel):
    time: str
