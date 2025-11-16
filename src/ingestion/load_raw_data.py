import pandas as pd
from src.db.connection import get_engine


def load_raw_data():
    """
    Loads the raw Lending Club dataset from a local CSV file
    and inserts it into the PostgreSQL table raw.lending_club_loans.
    """
    csv_path = "data/loan.csv"  
    print(f" Reading CSV from: {csv_path}")

    df = pd.read_csv(csv_path)
    print(" DataFrame shape:", df.shape)

    #Basic preprocessing (convert date columns) 
    if "issue_date" in df.columns:
        df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")

    if "earliest_credit_line" in df.columns:
        df["earliest_credit_line"] = pd.to_datetime(df["earliest_credit_line"], errors="coerce")

    print(" Connecting to PostgreSQL...")
    engine = get_engine()

    print(" Loading data into raw.lending_club_loans...")

    df.to_sql(
        name="lending_club_loans",
        con=engine,
        schema="raw",
        if_exists="append",
        index=False,
    )

if __name__ == "__main__":
    load_raw_data()
