# MSc Thesis – End-to-End Data Engineering Pipeline for Loan Portfolio Monitoring and KPI Calculation with API Exposure

## Overview
This repository contains the implementation of my MSc Thesis project at the National and Kapodistrian University of Athens (NKUA).  
The project focuses on designing and implementing an **end-to-end Data Engineering pipeline** for monitoring loan portfolios and calculating KPIs.  
The pipeline is demonstrated with API exposure using **FastAPI**.

## Dataset
- **Source**: Lending Club dataset (2007–2015)  
- ~890,000 loans, 75 variables  
- Includes borrower info, loan amount, interest rate, loan status, grade/sub-grade.

## Objectives
- Ingest raw loan data (CSV format).
- Store data in **PostgreSQL** with raw / staging / KPI schemas.
- Apply transformations (cleaning, flags, derived fields).
- Calculate 5 main KPIs for loan portfolio monitoring:
  1. **Default Rate KPI**
  2. **Average Loan Amount KPI**
  3. **Average Interest Rate KPI**
  4. **Portfolio Growth KPI**
  5. **Loan Distribution by Grade KPI**
- Expose KPIs through **FastAPI endpoints**.

## Tech Stack
- **Python** (pandas, sqlalchemy, fastapi)
- **PostgreSQL**
- **VS Code** for development
- **DataGrip** for SQL database management
- **Uvicorn** (server for FastAPI)

## Repository Structure (planned)

MasterThesis_DataEngineering_EleftheriaPardali/
│
├── data/                # Raw dataset (CSV files, Lending Club data)
│
├── sql/                 # SQL scripts (schemas, transformations, KPIs)
│
├── src/                 # Python source code
│   ├── ingestion/       # Data loading scripts
│   ├── transformations/ # Cleaning, derived fields
│   └── api/             # FastAPI app
│
├── README.md            # Project description
└── requirements.txt     # Dependencies

