from datetime import date, timedelta
import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

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


@router.get("/{security_id}/timeline")
def get_security_timeline(
    security_id: int,
    days: int = Query(default=90, ge=15, le=365),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    security = get_security_by_id(db, security_id)

    if security is None:
        raise HTTPException(
            status_code=404,
            detail="Security not found"
        )

    base_price = float(security.last_price)
    seed = sum(ord(char) for char in security.symbol)
    trend = ((seed % 13) - 5) / 2400
    volatility = 0.011 + (seed % 8) / 1000
    start = date.today() - timedelta(days=days - 1)
    price = base_price * (1 - trend * days / 2)
    points = []

    for index in range(days):
        wave = math.sin((index + seed) / 5.0) * volatility
        pulse = math.cos((index + seed) / 11.0) * volatility * 0.55
        move = trend + wave + pulse
        open_price = price
        close_price = max(1, open_price * (1 + move))
        high_price = max(open_price, close_price) * (1 + volatility * (0.45 + ((index + seed) % 5) / 10))
        low_price = min(open_price, close_price) * (1 - volatility * (0.35 + ((index + seed) % 4) / 10))
        volume = 850000 + ((seed * 977 + index * 13791) % 4200000)
        points.append({
            "date": (start + timedelta(days=index)).isoformat(),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume,
        })
        price = close_price

    if points:
        latest = points[-1]["close"] or 1
        factor = base_price / latest
        for point in points:
            point["open"] = round(point["open"] * factor, 2)
            point["high"] = round(point["high"] * factor, 2)
            point["low"] = round(point["low"] * factor, 2)
            point["close"] = round(point["close"] * factor, 2)

    return {
        "security_id": security.security_id,
        "symbol": security.symbol,
        "points": points,
    }
