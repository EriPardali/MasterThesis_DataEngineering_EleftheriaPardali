import csv
from pathlib import Path
from src.db.connection import get_engine


STAGING_CSV = Path("data/processed/loan_kpi_staging.csv")


def load_into_staging():
    engine = get_engine()
    print("Loading KPI dataset into staging.loan_applications ...")

    sql = """
        COPY staging.loan_applications (
            id,
            member_id,
            loan_amnt,
            funded_amnt,
            int_rate,
            installment,
            sub_grade,
            issue_d,
            issue_d_year,
            issue_d_month,
            annual_inc,
            dti,
            emp_length_years,
            addr_state,
            revol_bal,
            revol_util,
            credit_history_age_months,
            total_pymnt,
            total_rec_prncp,
            total_rec_int,
            recoveries,
            last_pymnt_d,
            last_pymnt_amnt,
            payment_to_loan_ratio,
            income_to_loan_ratio,
            grade_ord,
            sub_grade_ord,
            loan_status_binary
        )
        FROM STDIN
        WITH CSV HEADER DELIMITER ',' QUOTE '\"'
    """

    with engine.raw_connection() as conn:
        cur = conn.cursor()

        with open(STAGING_CSV, "r", encoding="utf-8") as f:
            cur.copy_expert(sql, f)

        conn.commit()

    print("Staging load complete ✔️")
    

if __name__ == "__main__":
    load_into_staging()
