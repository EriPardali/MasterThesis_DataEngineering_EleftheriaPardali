# MSc Thesis – End-to-End Data Engineering Pipeline for Loan Portfolio Monitoring and KPI Calculation with API Exposure

## Overview
This repository contains the implementation of my MSc Thesis project at the **National and Kapodistrian University of Athens (NKUA)**.

The project focuses on the design and implementation of an **end-to-end Data Engineering pipeline** for loan portfolio monitoring.  
It covers the full lifecycle of data handling, from **raw data ingestion** to **KPI computation and API-based exposure**, following production-oriented data engineering practices.

The pipeline integrates:
- relational data storage,
- transformation and feature engineering logic,
- workflow orchestration using **Apache Airflow**,
- and a REST API layer implemented with **FastAPI** for KPI access.

---

## Dataset
- **Source**: Lending Club loan dataset (2007–2015)
- ~890,000 loan records, ~75 variables
- Includes borrower characteristics, loan attributes, interest rates, loan status, and credit grades

The dataset is ingested in raw form and progressively transformed into structured analytical tables suitable for portfolio-level KPI computation.

---

## Objectives
The main objectives of the project are:

- Design a **modular data engineering architecture** for loan portfolio analytics
- Ingest raw loan data from CSV files into a relational database
- Organize data into **raw**, **staging**, and **analytics** layers
- Apply data cleaning, transformation, and feature engineering logic
- Compute core **loan portfolio monitoring KPIs**, including:
  1. **Default Rate**
  2. **Average Loan Amount**
  3. **Average Interest Rate**
  4. **Portfolio Growth**
  5. **Loan Distribution by Grade**
- Orchestrate data processing workflows using **Apache Airflow**
- Expose computed KPIs through **FastAPI REST endpoints**

---

## Tech Stack
- **Python** (pandas, SQLAlchemy, FastAPI)
- **PostgreSQL** (relational data storage)
- **Apache Airflow** (workflow orchestration)
- **Docker & Docker Compose** (containerized environment)
- **VS Code** (development environment)
- **DataGrip** (database exploration and SQL development)
- **Uvicorn** (FastAPI application server)

---

## Repository Structure
The repository is organized to reflect the main components of a production-style data engineering pipeline, with a clear separation between orchestration, data processing, schema management, API exposure, and documentation.

### Directory layout
```text
MasterThesis_DataEngineering_EleftheriaPardali/
│
├── airflow/
│   ├── dags/
│   │   ├── loan_pipeline_dag.py
│   │   └── tests/
│   ├── logs/                
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
