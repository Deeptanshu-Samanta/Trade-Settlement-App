from pathlib import Path

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# A file database keeps the demo usable on a new machine.  Set DATABASE_URL to
# a PostgreSQL URL in .env when deploying the application.
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{Path(__file__).resolve().parents[2] / 'trade_app.db'}"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

