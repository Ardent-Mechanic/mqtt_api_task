from datetime import datetime

from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.base import Base


class MetricData(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    bs_id: Mapped[int] = mapped_column(Integer, unique=True)
    time: Mapped[datetime] = mapped_column(DateTime)
    event: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    value: Mapped[float] = mapped_column(Float)
    mc: Mapped[bool] = mapped_column(Integer)
