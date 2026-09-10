from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Wallet(Base):
    __tablename__ = "wallet"

    wallet_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        unique=True
    )

    balance: Mapped[float] = mapped_column(
        Numeric(20, 4),
        nullable=False,
        default=0
    )