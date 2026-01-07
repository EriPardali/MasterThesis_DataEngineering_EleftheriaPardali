from sqlalchemy import text
from src.db.connection import get_engine


def test_db_connection_works():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()

    assert result == 1