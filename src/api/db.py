import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db_url() -> str:
    db_url = os.getenv("AIRFLOW_CONN_THESIS_POSTGRES") or os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "No database URL found. Set AIRFLOW_CONN_THESIS_POSTGRES (Docker/Airflow) "
            "or DATABASE_URL (local)."
        )
    return db_url

engine = create_engine(get_db_url(), pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
