from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db import get_db

router = APIRouter(prefix="/kpi", tags=["KPIs"])


@router.get("/default_rate")
def get_default_rate(db: Session = Depends(get_db)):
    """
    Default Rate = average of loan_status_binary (1=default, 0=non-default)
    """
    try:
        query = text("""
            SELECT
                CASE
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE AVG(loan_status_binary::float)
                END AS default_rate
            FROM analytics.loan_portfolio_features;
        """)
        result = db.execute(query).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (default_rate): {e}")

    val = 0.0 if (result is None or result[0] is None) else float(result[0])
    return {"default_rate": round(val, 4)}


@router.get("/average_loan_amount")
def avg_loan_amount(db: Session = Depends(get_db)):
    """
    Average original loan amount (loan_amnt)
    """
    try:
        query = text("""
            SELECT AVG(loan_amnt) AS avg_loan_amount
            FROM analytics.loan_portfolio_features;
        """)
        result = db.execute(query).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (average_loan_amount): {e}")

    val = 0.0 if (result is None or result[0] is None) else float(result[0])
    return {"average_loan_amount": round(val, 2)}


@router.get("/average_interest_rate")
def avg_interest_rate(db: Session = Depends(get_db)):
    """
    Average interest rate across the portfolio.
    """
    try:
        query = text("""
            SELECT AVG(int_rate) AS avg_int_rate
            FROM analytics.loan_portfolio_features;
        """)
        result = db.execute(query).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (average_interest_rate): {e}")

    val = 0.0 if (result is None or result[0] is None) else float(result[0])
    return {"average_interest_rate": round(val, 4)}


@router.get("/portfolio_growth")
def portfolio_growth(db: Session = Depends(get_db)):
    """
    Portfolio growth by origination year.
    """
    try:
        query = text("""
            WITH yearly AS (
                SELECT
                    COALESCE(issue_d_year, DATE_PART('year', issue_d)::int) AS issue_year,
                    SUM(loan_amnt) AS total_loan_amount
                FROM analytics.loan_portfolio_features
                WHERE COALESCE(issue_d_year, DATE_PART('year', issue_d)::int) IS NOT NULL
                GROUP BY 1
            )
            SELECT
                issue_year,
                total_loan_amount,
                LAG(total_loan_amount) OVER (ORDER BY issue_year) AS prev_total,
                CASE
                    WHEN LAG(total_loan_amount) OVER (ORDER BY issue_year) IS NULL THEN NULL
                    WHEN LAG(total_loan_amount) OVER (ORDER BY issue_year) = 0 THEN NULL
                    ELSE (total_loan_amount - LAG(total_loan_amount) OVER (ORDER BY issue_year))
                         / LAG(total_loan_amount) OVER (ORDER BY issue_year)
                END AS growth_rate
            FROM yearly
            ORDER BY issue_year;
        """)
        rows = db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (portfolio_growth): {e}")

    out = []
    for r in rows:
        out.append(
            {
                "year": int(r.issue_year),
                "total_loan_amount": float(r.total_loan_amount),
                "previous_total_loan_amount": float(r.prev_total) if r.prev_total is not None else None,
                "growth_rate": float(r.growth_rate) if r.growth_rate is not None else None,
            }
        )

    return {"portfolio_growth": out}


@router.get("/loan_distribution_by_grade")
def loan_distribution_by_grade(db: Session = Depends(get_db)):
    """
    Loan distribution by grade (A-G), derived from sub_grade (e.g., 'B3' -> 'B').
    Returns count and share per grade.
    """
    try:
        query = text("""
            SELECT
                LEFT(sub_grade, 1) AS grade,
                COUNT(*) AS loan_count,
                COUNT(*)::float / SUM(COUNT(*)) OVER () AS share
            FROM analytics.loan_portfolio_features
            WHERE sub_grade IS NOT NULL AND sub_grade <> ''
            GROUP BY LEFT(sub_grade, 1)
            ORDER BY LEFT(sub_grade, 1);
        """)
        rows = db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (loan_distribution_by_grade): {e}")

    result = []
    for row in rows:
        result.append(
            {
                "grade": row.grade,
                "loan_count": int(row.loan_count),
                "share": round(float(row.share), 4),
            }
        )

    return {"loan_distribution_by_grade": result}
