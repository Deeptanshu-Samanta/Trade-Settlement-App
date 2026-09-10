from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import UserCreate
from app.models.wallet import Wallet

password_hash=PasswordHash.recommended()

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def register_user(
    db: Session,
    user_data: UserCreate
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        return None

    hashed_password = password_hash.hash(
        user_data.password
    )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        dob=user_data.dob,
        phone=user_data.phone,
        password=hashed_password
    )

    db.add(new_user)
    db.flush()

    wallet = Wallet(
        user_id=new_user.user_id,
        balance=0
    )

    db.add(wallet)

    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = authenticate_user(
        db,
        email,
        password
    )

    if user is None:
        return None

    return create_access_token(
        user.user_id
    )