import pandas as pd
import numpy as np
import re
from pathlib import Path

# Paths inside Airflow containers
INPUT_FILE = Path("/opt/airflow/data/loan.csv")
OUTPUT_FILE = Path("/opt/airflow/data/processed/loan_features.csv")
PROCESSED_DIR = OUTPUT_FILE.parent

CHUNK_SIZE = 100_000

# Keep only what is needed 
BASE_COLS = [
    "loan_amnt", "int_rate", "term", "installment",
    "grade", "sub_grade", "purpose", "annual_inc", "dti",
    "home_ownership", "addr_state", "delinq_2yrs", "inq_last_6mths",
    "revol_util", "open_acc", "total_acc", "earliest_cr_line",
    "loan_status", "total_pymnt", "total_rec_prncp", "recoveries",
    "issue_d", "emp_length"
]

ENGINEERED_COLS = [
    "term_months", "emp_length_years", "grade_ord", "sub_grade_ord",
    "issue_year", "issue_month", "earliest_cr_line_year", "earliest_cr_line_month",
    "credit_history_age_months", "payment_to_loan_ratio", "income_to_loan_ratio"
]


def emp_len_to_years(x) -> float:
    if pd.isna(x):
        return np.nan
    s = str(x).strip().lower()
    if s.startswith("<"):
        return 0.0
    m = re.search(r"(\d+)", s)
    if not m:
        return np.nan
    val = float(m.group(1))
    return 10.0 if "+" in s else val


def subgrade_to_ord(x) -> float:
    if pd.isna(x):
        return np.nan
    s = str(x).strip().upper()
    if len(s) < 2:
        return np.nan
    letter, num = s[0], s[1:]
    if letter not in "ABCDEFG" or not num.isdigit():
        return np.nan
    base = (ord(letter) - ord("A")) * 5
    return float(base + int(num))


def transform_chunk(fe: pd.DataFrame) -> pd.DataFrame:
    # ---- EDA consistency: remove non-originated loans ----
    if "loan_status" in fe.columns:
        fe = fe[
            ~fe["loan_status"].astype(str).str.strip().str.contains(
                "Does not meet the credit policy", na=False)
        ].copy()
    # term -> months
    if "term" in fe.columns:
        fe["term_months"] = pd.to_numeric(
            fe["term"].astype(str).str.extract(r"(\d+)")[0],
            errors="coerce"
        ).astype("float32")

    # Employment_length -> years
    if "emp_length" in fe.columns:
        fe["emp_length_years"] = fe["emp_length"].apply(emp_len_to_years).astype("float32")

    # grade -> ordinal
    if "grade" in fe.columns:
        grade_order = {"g": 1, "f": 2, "e": 3, "d": 4, "c": 5, "b": 6, "a": 7}
        fe["grade_ord"] = fe["grade"].astype(str).str.lower().map(grade_order).astype("float32")

    # sub_grade -> ordinal
    if "sub_grade" in fe.columns:
        fe["sub_grade_ord"] = fe["sub_grade"].apply(subgrade_to_ord).astype("float32")

    # Dates (Dec-2015)
    FMT = "%b-%Y"
    issue_dt = pd.to_datetime(
        fe["issue_d"].astype(str).str.strip(),
        format=FMT,
        errors="coerce"
    ) if "issue_d" in fe.columns else None

    ecl_dt = pd.to_datetime(
        fe["earliest_cr_line"].astype(str).str.strip(),
        format=FMT,
        errors="coerce"
    ) if "earliest_cr_line" in fe.columns else None

    if issue_dt is not None:
        fe["issue_year"] = issue_dt.dt.year.astype("float32")
        fe["issue_month"] = issue_dt.dt.month.astype("float32")

    if ecl_dt is not None:
        fe["earliest_cr_line_year"] = ecl_dt.dt.year.astype("float32")
        fe["earliest_cr_line_month"] = ecl_dt.dt.month.astype("float32")

    # Credit history age in months
    if issue_dt is not None and ecl_dt is not None:
        mask = issue_dt.notna() & ecl_dt.notna()
        fe["credit_history_age_months"] = np.nan

        months_diff = (
            (issue_dt.dt.year[mask] - ecl_dt.dt.year[mask]) * 12
            + (issue_dt.dt.month[mask] - ecl_dt.dt.month[mask])
        ).astype("float32")

        fe.loc[mask, "credit_history_age_months"] = months_diff
        fe.loc[fe["credit_history_age_months"] < 0, "credit_history_age_months"] = np.nan

    # Numeric safe
    for col in ["loan_amnt", "annual_inc", "total_pymnt", "total_rec_prncp", "recoveries", "dti"]:
        if col in fe.columns:
            fe[col] = pd.to_numeric(fe[col], errors="coerce")

    # revol_util is often like "45.3%"
    if "revol_util" in fe.columns:
        fe["revol_util"] = (
            fe["revol_util"].astype(str).str.replace("%", "", regex=False)
        )
        fe["revol_util"] = pd.to_numeric(fe["revol_util"], errors="coerce")

    if "total_pymnt" in fe.columns and "loan_amnt" in fe.columns:
        fe["payment_to_loan_ratio"] = fe["total_pymnt"] / fe["loan_amnt"]

    if "annual_inc" in fe.columns and "loan_amnt" in fe.columns:
        fe["income_to_loan_ratio"] = fe["annual_inc"] / fe["loan_amnt"]

    final_cols = [c for c in (BASE_COLS + ENGINEERED_COLS) if c in fe.columns]
    return fe.loc[:, final_cols]


def run_feature_engineering() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            f"Check your docker volume mounts ./data -> /opt/airflow/data"
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Deterministic output
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    total_in = 0
    total_out = 0
    first = True

    # Read only needed columns if they exist (prevents KeyError)
    try:
        reader = pd.read_csv(
            INPUT_FILE,
            chunksize=CHUNK_SIZE,
            low_memory=False,
            usecols=lambda c: c in set(BASE_COLS)  # keep only base cols
        )
    except Exception:
        reader = pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False)

    for i, chunk in enumerate(reader, start=1):
        total_in += len(chunk)

        out = transform_chunk(chunk)
        total_out += len(out)

        out.to_csv(
            OUTPUT_FILE,
            index=False,
            mode="w" if first else "a",
            header=first,
            lineterminator="\n"
        )
        first = False

        print(f"[chunk {i}] in={len(chunk)} out={len(out)} total_in={total_in} total_out={total_out}")

    print("Feature engineering completed.")
    print(f"Input:  {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE} (rows={total_out})")


if __name__ == "__main__":
    run_feature_engineering()
