from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException,APIRouter,Depends

from app.core.security import get_current_user
from app.database.session import get_db
from app.schemas.security import SecurityRead
from app.services.security_service import (
    get_all_securities,
    get_security_by_id
)


router = APIRouter(
    prefix="/securities",
    tags=["Securities"]
)


@router.get(
    "",
    response_model=list[SecurityRead]
)
def get_securities(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_securities(db)


@router.get(
    "/{security_id}",
    response_model=SecurityRead
)
def get_security(
    security_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    security = get_security_by_id(
        db,
        security_id
    )

    if security is None:
        raise HTTPException(
            status_code=404,


            detail="Security not found"
    )

    return security