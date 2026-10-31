import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

try:
    engine: Engine | None = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
except Exception:
    engine = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_db_connection() -> dict:
    """Check if the configured database is reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "success",
            "database": "connected",
            "message": "Database connection is successful.",
        }
    except Exception as exc:
        return {
            "database": "disconnected",
        }


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()