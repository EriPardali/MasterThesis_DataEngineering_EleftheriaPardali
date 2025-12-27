from sqlalchemy import BigInteger, Integer, SmallInteger, Numeric, Date, Text, String

STAGING_DTYPES = {
    "loan_amnt": Numeric(12, 2),
    "int_rate": Numeric(6, 4),
    "installment": Numeric(12, 2),
    "sub_grade": Text,
    "issue_d": Date,
    "issue_d_year": SmallInteger,
    "issue_d_month": SmallInteger,
    "annual_inc": Numeric(14, 2),
    "dti": Numeric(7, 4),
    "emp_length_years": SmallInteger,
    "addr_state": String(2),
    "revol_bal": BigInteger,
    "revol_util": Numeric(7, 4),
    "credit_history_age_months": Integer,
    "total_pymnt": Numeric(14, 2),
    "total_rec_int": Numeric(14, 2),
    "recoveries": Numeric(14, 2),
    "last_pymnt_d": Date,
    "last_pymnt_amnt": Numeric(14, 2),
    "payment_to_loan_ratio": Numeric(14, 6),
    "income_to_loan_ratio": Numeric(14, 6),
    "grade_ord": SmallInteger,
    "sub_grade_ord": SmallInteger,
    "loan_status_binary": SmallInteger,
}

