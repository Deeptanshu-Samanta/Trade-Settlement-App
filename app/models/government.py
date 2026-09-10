from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Government(Base):
    __tablename__ = "government"

    security_id: Mapped[int] = mapped_column(
        ForeignKey("security.security_id"),
        primary_key=True
    )

    agency: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    jurisdiction: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    clearance_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )