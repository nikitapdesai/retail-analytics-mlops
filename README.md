
# Retail Analytics Platform

An end-to-end retail analytics and data engineering project built using the UCI Online Retail dataset. The platform processes transactional retail data, validates and cleans records, loads a PostgreSQL data warehouse, orchestrates ETL tasks with Apache Airflow, and presents business insights through a Streamlit dashboard.

## Project Overview

The project demonstrates a retail data engineering workflow, from raw data ingestion to analytics-ready warehouse tables and dashboard visualizations.

### Key Features

- **Data ingestion:** Reads the original Online Retail Excel dataset and records ingestion status.
- **Data staging:** Stores the raw transactional data in a staging layer.
- **Data validation:** Identifies cancelled invoices, invalid quantities, invalid prices, and missing customer identifiers.
- **Data transformation:** Cleans records, converts data types, calculates revenue, and removes duplicates.
- **Data warehousing:** Loads date, customer, product, and geography dimensions, along with the sales fact table, into PostgreSQL.
- **ETL orchestration:** Uses Apache Airflow to coordinate pipeline tasks and track their execution.
- **Business intelligence:** Uses Streamlit to display sales trends, top products, geographical sales, and customer retention metrics.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Data processing | Pandas |
| Source dataset | UCI Online Retail |
| Data warehouse | PostgreSQL |
| Workflow orchestration | Apache Airflow |
| Containerization | Docker and Docker Compose |
| Dashboard | Streamlit |
| Database connectivity | psycopg2 |
| Configuration management | python-dotenv |

## Data Processing Results

| Metric | Result |
|---|---:|
| Raw records | 541,909 |
| Rejected records | 144,025 |
| Valid records after validation | 397,884 |
| Duplicate records removed during cleaning | 5,192 |
| Cleaned records | 392,692 |