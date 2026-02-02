from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
        "owner": "eri",
        "retries": 1,
}

with DAG(
    dag_id="loan_portfolio_pipeline",
    default_args=default_args,
    description="End-to-end pipeline: raw -> FE -> staging -> analytics -> tests",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["thesis", "lendingclub", "kpi"],
) as dag:
        common_env = {
            "PYTHONPATH": "/opt/airflow/project",
            "AIRFLOW_CONN_THESIS_POSTGRES": (
                "postgresql://postgres:postgres@thesis-postgres:5432/loan_portfolio_db"
            ),
        }

        raw_ingestion = BashOperator(
            task_id="raw_ingestion",
            bash_command="python -m src.ingestion.load_raw_data",
            env=common_env,
        )

        feature_engineering = BashOperator(
            task_id="feature_engineering",
            bash_command="python /opt/airflow/project/src/transformations/feature_engineering.py",
            env=common_env,
        )

        make_typed_kpi_csv = BashOperator(
            task_id="make_typed_kpi_csv",
            bash_command="python /opt/airflow/project/src/transformations/make_typed_kpi_csv.py",
            env=common_env,
        )

        load_staging = BashOperator(
            task_id="load_to_staging",
            bash_command="python -m src.transformations.load_staging_data",
            env=common_env,
        )

        promote_analytics = BashOperator(
            task_id="promote_to_analytics",
            bash_command="python -m src.transformations.load_analytics_data",
            env=common_env,
        )

        run_tests = BashOperator(
        task_id="run_tests",
        bash_command="python -m pytest -q /opt/airflow/dags/tests",
        env={
            "PYTHONPATH": "/opt/airflow/project:/opt/airflow/dags",
            "AIRFLOW_HOME": "/opt/airflow",
            "AIRFLOW_CONN_THESIS_POSTGRES": (
                "postgresql://postgres:postgres@thesis-postgres:5432/loan_portfolio_db"
            ),
        },
    )

        (
            raw_ingestion
            >> feature_engineering
            >> make_typed_kpi_csv
            >> load_staging
            >> promote_analytics
            >> run_tests
        )
