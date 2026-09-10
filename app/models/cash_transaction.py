from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CashTransaction(Base):
    __tablename__ = "cash_transaction"

    transaction_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallet.wallet_id"),
        nullable=False
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )