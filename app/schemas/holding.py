from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HoldingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    holding_id: int
    user_id: int
    security_id: int
    quantity: float
    avg_price: float
    update_date: datetime