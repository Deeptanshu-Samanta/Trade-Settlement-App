from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.cash_transaction import (
    CashDepositCreate,
    CashTransactionRead
)
from app.services.cash_service import (
    deposit_cash,
    get_user_cash_transactions
)
from app.schemas.wallet import WalletRead

from app.services.cash_service import (
    deposit_cash,
    get_user_cash_transactions,
    get_user_balance
)


router = APIRouter(
    prefix="/cash",
    tags=["Cash"]
)


@router.post(
    "/deposit",
    response_model=CashTransactionRead
)
def deposit(
    deposit_data: CashDepositCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return deposit_cash(
            db,
            current_user.user_id,
            deposit_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/transactions",
    response_model=list[CashTransactionRead]
)
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_cash_transactions(
        db,
        current_user.user_id
    )


@router.get(
    "/balance",
    response_model=WalletRead
)
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_user_balance(
            db,
            current_user.user_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )