from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Corporate(Base):
    __tablename__ = "corporate"

# here the fk itself acts as the pk.
    security_id: Mapped[int] = mapped_column(
        ForeignKey("security.security_id"),
        primary_key=True
    )

    company_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    risk_factor: Mapped[float | None] = mapped_column(
        Numeric(5, 2)
    )

    industry: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )