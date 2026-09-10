from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CashDepositCreate(BaseModel):
    amount: float
    description: str | None = None


class CashTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transaction_id: int
    wallet_id: int
    transaction_type: str
    amount: float
    transaction_date: datetime
    description: str | None