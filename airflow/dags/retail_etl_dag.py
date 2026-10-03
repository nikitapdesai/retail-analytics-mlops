import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import psycopg2
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

PROJECT_ROOT = Path("/opt/retail")
SRC = PROJECT_ROOT / "src"


def run_script(script_path):
    """Execute an existing project script and stop if it fails."""
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT),
        check=True,
    )


def ingest_data():
    """Run ingestion and explicitly check its status log."""
    run_script(SRC / "ingestion" / "ingest.py")

    log_file = PROJECT_ROOT / "data" / "raw" / "ingestion_log.json"
    with open(log_file, "r", encoding="utf-8") as file:
        log = json.load(file)

    if log.get("status") != "SUCCESS":
        raise RuntimeError(
            f"Ingestion failed. Check the ingestion log: {log.get('error')}"
        )


def stage_data():
    run_script(SRC / "ingestion" / "stage_data.py")


def validate_data():
    run_script(SRC / "validation" / "validate_data.py")


def clean_data():
    run_script(SRC / "transformation" / "clean_data.py")


def load_dimensions():
    run_script(SRC / "database" / "load_dimensions.py")


def load_fact_sales_safely():
    """Prevent accidental duplicate insertion into the existing fact table."""
    cleaned_file = PROJECT_ROOT / "data" / "processed" / "cleaned_retail.csv"
    expected_rows = len(pd.read_csv(cleaned_file))

    conn = psycopg2.connect(
        host="host.docker.internal",
        port=int(__import__("os").environ["DB_PORT"]),
        dbname=__import__("os").environ["DB_NAME"],
        user=__import__("os").environ["DB_USER"],
        password=__import__("os").environ["DB_PASSWORD"],
        connect_timeout=10,
    )

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM fact_sales;")
            existing_rows = cur.fetchone()[0]
    finally:
        conn.close()

    if existing_rows == expected_rows:
        print(
            f"Skipping fact load: fact_sales already contains "
            f"{existing_rows} rows, matching the cleaned dataset."
        )
        return

    if existing_rows != 0:
        raise RuntimeError(
            f"Safety check stopped the load: fact_sales contains "
            f"{existing_rows} rows, but the cleaned dataset contains "
            f"{expected_rows}. No new fact records were inserted."
        )

    run_script(SRC / "database" / "load_fact_sales.py")

    conn = psycopg2.connect(
        host="host.docker.internal",
        port=int(__import__("os").environ["DB_PORT"]),
        dbname=__import__("os").environ["DB_NAME"],
        user=__import__("os").environ["DB_USER"],
        password=__import__("os").environ["DB_PASSWORD"],
        connect_timeout=10,
    )

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM fact_sales;")
            actual_rows = cur.fetchone()[0]
    finally:
        conn.close()

    if actual_rows != expected_rows:
        raise RuntimeError(
            f"Fact row count mismatch: expected {expected_rows}, "
            f"found {actual_rows}. Investigate before retrying."
        )

    print(f"Fact load verified: {actual_rows} rows.")


with DAG(
    dag_id="retail_analytics_etl",
    description="Retail data ingestion, validation, cleaning, and warehouse loading",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 0},
    tags=["retail", "etl", "data-engineering"],
) as dag:

    ingestion_task = PythonOperator(
        task_id="ingest_raw_data",
        python_callable=ingest_data,
    )

    staging_task = PythonOperator(
        task_id="stage_raw_data",
        python_callable=stage_data,
    )

    validation_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data,
    )

    cleaning_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
    )

    dimensions_task = PythonOperator(
        task_id="load_dimensions",
        python_callable=load_dimensions,
    )

    fact_task = PythonOperator(
        task_id="load_fact_sales_safely",
        python_callable=load_fact_sales_safely,
    )

    (
        ingestion_task
        >> staging_task
        >> validation_task
        >> cleaning_task
        >> dimensions_task
        >> fact_task
    )
