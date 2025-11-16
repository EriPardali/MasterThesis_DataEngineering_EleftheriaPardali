import csv
from pathlib import Path
from src.db.connection import get_engine


# Path to the raw CSV file (relative to project root)
CSV_PATH = Path("data/loan.csv")


def create_raw_table_if_not_exists(engine) -> None:
    """
    Reads the CSV header and creates the table raw.lending_club_loans
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

    CREATE TABLE IF NOT EXISTS raw.lending_club_loans (
        {column_definitions}
    );
    """

    print("Creating table raw.lending_club_loans (if not exists)...")
    with engine.connect() as conn:
        conn.exec_driver_sql(ddl)
        conn.commit()

    print("Table creation check completed.")


def load_raw_data_with_copy() -> None:
    """
    Loads the FULL Lending Club dataset into PostgreSQL using COPY,
    which is the fastest and most efficient method for bulk ingestion.
    """
    engine = get_engine()
    print(f"Using CSV file: {CSV_PATH}")

    # 1. Create raw table structure if needed
    create_raw_table_if_not_exists(engine)

    # 2. COPY data into PostgreSQL
    print("Opening raw_connection() for COPY...")
    conn = engine.raw_connection()

    try:
        with conn.cursor() as cur, CSV_PATH.open("r", encoding="utf-8") as f:
            print("Starting COPY into raw.lending_club_loans ...")
            copy_sql = """
                COPY raw.lending_club_loans
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


