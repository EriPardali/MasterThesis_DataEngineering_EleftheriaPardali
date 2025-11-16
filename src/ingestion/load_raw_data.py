import psycopg2
import csv
import os

def load_fast():
    csv_path = "data/loan.csv"
    conn = psycopg2.connect(
        dbname="loan_portfolio_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Creating table raw.lending_club_loans...")

    cur.execute("""
        DROP TABLE IF EXISTS raw.lending_club_loans;

        CREATE TABLE raw.lending_club_loans (
            id BIGINT,
            member_id BIGINT,
            loan_amnt INTEGER,
            funded_amnt INTEGER,
            funded_amnt_inv INTEGER,
            term TEXT,
            int_rate TEXT,
            installment TEXT,
            grade TEXT,
            sub_grade TEXT,
            emp_title TEXT,
            emp_length TEXT,
            home_ownership TEXT,
            annual_inc REAL,
            verification_status TEXT,
            issue_d TEXT,
            loan_status TEXT,
            purpose TEXT,
            title TEXT,
            zip_code TEXT,
            addr_state TEXT,
            earliest_cr_line TEXT,
            -- ... Μπορούμε να προσθέσουμε και τα υπόλοιπα 145 columns,
            -- ή να κάνουμε dynamic load.
            dummy TEXT
        );
    """)

    conn.commit()

    print("Loading file with COPY...")

    with open(csv_path, "r", encoding="utf-8") as f:
        next(f)  
        cur.copy_expert("""
            COPY raw.lending_club_loans
            FROM STDIN
            WITH (FORMAT csv, NULL '', DELIMITER ',', QUOTE '\"');
        """, f)

    conn.commit()
    cur.close()
    conn.close()

    print(" Fast ingest complete.")
    

if __name__ == "__main__":
    load_fast()
