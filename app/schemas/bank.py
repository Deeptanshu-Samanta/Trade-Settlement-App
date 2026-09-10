from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BankCreate(BaseModel):
    account_no: str
    ifsc_code: str
    bank_name: str


class BankRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    account_no: str
    ifsc_code: str
    bank_name: str
    linked_at: datetime
    user_id: int