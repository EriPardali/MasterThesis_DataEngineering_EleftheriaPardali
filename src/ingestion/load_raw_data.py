import csv
from pathlib import Path
from src.db.connection import get_engine


# Absolute path to the raw CSV file
CSV_PATH = Path(r"C:\Users\parda\OneDrive\Desktop\Thesis\data\loan.csv")


def create_raw_table_if_not_exists(engine) -> None:
    """
    Reads the CSV header and recreates the table raw.loan_portfolio
    with all columns as TEXT (schema-on-read approach).
    """
    print(f"Reading CSV header from: {CSV_PATH}")

    # Read only the first row (column names)
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    # Build TEXT columns
    column_definitions = ",\n    ".join(
        [f'"{col}" TEXT' for col in header]
    )

    ddl = f"""
    CREATE SCHEMA IF NOT EXISTS raw;

    DROP TABLE IF EXISTS raw.loan_portfolio;

    CREATE TABLE raw.loan_portfolio (
        {column_definitions}
    );
    """

    print("Recreating table raw.loan_portfolio ...")
    with engine.connect() as conn:
        conn.exec_driver_sql(ddl)
        conn.commit()

    print("Table creation completed.")


def load_raw_data_with_copy() -> None:
    """
    Loads the Lending Club dataset into PostgreSQL using COPY.
    """
    engine = get_engine()
    print(f"Using CSV file: {CSV_PATH}")

    # 1. Create raw table structure
    create_raw_table_if_not_exists(engine)

    # 2. COPY data into PostgreSQL
    print("Opening raw_connection() for COPY...")
    conn = engine.raw_connection()

    try:
        with conn.cursor() as cur, CSV_PATH.open("r", encoding="utf-8") as f:
            print("Starting COPY into raw.loan_portfolio ...")
            copy_sql = """
                COPY raw.loan_portfolio
                FROM STDIN
                WITH (FORMAT csv, HEADER true)
            """
            cur.copy_expert(copy_sql, f)

        conn.commit()
        print("COPY completed successfully.")

    finally:
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    load_raw_data_with_copy()
