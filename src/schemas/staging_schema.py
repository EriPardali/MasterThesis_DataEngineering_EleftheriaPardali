# src/schemas/staging_schema.py
from sqlalchemy import (
    BigInteger, Float, Text
)

STAGING_DTYPES = {
    "loan_amnt": BigInteger(),
    "term_months": Float(),
    "int_rate": Float(),
    "installment": Float(),
    "grade_ord": Float(),
    "sub_grade_ord": Float(),
    "emp_length_years": Float(),
    "annual_inc": Float(),
    "dti": Float(),
    "revol_util": Float(),
    "inq_last_6mths": Float(),
    "open_acc": Float(),
    "total_acc": Float(),
    "issue_d_year": Float(),
    "issue_d_month": Float(),
    "earliest_cr_line_year": Float(),
    "earliest_cr_line_month": Float(),
    "credit_history_age_months": Float(),
    "addr_state": Text(),
    "loan_status": Text(),
    "total_pymnt": Float(),
    "total_rec_prncp": Float(),
}
