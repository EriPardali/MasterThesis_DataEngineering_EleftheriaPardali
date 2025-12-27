import pandas as pd
from pathlib import Path
from src.db.connection import get_engine
from src.schemas.staging_schema import STAGING_DTYPES


def load_analytics_data():
    engine = get_engine()

    print("Reading from staging.loan_portfolio_features ...")
    df = pd.read_sql("SELECT * FROM staging.loan_portfolio_features", engine)

    print("Writing to analytics.loan_portfolio_features ...")
    df.to_sql(
        name="loan_portfolio_features",
        schema="analytics",
        con=engine,
        if_exists="replace",
        index=False,
        dtype=STAGING_DTYPES
    )

    print("Completed loading into analytics.loan_portfolio_features.")

if __name__ == "__main__":
    load_analytics_data()
