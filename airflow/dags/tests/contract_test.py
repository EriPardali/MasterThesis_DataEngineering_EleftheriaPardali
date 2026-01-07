from sqlalchemy import text
from src.db.connection import get_engine


def test_analytics_table_exists():
    engine = get_engine()

    q = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'analytics'
              AND table_name = 'loan_portfolio_features'
        );
    """)

    with engine.connect() as conn:
        exists = conn.execute(q).scalar()

    assert exists is True


def test_required_columns_exist():
    """
    Columns that our KPI endpoints rely on.
    """
    required = {
        "loan_amnt",
        "int_rate",
        "issue_d",               # used for portfolio_growth
        "loan_status_binary",    # used for default_rate (your table has this, not loan_status)
        "grade_ord",             # used for loan_distribution_by_grade (your table has grade_ord, not grade)
    }

    engine = get_engine()

    q = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'analytics'
          AND table_name = 'loan_portfolio_features';
    """)

    with engine.connect() as conn:
        cols = {row[0] for row in conn.execute(q).fetchall()}

    missing = required - cols
    assert not missing, f"Missing columns: {missing}"