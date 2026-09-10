from datetime import date

from pydantic import BaseModel, ConfigDict


class SecurityCreate(BaseModel):
    symbol: str
    security_date: date
    exchange_id: int
    last_price: float


class SecurityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    security_id: int
    symbol: str
    security_date: date
    exchange_id: int
    last_price: float
