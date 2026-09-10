from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.bank import BankCreate, BankRead
from app.services.bank_service import create_bank_account, delete_bank_account, get_my_bank_accounts


router = APIRouter(
    prefix="/banks",
    tags=["Banks"]
)


@router.post(
    "",
    response_model=BankRead
)
def add_bank_account(
    bank_data: BankCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_bank_account(db, current_user.user_id, bank_data)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="This account is already linked")


@router.get("", response_model=list[BankRead])
def list_bank_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_bank_accounts(db, current_user.user_id)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_bank_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not delete_bank_account(db, account_id, current_user.user_id):
        raise HTTPException(status_code=404, detail="Bank account not found")
