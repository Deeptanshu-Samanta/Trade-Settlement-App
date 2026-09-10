from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.trade_execution import TradeExecution
from app.models.trade_order import TradeOrder


def execute_trade_order(
    db: Session,
    order_id: int,
    user_id: int
):
    order = (
        db.query(TradeOrder)
        .filter(
            TradeOrder.order_id == order_id,
            TradeOrder.user_id == user_id
        )
        .first()
    )

    if order is None:
        return None

    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be executed"
        )

    execution = TradeExecution(
        order_id=order.order_id,
        execution_qty=order.quantity,
        execution_price=order.price,
        execution_date=datetime.now(timezone.utc),
        settlement_status="PENDING",
        settlement_date=None
    )

    order.status = "EXECUTED"

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution


def get_user_executions(
    db: Session,
    user_id: int
):
    return (
        db.query(TradeExecution)
        .join(
            TradeOrder,
            TradeExecution.order_id ==
            TradeOrder.order_id
        )
        .filter(
            TradeOrder.user_id == user_id
        )
        .order_by(
            TradeExecution.execution_date.desc()
        )
        .all()
    )


def get_execution_by_id(
    db: Session,
    execution_id: int,
    user_id: int
):
    return (
        db.query(TradeExecution)
        .join(
            TradeOrder,
            TradeExecution.order_id ==
            TradeOrder.order_id
        )
        .filter(
            TradeExecution.execution_id ==
            execution_id,
            TradeOrder.user_id == user_id
        )
        .first()
    )