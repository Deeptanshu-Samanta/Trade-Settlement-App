from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.cash_transaction import CashTransaction
from app.models.holding import Holding
from app.models.trade_execution import TradeExecution
from app.models.trade_order import TradeOrder
from app.models.wallet import Wallet


def settle_execution(
    db: Session,
    execution_id: int,
    user_id: int
):
    execution = (
        db.query(TradeExecution)
        .join(
            TradeOrder,
            TradeExecution.order_id ==
            TradeOrder.order_id
        )
        .filter(
            TradeExecution.execution_id == execution_id,
            TradeOrder.user_id == user_id
        )
        .first()
    )

    if execution is None:
        raise ValueError(
            "Execution not found"
        )

    if execution.settlement_status != "PENDING":
        raise ValueError(
            "Execution is already settled"
        )

    order = (
        db.query(TradeOrder)
        .filter(
            TradeOrder.order_id ==
            execution.order_id
        )
        .first()
    )

    wallet = (
        db.query(Wallet)
        .filter(
            Wallet.user_id == user_id
        )
        .first()
    )

    if wallet is None:
        raise ValueError(
            "Wallet not found"
        )

    trade_value = Decimal(str(execution.execution_qty)) * Decimal(str(execution.execution_price))

    holding = (
        db.query(Holding)
        .filter(
            Holding.user_id == user_id,
            Holding.security_id == order.security_id
        )
        .first()
    )

    if order.order_type == "BUY":

        if wallet.balance < trade_value:
            raise ValueError(
                "Insufficient wallet balance"
            )

        wallet.balance = Decimal(str(wallet.balance)) - trade_value

        if holding is None:

            holding = Holding(
                user_id=user_id,
                security_id=order.security_id,
                quantity=execution.execution_qty,
                avg_price=execution.execution_price,
                update_date=datetime.now(timezone.utc)
            )

            db.add(holding)

        else:

            old_quantity = holding.quantity
            old_avg_price = holding.avg_price

            new_quantity = (
                old_quantity +
                execution.execution_qty
            )

            new_avg_price = (
                (
                    old_quantity * old_avg_price
                ) +
                (
                    execution.execution_qty *
                    execution.execution_price
                )
            ) / new_quantity

            holding.quantity = new_quantity
            holding.avg_price = new_avg_price
            holding.update_date = datetime.now(timezone.utc)

        cash_transaction = CashTransaction(
            wallet_id=wallet.wallet_id,
            transaction_type="BUY",
            amount=trade_value,
            transaction_date=datetime.now(timezone.utc),
            description=f"BUY settlement for execution {execution.execution_id}"
        )

        db.add(cash_transaction)

    elif order.order_type == "SELL":

        if holding is None:
            raise ValueError(
                "No holding available for this security"
            )

        if holding.quantity < execution.execution_qty:
            raise ValueError(
                "Insufficient security quantity"
            )

        holding.quantity -= execution.execution_qty
        holding.update_date = datetime.now(timezone.utc)

        wallet.balance = Decimal(str(wallet.balance)) + trade_value

        cash_transaction = CashTransaction(
            wallet_id=wallet.wallet_id,
            transaction_type="SELL",
            amount=trade_value,
            transaction_date=datetime.now(timezone.utc),
            description=f"SELL settlement for execution {execution.execution_id}"
        )

        db.add(cash_transaction)

    else:
        raise ValueError(
            "Invalid order type"
        )

    execution.settlement_status = "SETTLED"
    execution.settlement_date = datetime.now(timezone.utc)

    db.commit()
    db.refresh(execution)

    return execution
