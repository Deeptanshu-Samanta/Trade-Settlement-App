from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    dob: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )