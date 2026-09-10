from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TradeExecutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    execution_id: int
    order_id: int
    execution_qty: float
    execution_price: float
    execution_date: datetime
    settlement_status: str
    settlement_date: datetime | None