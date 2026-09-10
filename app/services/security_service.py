from sqlalchemy.orm import Session

from app.models.security import Security


def get_all_securities(
    db: Session
):
    return (
        db.query(Security)
        .order_by(Security.symbol)
        .all()
    )


def get_security_by_id(
    db: Session,
    security_id: int
):
    return (
        db.query(Security)
        .filter(
            Security.security_id == security_id
        )
        .first()
    )