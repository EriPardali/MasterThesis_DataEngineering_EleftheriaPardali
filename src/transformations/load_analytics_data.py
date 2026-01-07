import pandas as pd
from sqlalchemy import text
from sqlalchemy.types import Float, Integer, BigInteger, String

from src.db.connection import get_engine


def load_analytics_data() -> None:
    """
    Build analytics KPI tables.
    Reads from staging.loan_kpi_staging
    Writes KPI tables into analytics schema.
    """

    engine = get_engine()

    # Ensure analytics schema exists
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))

    # Read staging table (row-level)
    print("Reading data from staging.loan_kpi_staging ...")
    df = pd.read_sql("SELECT * FROM staging.loan_kpi_staging", con=engine)
    print(f"Rows read from staging: {len(df)}")

    # --- KPI 1: Default Rate ---
    if "loan_status_binary" in df.columns:
        default_rate = df["loan_status_binary"].mean()
    elif "loan_status" in df.columns:
        default_statuses = ["Charged Off", "Late (31-120 days)"]
        default_rate = df["loan_status"].isin(default_statuses).mean()
    else:
        raise ValueError("Cannot compute Default Rate: missing loan_status_binary or loan_status")

    # --- KPI 2: Average Loan Amount ---
    avg_loan_amount = df["loan_amnt"].mean()

    # --- KPI 3: Average Interest Rate ---
    avg_interest_rate = df["int_rate"].mean()

    kpi_summary = pd.DataFrame({
        "kpi": ["default_rate", "avg_loan_amount", "avg_interest_rate"],
        "value": [float(default_rate), float(avg_loan_amount), float(avg_interest_rate)],
    })

    # --- KPI 4: Loan Distribution by Grade ---
    if "grade_ord" not in df.columns:
        raise ValueError("Cannot compute grade distribution: missing grade_ord")

    grade_dist = (
        df["grade_ord"]
        .value_counts(normalize=True)
        .rename_axis("grade_ord")
        .reset_index(name="proportion")
        .sort_values("grade_ord")
    )

    # --- KPI 5: Portfolio Growth (YoY) ---
    if "issue_d_year" not in df.columns:
        raise ValueError("Cannot compute portfolio growth: missing issue_d_year")

    portfolio_by_year = df.groupby("issue_d_year")["loan_amnt"].sum().sort_index()
    growth_rate = portfolio_by_year.pct_change().fillna(0)

    portfolio_growth_df = pd.DataFrame({
        "issue_d_year": portfolio_by_year.index.astype(int),
        "total_loan_amount": portfolio_by_year.values,
        "growth_rate": growth_rate.values,
    })

    # Write KPI tables to analytics schema
    print("Writing KPI tables to analytics schema ...")

    kpi_summary.to_sql(
        name="kpi_portfolio_overview",
        schema="analytics",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={"kpi": String(), "value": Float()},
    )

    grade_dist.to_sql(
        name="kpi_grade_distribution",
        schema="analytics",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={"grade_ord": Integer(), "proportion": Float()},
    )

    portfolio_growth_df.to_sql(
        name="kpi_portfolio_growth",
        schema="analytics",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={"issue_d_year": Integer(), "total_loan_amount": BigInteger(), "growth_rate": Float()},
    )

    print("KPI tables created successfully in analytics schema.")


if __name__ == "__main__":
    load_analytics_data()
