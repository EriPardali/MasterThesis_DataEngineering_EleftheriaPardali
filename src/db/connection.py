import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine.

    Priority:
    1) AIRFLOW_CONN_THESIS_POSTGRES (Airflow-style connection, used in Docker/Airflow)
    2) DATABASE_URL (generic, used for local runs)
    """

    db_url = (
        os.getenv("AIRFLOW_CONN_THESIS_POSTGRES")
        or os.getenv("DATABASE_URL")
    )

    if not db_url:
        raise RuntimeError(
            "No database connection string found. "
            "Set AIRFLOW_CONN_THESIS_POSTGRES (Airflow/Docker) "
            "or DATABASE_URL (local)."
        )

    return create_engine(
        db_url,
        pool_pre_ping=True,
        future=True,
    )
