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

## Repository Structure  

The repository is organized into separate branches and directories to reflect the main stages of the pipeline.  

### Branches and their purpose  
- **main/** → Stable version, project overview  
- **data-ingestion/** → Python scripts for loading the Lending Club dataset  
- **data-cleaning-transformations/** → SQL/Python scripts for data cleaning & transformations  
- **kpi-calculation/** → SQL scripts for KPI derivation  
- **api-exposure/** → FastAPI app for exposing KPIs  

### Directory layout  
```bash
MasterThesis_DataEngineering_EleftheriaPardali/
│
├── airflow/
│   ├── dags/
│   │   ├── loan_pipeline_dag.py
│   │   └── tests/
│   ├── plugins/
│   └── Dockerfile
│
├── data/
│   └── README.md
│
├── docs/
│   ├── 02_Literature_Review/
│   ├── 03_Methodology/
│   └── 04_Results_and_Analysis/
│
├── sql/
│   └── 01_create_schemas.sql
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── routes/
│   │   │   └── kpi.py
│   │   └── Dockerfile
│   │
│   ├── db/
│   │   └── connection.py
│   │
│   ├── ingestion/
│   │   └── load_raw_data.py
│   │
│   ├── schemas/
│   │   └── staging_schema.py
│   │
│   ├── transformations/
│   │   ├── feature_engineering.py
│   │   ├── load_staging_data.py
│   │   ├── load_analytics_data.py
│   │   └── make_typed_kpi_csv.py
│   │
│   └── kpis/
│       └── kpi_loan_portfolio.ipynb
│
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .gitignore
└── .dockerignore
