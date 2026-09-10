from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TradeExecution(Base):
    __tablename__ = "trade_execution"

    execution_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("trade_order.order_id"),
        nullable=False
    )

    execution_qty: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    execution_price: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    execution_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    settlement_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    settlement_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )