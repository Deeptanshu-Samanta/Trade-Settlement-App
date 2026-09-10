from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.holding import HoldingRead
from app.services.holding_service import (
    get_user_holdings,
    get_holding_by_id
)


router = APIRouter(
    prefix="/holdings",
    tags=["Holdings"]
)


@router.get(
    "",
    response_model=list[HoldingRead]
)
def get_my_holdings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_holdings(
        db,
        current_user.user_id
    )


@router.get(
    "/{holding_id}",
    response_model=HoldingRead
)
def get_my_holding(
    holding_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = get_holding_by_id(
        db,
        holding_id,
        current_user.user_id
    )

    if holding is None:
        raise HTTPException(status_code=404, detail="Holding not found")

    return holding
