from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.trade_order import (
    TradeOrderCreate,
    TradeOrderRead
)
from app.services.order_service import (
    create_trade_order,
    get_user_orders,
    get_order_by_id,
    cancel_trade_order
)


router = APIRouter(
    prefix="/orders",
    tags=["Trade Orders"]
)


@router.post(
    "",
    response_model=TradeOrderRead,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order_data: TradeOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_trade_order(
            db,
            current_user.user_id,
            order_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "",
    response_model=list[TradeOrderRead]
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_orders(
        db,
        current_user.user_id
    )


@router.get(
    "/{order_id}",
    response_model=TradeOrderRead
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = get_order_by_id(
        db,
        order_id,
        current_user.user_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.delete("/{order_id}")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cancelled = cancel_trade_order(
        db,
        order_id,
        current_user.user_id
    )

    if not cancelled:
        raise HTTPException(
            status_code=404,
            detail="Order not found or cannot be cancelled"
        )

    return {
        "message": "Order cancelled successfully"
    }