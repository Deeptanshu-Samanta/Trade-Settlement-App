from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Security(Base):
    __tablename__ = "security"

    security_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    symbol: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    security_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    exchange_id: Mapped[int] = mapped_column(
        ForeignKey("exchange.exchange_id"),
        nullable=False
    )

    last_price: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False,
        default=0,
    )
