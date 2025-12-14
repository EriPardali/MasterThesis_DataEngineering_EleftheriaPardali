from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # <-- IMPORTANT
from ..db import get_db

router = APIRouter(prefix="/kpi", tags=["KPIs"])


@router.get("/default_rate")
def get_default_rate(db: Session = Depends(get_db)):
    """
    Default loans = 'Charged Off' OR 'Late (31-120 days)'
    Default Rate = defaults / total loans
    """
    try:
        query = text("""
            SELECT 
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE 
                        SUM(
                            CASE 
                                WHEN loan_status = 'Charged Off'
                                  OR loan_status = 'Late (31-120 days)'
                                THEN 1 ELSE 0 
                            END
                        )::float
                        / COUNT(*)
                END AS default_rate
            FROM analytics.loan_portfolio_features;
        """)
        result = db.execute(query).fetchone()
    except Exception as e:
        # e.g. wrong schema/table name
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result is None or result[0] is None:
        return {"default_rate": 0.0}

    return {"default_rate": round(float(result[0]), 4)}


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
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if result is None or result[0] is None:
        return {"average_loan_amount": 0.0}

    return {"average_loan_amount": float(result[0])}

@router.get("/average_interest_rate")
def avg_interest_rate(db: Session = Depends(get_db)):
    """
    Average interest rate across the portfolio.
    Assumes int_rate is stored as numeric (e.g. 13.49 for 13.49%).
    """
    try:
        query = text("""
            SELECT AVG(int_rate) AS avg_int_rate
            FROM analytics.loan_portfolio_features;
        """)
        result = db.execute(query).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (average_interest_rate): {e}")

    if result is None or result[0] is None:
        return {"average_interest_rate": 0.0}

    return {"average_interest_rate": float(result[0])}


@router.get("/portfolio_growth")
def portfolio_growth(db: Session = Depends(get_db)):
    """
    Portfolio growth by origination year.
    Uses SUM(loan_amnt) per year and computes year-on-year growth rate.
    Assumes issue_d is a DATE/TIMESTAMP column.
    """
    try:
        query = text("""
            SELECT
                issue_year,
                total_loan_amount,
                LAG(total_loan_amount) OVER (ORDER BY issue_year) AS prev_total,
                CASE 
                    WHEN LAG(total_loan_amount) OVER (ORDER BY issue_year) IS NULL 
                        THEN NULL
                    WHEN LAG(total_loan_amount) OVER (ORDER BY issue_year) = 0
                        THEN NULL
                    ELSE 
                        (total_loan_amount - LAG(total_loan_amount) OVER (ORDER BY issue_year))
                        / LAG(total_loan_amount) OVER (ORDER BY issue_year)
                END AS growth_rate
            FROM (
                SELECT 
                    DATE_PART('year', issue_d)::int AS issue_year,
                    SUM(loan_amnt) AS total_loan_amount
                FROM analytics.loan_portfolio_features
                GROUP BY DATE_PART('year', issue_d)::int
            ) t
            ORDER BY issue_year;
        """)
        rows = db.execute(query).fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (portfolio_growth): {e}")

    result = []
    for row in rows:
        year = int(row.issue_year)
        total = float(row.total_loan_amount)
        prev_total = float(row.prev_total) if row.prev_total is not None else None
        growth = float(row.growth_rate) if row.growth_rate is not None else None

        result.append(
            {
                "year": year,
                "total_loan_amount": total,
                "previous_total_loan_amount": prev_total,
                "growth_rate": growth,  # e.g. 0.15 = +15%
            }
        )

    return {"portfolio_growth": result}


@router.get("/loan_distribution_by_grade")
def loan_distribution_by_grade(db: Session = Depends(get_db)):
    """
    Loan distribution by grade (A-G).
    Returns count of loans and share of portfolio per grade.
    """
    try:
        query = text("""
            SELECT 
                grade,
                COUNT(*) AS loan_count,
                COUNT(*)::float / SUM(COUNT(*)) OVER () AS share
            FROM analytics.loan_portfolio_features
            GROUP BY grade
            ORDER BY grade;
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
                "share": float(row.share),  # e.g. 0.23 = 23% of portfolio
            }
        )

    return {"loan_distribution_by_grade": result}