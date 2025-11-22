import csv
from datetime import datetime
from pathlib import Path
from src.db.connection import get_engine

RAW_CSV = Path("data/loan_raw.csv")


def load_into_staging():
    engine = get_engine()
    print("Loading cleaned data into staging.loan_applications ...")
    
    sql = """
        COPY staging.loan_applications(
            loan_id,
            member_id,
            loan_amnt,
            int_rate,
            loan_status,
            grade,
            sub_grade,
            issue_d
        )
        FROM STDIN
        WITH CSV HEADER DELIMITER ',' QUOTE '\"';
    """
    
    with engine.raw_connection() as conn:
        with conn.cursor() as cur, RAW_CSV.open("r", encoding="utf-8") as f:
            cur.copy_expert(sql, f)
        conn.commit()

    print("Staging load complete.")
