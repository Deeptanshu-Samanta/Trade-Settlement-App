from sqlalchemy.orm import Session

from app.models.holding import Holding


def get_user_holdings(
    db: Session,
    user_id: int
):
    return (
        db.query(Holding)
        .filter(Holding.user_id == user_id)
        .all()
    )


def get_holding_by_id(
    db: Session,
    holding_id: int,
    user_id: int
):
    return (
        db.query(Holding)
        .filter(
            Holding.holding_id == holding_id,
            Holding.user_id == user_id
        )
        .first()
    )