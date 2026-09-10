from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.bank import Bank
from app.schemas.bank import BankCreate


def create_bank_account(
    db: Session,
    user_id: int,
    bank_data: BankCreate
):
    bank = Bank(
        account_no=bank_data.account_no,
        ifsc_code=bank_data.ifsc_code,
        bank_name=bank_data.bank_name,
        user_id=user_id,
        linked_at=datetime.now(timezone.utc)
    )

    db.add(bank)
    db.commit()
    db.refresh(bank)

    return bank


def get_my_bank_accounts(
    db: Session,
    user_id: int
):
    return (
        db.query(Bank)
        .filter(Bank.user_id == user_id)
        .all()
    )


def delete_bank_account(
    db: Session,
    account_id: int,
    user_id: int
):
    bank = (
        db.query(Bank)
        .filter(
            Bank.account_id == account_id,
            Bank.user_id == user_id
        )
        .first()
    )

    if bank is None:
        return False

    db.delete(bank)
    db.commit()

    return True