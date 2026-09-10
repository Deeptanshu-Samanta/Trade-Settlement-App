from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.security import Security
from app.models.trade_order import TradeOrder
from app.models.holding import Holding
from app.models.wallet import Wallet
from app.schemas.trade_order import TradeOrderCreate


def create_trade_order(
    db: Session,
    user_id: int,
    order_data: TradeOrderCreate
):
    security = (
        db.query(Security)
        .filter(
            Security.security_id ==
            order_data.security_id
        )
        .first()
    )

    if security is None:
        raise ValueError(
            "Security not found"
        )

    if order_data.quantity <= 0:
        raise ValueError(
            "Quantity must be greater than zero"
        )

    order_type = order_data.order_type.upper()
    if order_type not in {
        "BUY",
        "SELL"
    }:
        raise ValueError(
            "Order type must be BUY or SELL"
        )

    # Reject trades that cannot settle before creating an order.  The same
    # checks are retained at settlement time to protect concurrent requests.
    execution_price = float(security.last_price)
    if execution_price <= 0:
        raise ValueError("A quote is not available for this security")
    trade_value = order_data.quantity * execution_price
    if order_type == "BUY":
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if wallet is None or float(wallet.balance) < trade_value:
            raise ValueError("Insufficient wallet balance")
    else:
        holding = db.query(Holding).filter(
            Holding.user_id == user_id,
            Holding.security_id == order_data.security_id,
        ).first()
        if holding is None or float(holding.quantity) < order_data.quantity:
            raise ValueError("Insufficient security quantity")

    order = TradeOrder(
        user_id=user_id,
        security_id=order_data.security_id,
        order_type=order_type,
        quantity=order_data.quantity,
        price=execution_price,
        order_date=datetime.now(timezone.utc),
        status="PENDING"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def get_user_orders(
    db: Session,
    user_id: int
):
    return (
        db.query(TradeOrder)
        .filter(TradeOrder.user_id == user_id)
        .order_by(TradeOrder.order_date.desc())
        .all()
    )


def get_order_by_id(
    db: Session,
    order_id: int,
    user_id: int
):
    return (
        db.query(TradeOrder)
        .filter(
            TradeOrder.order_id == order_id,
            TradeOrder.user_id == user_id
        )
        .first()
    )


def cancel_trade_order(
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
        return False

    if order.status != "PENDING":
        return False

    order.status = "CANCELLED"

    db.commit()

    return True
