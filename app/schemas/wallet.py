from pydantic import BaseModel, ConfigDict


class WalletRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_id: int
    user_id: int
    balance: float