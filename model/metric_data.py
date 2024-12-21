from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class MetricData(Base):
    metric_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    topic_id: Mapped[int] = mapped_column(Integer)
    bs_id: Mapped[int] = mapped_column(Integer)
    time: Mapped[datetime] = mapped_column(DateTime)
    event: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    value: Mapped[float] = mapped_column(Float)
    mc: Mapped[bool] = mapped_column(Integer, nullable=True)
