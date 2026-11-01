"""Optional scheduled Airflow orchestration; uses same tasks as the CLI pipeline."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ecommerce_etl_demo",
    description="Generate synthetic data, upsert to Postgres, validate and build dbt marts",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["portfolio", "etl", "dbt"],
) as dag:
    generate = BashOperator(task_id="generate_source", bash_command="cd /app && python -m src.generate_data")
    ingest = BashOperator(task_id="ingest_postgres", bash_command="cd /app && python -m src.load")
    quality = BashOperator(task_id="validate_raw", bash_command="cd /app && python -m src.checks")
    build = BashOperator(task_id="dbt_build", bash_command="cd /app && dbt build --project-dir dbt --profiles-dir dbt")
    generate >> ingest >> quality >> build
