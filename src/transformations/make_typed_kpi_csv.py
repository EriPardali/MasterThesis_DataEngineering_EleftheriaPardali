import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/loan_kpi_staging.csv")
OUT_PATH = Path("data/processed/loan_kpi_staging_typed.csv")

def parse_month_year(s: pd.Series) -> pd.Series:
    # "Dec-2015" -> 2015-12-01 (DATE)
    dt = pd.to_datetime(s.astype(str).str.strip(), format="%b-%Y", errors="coerce")
    return dt.dt.to_period("M").dt.to_timestamp()

def main():
    df = pd.read_csv(IN_PATH)

    # --- Dates ---     
    if "issue_d" in df.columns:
        df["issue_d"] = parse_month_year(df["issue_d"])
    if "last_pymnt_d" in df.columns:
        df["last_pymnt_d"] = parse_month_year(df["last_pymnt_d"])

    # --- Integer-like fields (nullable ints) ---
    int_cols_small = ["issue_d_year", "issue_d_month", "emp_length_years", "grade_ord", "sub_grade_ord", "loan_status_binary"]
    int_cols = ["credit_history_age_months"]
    int_cols_big = ["revol_bal"]

    for c in int_cols_small:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    for c in int_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    for c in int_cols_big:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    # --- Numeric fields ---
    num_cols = [
        "loan_amnt","int_rate","installment","annual_inc","dti","revol_util",
        "total_pymnt","total_rec_int","recoveries","last_pymnt_amnt",
        "payment_to_loan_ratio","income_to_loan_ratio"
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Text fields ---
    if "addr_state" in df.columns:
        df["addr_state"] = df["addr_state"].astype("string")
    if "sub_grade" in df.columns:
        df["sub_grade"] = df["sub_grade"].astype("string")

    df.to_csv(OUT_PATH, index=False)
    print(f"Saved typed CSV to: {OUT_PATH} | shape={df.shape}")

if __name__ == "__main__":
    main()
