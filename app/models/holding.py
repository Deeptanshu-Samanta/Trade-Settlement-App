from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Holding(Base):
    __tablename__ = "holdings"

    holding_id: Mapped[int] = mapped_column(
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

    quantity: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    avg_price: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    update_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )