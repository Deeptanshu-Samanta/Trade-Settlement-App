from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def get_user_wallet(
    db: Session,
    user_id: int
):
    return (
        db.query(Wallet)
        .filter(
            Wallet.user_id == user_id
        )
        .first()
    )


def create_wallet(
    db: Session,
    user_id: int
):
    existing_wallet = get_user_wallet(
        db,
        user_id
    )

    if existing_wallet:
        return existing_wallet

    wallet = Wallet(
        user_id=user_id,
        balance=0
    )

    db.add(wallet)
    db.commit()
    db.refresh(wallet)

    return wallet