from pydantic import BaseModel, Field
from pydantic import ConfigDict
from datetime import datetime


class GetMetricData(BaseModel):
    """
    Модель для получения метрик в заданном временном диапазоне.

    Поля:
    - datetime_start: Начальная дата и время периода.
    - datetime_end: Конечная дата и время периода.
    """

    datetime_start: str = Field(
        ...,
        description="Начальная дата и время периода",
        example="2024-12-01 00:00:00"
    )
    datetime_end: str = Field(
        ...,
        description="Конечная дата и время периода ",
        example="2024-12-18 00:00:00"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "datetime_start": "2024-12-01 00:00:00",
                "datetime_end": "2024-12-18 00:00:00"
            }
        }


class MetricDataCreate(BaseModel):
    """
    Схема для приема данных в виде строки JSON.
    """
    data: str = Field(
        ...,
        description="JSON-строка с данными, содержащими ключи: id, bs_id, time,"
                    " event, type, value, mc.",
        example='{"id":802241,"bs_id":151124,"time":1733832653,'
                '"event":"period","type":"temperature","value":24.2,"mc":6}'
    )
