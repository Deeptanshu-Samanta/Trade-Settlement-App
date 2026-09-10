from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.trade_execution import TradeExecutionRead
from app.services.execution_service import (
    get_user_executions,
    get_execution_by_id,
    execute_trade_order
)


router = APIRouter(
    prefix="/executions",
    tags=["Trade Executions"]
)


@router.get(
    "",
    response_model=list[TradeExecutionRead]
)
def get_my_executions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_executions(
        db,
        current_user.user_id
    )

@router.post(
    "/order/{order_id}",
    response_model=TradeExecutionRead
)
def execute_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        execution = execute_trade_order(
            db,
            order_id,
            current_user.user_id
        )

        if execution is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return execution

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/{execution_id}",
    response_model=TradeExecutionRead
)
def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    execution = get_execution_by_id(
        db,
        execution_id,
        current_user.user_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    return execution