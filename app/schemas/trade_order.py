from pydantic import BaseModel, ConfigDict, Field


class TradeOrderCreate(BaseModel):
    security_id: int
    order_type: str
    quantity: float = Field(gt=0)
    # Quotes are server-side demo prices.  Kept optional for API clients; any
    # submitted value is ignored rather than trusted as an execution price.
    price: float | None = Field(default=None, gt=0)

from datetime import datetime

class TradeOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    user_id: int
    security_id: int
    order_type: str
    order_date: datetime
    status: str
    quantity: float
    price: float
