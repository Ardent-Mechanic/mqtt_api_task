from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class MetricData(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    bs_id: Mapped[int] = mapped_column(Integer, unique=True)
    time: Mapped[str] = mapped_column(String(50))
    event: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(5))
    mc: Mapped[bool] = mapped_column(Integer)
