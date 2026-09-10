from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Bank(Base):
    __tablename__ = "bank"

    account_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    account_no: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True
    )

    ifsc_code: Mapped[str] = mapped_column(
        String(11),
        nullable=False
    )

    bank_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    linked_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )