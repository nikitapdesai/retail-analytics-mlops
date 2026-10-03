\# Retail Analytics Platform



An end-to-end retail analytics and data engineering project built using the UCI Online Retail dataset. The platform processes transactional retail data, validates and cleans records, loads a PostgreSQL data warehouse, orchestrates ETL tasks with Apache Airflow, and presents business insights through a Streamlit dashboard.



\## Project Overview



The project demonstrates a retail data engineering workflow, from raw data ingestion to analytics-ready warehouse tables and dashboard visualizations.



\### Key Features



\* \*\*Data ingestion:\*\* Reads the original Online Retail Excel dataset and records ingestion status.

\* \*\*Data staging:\*\* Stores the raw transactional data in a staging layer.

\* \*\*Data validation:\*\* Identifies cancelled invoices, invalid quantities, invalid prices, and missing customer identifiers.

\* \*\*Data transformation:\*\* Cleans records, converts data types, calculates revenue, and removes duplicates.

\* \*\*Data warehousing:\*\* Loads date, customer, product, and geography dimensions, along with the sales fact table, into PostgreSQL.

\* \*\*ETL orchestration:\*\* Uses Apache Airflow to coordinate the pipeline tasks and track their execution.

\* \*\*Business intelligence:\*\* Uses Streamlit to display sales trends, top products, customer segmentation, geographical sales, and customer retention metrics.



\## Architecture



```text

UCI Online Retail Dataset

&#x20;         |

&#x20;         v

&#x20;   Data Ingestion

&#x20;         |

&#x20;         v

&#x20;    Data Staging

&#x20;         |

&#x20;         v

&#x20;   Data Validation

&#x20;     /         \\

&#x20;    v           v

&#x20;Valid Records  Rejected Records

&#x20;    |

&#x20;    v

&#x20;Data Cleaning and Transformation

&#x20;    |

&#x20;    v

&#x20;PostgreSQL Data Warehouse

&#x20;    |

&#x20;    v

&#x20;Sales and Customer Analytics Marts

&#x20;    |

&#x20;    v

&#x20;Streamlit Dashboard



Apache Airflow orchestrates the ETL tasks.

```



\## Technology Stack



| Component                | Technology                |

| ------------------------ | ------------------------- |

| Programming language     | Python                    |

| Data processing          | Pandas                    |

| Source dataset           | UCI Online Retail         |

| Data warehouse           | PostgreSQL                |

| Workflow orchestration   | Apache Airflow            |

| Containerization         | Docker and Docker Compose |

| Dashboard                | Streamlit                 |

| Database connectivity    | psycopg2                  |

| Configuration management | python-dotenv             |



\## Dataset



The project uses the UCI Online Retail dataset, containing retail transactions with fields such as invoice number, stock code, product description, quantity, invoice date, unit price, customer ID, and country.



The dataset is used to analyze revenue, order activity, product performance, customer purchasing patterns, and geographical sales.



\## Data Processing Results



| Metric                                    |  Result |

| ----------------------------------------- | ------: |

| Raw records                               | 541,909 |

| Rejected records                          | 144,025 |

| Valid records after validation            | 397,884 |

| Duplicate records removed during cleaning |   5,192 |

| Cleaned records                           | 392,692 |



Rejected records are stored separately to support data quality inspection. The cleaned dataset is used for downstream warehouse loading.



\## Data Warehouse



The PostgreSQL warehouse contains dimension tables, a sales fact table, and analytics marts.



| Table           | Purpose                                         |

| --------------- | ----------------------------------------------- |

| `dim\_date`      | Date attributes for time-based analysis         |

| `dim\_customer`  | Customer information                            |

| `dim\_product`   | Product information                             |

| `dim\_geography` | Country-level geographical information          |

| `fact\_sales`    | Transaction-level sales records                 |

| `sales\_mart`    | Sales analytics for dashboard reporting         |

| `customer\_mart` | Customer-level analytics and retention analysis |



\## ETL Workflow with Apache Airflow



The Airflow DAG, `retail\_analytics\_etl`, organizes the following tasks:



1\. `ingest\_raw\_data` — ingests the source dataset and checks ingestion status.

2\. `stage\_raw\_data` — prepares the staging dataset.

3\. `validate\_data` — separates valid and rejected records.

4\. `clean\_data` — transforms and cleans valid data.

5\. `load\_dimensions` — loads the warehouse dimension tables.

6\. `load\_fact\_sales\_safely` — checks the existing fact-table row count before deciding whether to load the fact data.



The fact-loading task includes a row-count safety check to avoid reloading data when the existing fact-table count matches the cleaned dataset count.



\## Dashboard and Analytics



The Streamlit dashboard provides a visual summary of retail performance, including:



\* Revenue and order KPIs

\* Monthly revenue trends

\* Monthly revenue and order comparisons

\* Top 10 products by revenue

\* Customer retention and repeat-purchase analysis



Screenshots of the dashboard and Airflow execution are available in \[`docs/screenshots/`](docs/screenshots/).



\## Project Structure



```text

retail-analytics-platform/

├── airflow/

│   ├── dags/

│   │   └── retail\_etl\_dag.py

│   ├── Dockerfile

│   └── docker-compose.yaml

├── dashboard/

│   └── app.py

├── data/

│   ├── raw/

│   ├── staging/

│   ├── processed/

│   └── rejected/

├── docs/

│   └── screenshots/

├── src/

│   ├── ingestion/

│   ├── validation/

│   ├── transformation/

│   └── database/

├── requirements.txt

├── .gitignore

└── README.md

```



\## Setup and Execution



\### Prerequisites



\* Python 3.11

\* PostgreSQL

\* Docker Desktop with Docker Compose

\* Git



\### 1. Clone the repository



```powershell

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd retail-analytics-platform

```



\### 2. Create and activate a virtual environment



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install Python dependencies



```powershell

pip install -r requirements.txt

```



\### 4. Configure the database



Create a local `.env` file in the project root with your PostgreSQL connection settings:



```text

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=retail\_dw

DB\_USER=your\_postgres\_username

DB\_PASSWORD=your\_postgres\_password

```



Use your own local credentials. Do not commit `.env` files or expose passwords in the repository.



Ensure that the PostgreSQL database and the required warehouse tables exist before running database-loading scripts.



\### 5. Run the Streamlit dashboard



From the project root:



```powershell

streamlit run dashboard\\app.py

```



\### 6. Start Apache Airflow



From the project root, ensure that the Airflow environment configuration file is available at `airflow/.env`, with the required local settings and database connection variables.



Start the Airflow services:



```powershell

docker compose -f airflow\\docker-compose.yaml up -d --build

```



Open the Airflow web interface at:



`http://localhost:8080`



Log in using the local credentials configured for your Airflow instance, then locate and trigger the `retail\_analytics\_etl` DAG.



To stop the services:



```powershell

docker compose -f airflow\\docker-compose.yaml down

```



\## Screenshots



Project screenshots include dashboard KPIs, monthly revenue trends, product performance, customer retention, and Airflow ETL execution. Refer to `docs/screenshots/` for the available images.



\## Future Enhancements



\* Add automated data quality tests and pipeline failure alerts.

\* Improve incremental and idempotent warehouse loading.

\* Refresh analytics marts automatically after successful warehouse loads.

\* Extend the platform with repeat-purchase or customer churn prediction.

\* Add model tracking, API-based inference, containerized model serving, and monitoring as part of a future MLOps extension.



\## Notes



This repository contains the project code and selected screenshots. Local datasets, database credentials, generated logs, and environment-specific configuration should remain outside version control.



