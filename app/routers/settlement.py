from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.trade_execution import TradeExecutionRead
from app.services.settlement_service import settle_execution


router = APIRouter(
    prefix="/settlements",
    tags=["Settlements"]
)


@router.post(
    "/{execution_id}",
    response_model=TradeExecutionRead
)
def settle_trade(
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return settle_execution(
            db,
            execution_id,
            current_user.user_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )