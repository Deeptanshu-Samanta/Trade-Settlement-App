from datetime import date
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database.base import Base
from app.database.connection import engine
from app.database.session import SessionLocal
from app.models import Exchange, Security

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.banks import router as banks_router
from app.routers.securities import router as securities_router
from app.routers.holdings import router as holdings_router
from app.routers.orders import router as orders_router
from app.routers.executions import router as executions_router
from app.routers.cash import router as cash_router
from app.routers.settlement import router as settlement_router



app = FastAPI(
    title="Trading & Settlement System",
    description="Backend API for a trading and settlement system",
    version="1.0.0"
)

NSE_SECURITIES = [
    ("RELIANCE", 1432.50), ("TCS", 3127.40), ("INFY", 1489.20),
    ("HDFCBANK", 1668.35), ("ICICIBANK", 1412.10), ("SBIN", 925.80),
    ("ITC", 422.70), ("LT", 3689.00), ("BHARTIARTL", 2013.60),
    ("HINDUNILVR", 2510.40), ("AXISBANK", 1189.75), ("KOTAKBANK", 1812.30),
    ("MARUTI", 12840.00), ("TATAMOTORS", 692.40), ("SUNPHARMA", 1684.10),
    ("BAJFINANCE", 7345.50), ("ADANIENT", 2468.80), ("ONGC", 241.65),
    ("COALINDIA", 389.20), ("POWERGRID", 286.35), ("NTPC", 337.80),
    ("TITAN", 3479.95), ("ULTRACEMCO", 11786.40), ("WIPRO", 512.70),
    ("HCLTECH", 1498.50),
]


@app.on_event("startup")
def initialise_database() -> None:
    """Create the local schema and seed a small NSE watchlist once."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        nse = db.query(Exchange).filter(Exchange.code == "NSE").first()
        if nse is None:
            nse = Exchange(name="National Stock Exchange", code="NSE")
            db.add(nse)
            db.flush()
        for symbol, price in NSE_SECURITIES:
            found = db.query(Security).filter(Security.symbol == symbol, Security.exchange_id == nse.exchange_id).first()
            if found is None:
                db.add(Security(symbol=symbol, security_date=date.today(), exchange_id=nse.exchange_id, last_price=price))
        db.commit()


# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(banks_router)
app.include_router(securities_router)
app.include_router(holdings_router)
app.include_router(orders_router)
app.include_router(executions_router)
app.include_router(cash_router)
app.include_router(settlement_router)


# Basic test endpoint
@app.get("/")
def root():
    return {
        "message": "Trading & Settlement API is running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/app", include_in_schema=False)
def web_app():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
