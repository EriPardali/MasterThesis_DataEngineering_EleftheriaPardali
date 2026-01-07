from pathlib import Path
import pandas as pd
from sqlalchemy import text

from src.db.connection import get_engine
from src.schemas.staging_schema import STAGING_DTYPES

DATA_DIR = Path("/opt/airflow/data")
CSV_PATH = DATA_DIR / "processed" / "loan_kpi_staging_typed.csv"

TARGET_SCHEMA = "staging"
TARGET_TABLE = "loan_kpi_staging"


def load_staging_data():
    engine = get_engine()

    print(f"Loading processed features from: {CSV_PATH}")

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Input CSV not found inside container: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # ---- column sanity checks ----
    missing = set(STAGING_DTYPES) - set(df.columns)
    extra = set(df.columns) - set(STAGING_DTYPES)

    if missing:
        raise ValueError(
            f"CSV missing columns defined in STAGING_DTYPES: {sorted(missing)}"
        )
    if extra:
        print(
            f"Warning: CSV has extra columns not in STAGING_DTYPES: {sorted(extra)}"
        )

    # ---- ensure schema exists ----
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {TARGET_SCHEMA};"))

    # ---- load with enforced SQL types ----
    df.to_sql(
        TARGET_TABLE,
        engine,
        schema=TARGET_SCHEMA,
        if_exists="replace",  
        index=False,
        method="multi",
        chunksize=5000,
        dtype=STAGING_DTYPES,  
    )

    print(f"Loaded {len(df)} rows into {TARGET_SCHEMA}.{TARGET_TABLE}")


if __name__ == "__main__":
    load_staging_data()
