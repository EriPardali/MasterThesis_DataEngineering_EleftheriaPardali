# src/api/main.py

from fastapi import FastAPI
from .routes import kpi

app = FastAPI(
    title="Loan Portfolio API",
    description="API exposing KPIs for the loan portfolio (Master Thesis)",
    version="1.0.0"
)

# Include the KPI router
app.include_router(kpi.router)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Loan Portfolio API is running!"}
