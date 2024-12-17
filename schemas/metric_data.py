from pydantic import BaseModel
from pydantic import ConfigDict


# Базовая схема
class MetricDataBase(BaseModel):
    id: int
    bs_id: int
    time: str
    event: str
    type: str
    value: str
    mc: int

    class Config:
        from_attributes = True