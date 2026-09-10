from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TradeOrder(Base):
    __tablename__ = "trade_order"

    order_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    security_id: Mapped[int] = mapped_column(
        ForeignKey("security.security_id"),
        nullable=False
    )

    order_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )