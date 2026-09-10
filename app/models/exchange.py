from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Exchange(Base):
    __tablename__ = "exchange"

    exchange_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )