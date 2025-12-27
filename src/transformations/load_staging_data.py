import pandas as pd
from pathlib import Path
from src.db.connection import get_engine
from src.schemas.staging_schema import STAGING_DTYPES


# Path to the processed CSV produced during feature engineering
CSV_PATH = Path("data/processed/loan_kpi_staging_typed.csv")


def load_staging_data():
    """
    Load processed feature-engineered data into the staging schema.
    Replaces the staging table on every run.
    """
    engine = get_engine()

    print(f"Loading processed features from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    print("Writing to staging.loan_portfolio_features ...")
    df.to_sql(
        name="loan_portfolio_features",
        schema="staging",
        con=engine,
        if_exists="replace",
        index=False,
        dtype=STAGING_DTYPES
    )

    print("Completed loading into staging.loan_portfolio_features.")


if __name__ == "__main__":
    load_staging_data()
