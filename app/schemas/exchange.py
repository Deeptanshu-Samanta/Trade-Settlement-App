from pydantic import BaseModel, ConfigDict


class ExchangeCreate(BaseModel):
    name: str
    code: str


class ExchangeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exchange_id: int
    name: str
    code: str