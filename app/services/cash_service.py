from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.cash_transaction import CashTransaction
from app.models.bank import Bank
from app.models.wallet import Wallet
from app.schemas.cash_transaction import CashDepositCreate


def deposit_cash(
    db: Session,
    user_id: int,
    deposit_data: CashDepositCreate
):
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

    if not db.query(Bank).filter(Bank.user_id == user_id).first():
        raise ValueError("Link a bank account before adding funds")

    if deposit_data.amount <= 0:
        raise ValueError(
            "Deposit amount must be greater than zero"
        )

    transaction = CashTransaction(
        wallet_id=wallet.wallet_id,
        transaction_type="DEPOSIT",
        amount=deposit_data.amount,
        transaction_date=datetime.now(timezone.utc),
        description=deposit_data.description
    )

    wallet.balance += Decimal(str(deposit_data.amount))

    db.add(transaction)
    db.commit()

    db.refresh(transaction)

    return transaction


def get_user_cash_transactions(
    db: Session,
    user_id: int
):
    return (
        db.query(CashTransaction)
        .join(
            Wallet,
            CashTransaction.wallet_id ==
            Wallet.wallet_id
        )
        .filter(
            Wallet.user_id == user_id
        )
        .order_by(
            CashTransaction.transaction_date.desc()
        )
        .all()
    )


def get_user_balance(
    db: Session,
    user_id: int
):
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

    return wallet
