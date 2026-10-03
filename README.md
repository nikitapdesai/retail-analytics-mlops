# \# Retail Analytics Platform

#

# An end-to-end retail analytics and data engineering project built using the UCI Online Retail dataset. The platform processes transactional retail data, validates and cleans records, loads a PostgreSQL data warehouse, orchestrates ETL tasks with Apache Airflow, and presents business insights through a Streamlit dashboard.

#

# \## Project Overview

#

# The project demonstrates a retail data engineering workflow, from raw data ingestion to analytics-ready warehouse tables and dashboard visualizations.

#

# \### Key Features

#

# \- \*\*Data ingestion:\*\* Reads the original Online Retail Excel dataset and records ingestion status.

# \- \*\*Data staging:\*\* Stores the raw transactional data in a staging layer.

# \- \*\*Data validation:\*\* Identifies cancelled invoices, invalid quantities, invalid prices, and missing customer identifiers.

# \- \*\*Data transformation:\*\* Cleans records, converts data types, calculates revenue, and removes duplicates.

# \- \*\*Data warehousing:\*\* Loads date, customer, product, and geography dimensions, along with the sales fact table, into PostgreSQL.

# \- \*\*ETL orchestration:\*\* Uses Apache Airflow to coordinate pipeline tasks and track their execution.

# \- \*\*Business intelligence:\*\* Uses Streamlit to display sales trends, top products, geographical sales, and customer retention metrics.

#

# \## Technology Stack

#

# | \*\*Component\*\*            | \*\*Technology\*\*            |

# | ------------------------ | ------------------------- |

# | Programming language     | Python                    |

# | Data processing          | Pandas                    |

# | Source dataset           | UCI Online Retail         |

# | Data warehouse           | PostgreSQL                |

# | Workflow orchestration   | Apache Airflow            |

# | Containerization         | Docker and Docker Compose |

# | Dashboard                | Streamlit                 |

# | Database connectivity    | psycopg2                  |

# | Configuration management | python-dotenv             |

#

# \## Data Processing Results

#

# | \*\*Metric\*\*                                | \*\*Result\*\* |

# | ----------------------------------------- | ---------- |

# | Raw records                               | 541,909    |

# | Rejected records                          | 144,025    |

# | Valid records after validation            | 397,884    |

# | Duplicate records removed during cleaning | 5,192     |

# | Cleaned records                           | 392,692   |

#

# The pipeline separates invalid records from valid transactions and prepares the cleaned data for analytical processing. The transformation stage calculates revenue and removes duplicate records before loading the data into the warehouse.

#

# \## Project Structure

#

# ```text

# retail-analytics-platform/

# ├── airflow/

# │   ├── dags/

# │   │   └── retail\_etl\_dag.py

# │   ├── logs/

# │   ├── config/

# │   ├── plugins/

# │   ├── Dockerfile

# │   └── docker-compose.yaml

# ├── dashboard/

# │   └── app.py

# ├── data/

# │   ├── raw/

# │   │   ├── Online Retail.xlsx

# │   │   └── ingestion\_log.json

# │   ├── staging/

# │   ├── processed/

# │   └── rejected/

# ├── docs/

# │   └── screenshots/

# ├── src/

# │   ├── ingestion/

# │   │   ├── ingest.py

# │   │   └── stage\_data.py

# │   ├── validation/

# │   │   └── validate\_data.py

# │   ├── transformation/

# │   │   └── clean\_data.py

# │   └── database/

# │       ├── load\_dimensions.py

# │       └── load\_fact\_sales.py

# ├── sql/

# ├── .gitignore

# ├── .env

# ├── requirements.txt

# └── README.md

# ```

#

# \*\*Note:\*\* Local environment files, generated Airflow configuration, and logs are excluded from version control. The `.env` file must be created locally and should not be committed to Git.

#

# \## Dataset

#

# The project uses the \*\*UCI Online Retail dataset\*\*, which contains transactional records from a UK-based online retail business.

#

# The original dataset includes the following fields:

#

# \- `InvoiceNo`: Invoice or transaction identifier.

# \- `StockCode`: Product identifier.

# \- `Description`: Product description.

# \- `Quantity`: Number of items purchased.

# \- `InvoiceDate`: Date and time of the transaction.

# \- `UnitPrice`: Price per unit.

# \- `CustomerID`: Customer identifier.

# \- `Country`: Customer's country.

#

# The dataset contains 541,909 raw records and is used to demonstrate data ingestion, validation, transformation, warehousing, and analytics.

#

# \## Data Engineering Workflow

#

# The pipeline is organized into the following stages.

#

# \### 1. Data Ingestion

#

# The ingestion module reads the source Excel dataset and records the ingestion status in a JSON log file. This provides a record of whether the source data was successfully read.

#

# \*\*Script:\*\* `src/ingestion/ingest.py`

#

# \### 2. Data Staging

#

# The raw dataset is copied into a staging CSV file, providing an intermediate layer between source ingestion and data validation.

#

# \*\*Script:\*\* `src/ingestion/stage\_data.py`

#

# \### 3. Data Validation

#

# The validation module identifies records that do not satisfy the project's data quality rules, including:

#

# \- Cancelled invoices.

# \- Non-positive quantities.

# \- Non-positive unit prices.

# \- Missing customer identifiers.

#

# Rejected records are saved with a rejection reason, while valid records are passed to the transformation stage.

#

# \*\*Script:\*\* `src/validation/validate\_data.py`

#

# \### 4. Data Transformation

#

# The transformation module cleans valid transactions, converts fields into appropriate data types, calculates revenue, and removes duplicate records.

#

# Revenue is calculated as:

#

# `Revenue = Quantity × UnitPrice`

#

# The cleaned dataset is saved as a CSV file for warehouse loading.

#

# \*\*Script:\*\* `src/transformation/clean\_data.py`

#

# \### 5. Data Warehousing

#

# PostgreSQL is used as the data warehouse. The data is organized into dimension tables and a sales fact table to support analytical queries.

#

# \*\*Dimension loading script:\*\* `src/database/load\_dimensions.py`

#

# \*\*Fact loading script:\*\* `src/database/load\_fact\_sales.py`

#

# \### 6. ETL Orchestration

#

# Apache Airflow coordinates the pipeline stages through a Directed Acyclic Graph (DAG). Each task represents a stage of the ETL workflow, allowing execution status and task logs to be monitored through the Airflow interface.

#

# \*\*DAG file:\*\* `airflow/dags/retail\_etl\_dag.py`

#

# \## Data Warehouse Design

#

# The PostgreSQL warehouse contains dimension tables, a fact table, and analytical mart tables.

#

# \### Dimension Tables

#

# | \*\*Table\*\*       | \*\*Purpose\*\* |

# | --------------- | ----------- |

# | `dim\_date`      | Stores date-related attributes for time-based analysis. |

# | `dim\_customer`  | Stores customer-related attributes. |

# | `dim\_product`   | Stores product identifiers and descriptions. |

# | `dim\_geography` | Stores geographical information, including country. |

#

# \### Fact Table

#

# The `fact\_sales` table stores transactional sales information and connects to the dimension tables through keys.

#

# Important fields include:

#

# \- `sales\_key`

# \- `invoice\_no`

# \- `date\_key`

# \- `customer\_key`

# \- `product\_key`

# \- `geography\_key`

# \- `quantity`

# \- `unit\_price`

# \- `revenue`

#

# \### Analytical Mart Tables

#

# | \*\*Table\*\*       | \*\*Purpose\*\* |

# | --------------- | ----------- |

# | `sales\_mart`    | Supports sales and revenue analysis. |

# | `customer\_mart` | Supports customer-level and retention analysis. |

#

# \### Warehouse Record Counts

#

# The following counts were observed after the ETL pipeline execution.

#

# | \*\*Table\*\*       | \*\*Records\*\* |

# | --------------- | ----------: |

# | `dim\_date`      | 305         |

# | `dim\_customer`  | 4,338       |

# | `dim\_product`   | 3,665       |

# | `dim\_geography` | 37          |

# | `fact\_sales`    | 392,692     |

# | `sales\_mart`    | 392,692     |

# | `customer\_mart` | 4,338       |

#

# The sales and customer marts were present in the warehouse during validation. The current Airflow DAG runs the ingestion, staging, validation, cleaning, dimension-loading, and fact-table safety-check tasks; it does not independently rebuild the analytical mart tables.

#

# \## Airflow ETL Pipeline

#

# The project uses Apache Airflow with Docker Compose to orchestrate the ETL workflow.

#

# \### DAG Task Sequence

#

# ```text

# ingest\_raw\_data

# &#x20;      |

# &#x20;      v

# stage\_raw\_data

# &#x20;      |

# &#x20;      v

# validate\_data

# &#x20;      |

# &#x20;      v

# clean\_data

# &#x20;      |

# &#x20;      v

# load\_dimensions

# &#x20;      |

# &#x20;      v

# load\_fact\_sales\_safely

# ```

#

# The DAG contains six tasks:

#

# 1\. `ingest\_raw\_data` — reads the original dataset and checks the ingestion status.

# 2\. `stage\_raw\_data` — creates the staging dataset.

# 3\. `validate\_data` — identifies rejected records and validates the remaining data.

# 4\. `clean\_data` — transforms valid records and produces the cleaned dataset.

# 5\. `load\_dimensions` — loads dimension tables into PostgreSQL.

# 6\. `load\_fact\_sales\_safely` — checks the expected and existing fact-table row counts before deciding whether to skip or perform the fact load.

#

# The fact-loading safety check helps prevent a duplicate load when the existing fact-table row count matches the cleaned dataset. It is a basic safeguard and does not verify that every existing record is identical to the cleaned data.

#

# \### Running Airflow

#

# Make sure Docker Desktop is installed and running before starting Airflow.

#

# From the project root, start the services:

#

# ```powershell

# docker compose -f airflow/docker-compose.yaml up -d --build

# ```

#

# Check the service status:

#

# ```powershell

# docker compose -f airflow/docker-compose.yaml ps

# ```

#

# Open the Airflow interface in a browser:

#

# ```text

# http://localhost:8080

# ```

#

# Log in using the Airflow credentials configured for the local environment. The default credentials in a standard local development setup may be `airflow` / `airflow` unless they have been changed.

#

# The DAG is named `retail\_analytics\_etl`. Trigger it from the Airflow interface and monitor the status of each task.

#

# To stop the services:

#

# ```powershell

# docker compose -f airflow/docker-compose.yaml down

# ```

#

# \*\*Environment note:\*\* The Compose configuration expects Airflow environment settings in `airflow/.env`. Database connection settings must be configured locally, and the database host must be reachable from the containers. On Docker Desktop for Windows, `host.docker.internal` can be used to connect to a PostgreSQL instance running on the host machine.

#

# \## Streamlit Dashboard

#

# The Streamlit dashboard presents business insights derived from the warehouse data and analytical marts.

#

# \### Dashboard Metrics

#

# The following values were observed in the dashboard during project validation.

#

# | \*\*Metric\*\*          | \*\*Value\*\*       |

# | ------------------- | --------------: |

# | Total Revenue       | £8,887,208.89   |

# | Total Orders        | 18,532          |

# | Customers           | 4,338           |

# | Transactions        | 392,692         |

# | Repeat Customer Rate | 65.6%           |

#

# \### Dashboard Views

#

# The dashboard includes the following analytical views:

#

# \- \*\*Key performance indicators:\*\* Overview of total revenue, orders, customers, transactions, and repeat customer rate.

# \- \*\*Monthly revenue trends:\*\* Tracks revenue over time to identify sales patterns.

# \- \*\*Monthly revenue and orders:\*\* Compares sales value and order activity across months.

# \- \*\*Top 10 products by revenue:\*\* Identifies products contributing the most revenue.

# \- \*\*Customer retention:\*\* Presents customer-level repeat-purchase and retention information.

# \- \*\*Geographical sales:\*\* Supports analysis of sales across countries.

#

# \### Running the Dashboard

#

# Activate the project's Python virtual environment and install the dependencies before running the application.

#

# From the project root:

#

# ```powershell

# streamlit run dashboard/app.py

# ```

#

# Streamlit will display a local URL in the terminal. Open that URL in a browser to view the dashboard.

#

# \## Screenshots

#

# Screenshots of the dashboard and Airflow execution are stored in `docs/screenshots/`.

#

# \### Dashboard KPIs

#

# !\[Dashboard KPIs](docs/screenshots/KPIs.png)

#

# \### Monthly Revenue

#

# !\[Monthly Revenue](docs/screenshots/Monthly\_revenue.png)

#

# \### Monthly Revenue and Orders

#

# !\[Monthly Revenue and Orders](docs/screenshots/Monthyly\_revenue\_orders.png)

#

# \### Top 10 Products by Revenue

#

# !\[Top 10 Products by Revenue](docs/screenshots/top\_10\_products.png)

#

# \### Customer Retention

#

# !\[Customer Retention](docs/screenshots/customer\_retention.png)

#

# \### Airflow ETL DAG

#

# !\[Airflow ETL DAG](docs/screenshots/airflow\_etl.png)

#

# \### Airflow ETL Execution

#

# !\[Airflow ETL Execution](docs/screenshots/running\_etl.png)

#

# \## Installation and Local Setup

#

# \### Prerequisites

#

# Install the following tools:

#

# \- Python 3.11

# \- PostgreSQL

# \- Docker Desktop

# \- Git

#

# \### 1. Clone the Repository

#

# ```powershell

# git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

# cd retail-analytics-platform

# ```

#

# Replace `<YOUR\_GITHUB\_REPOSITORY\_URL>` with the actual URL of your GitHub repository.

#

# \### 2. Create a Virtual Environment

#

# ```powershell

# python -m venv .venv

# ```

#

# Activate the environment in PowerShell:

#

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

#

# \### 3. Install Dependencies

#

# ```powershell

# pip install -r requirements.txt

# ```

#

# \### 4. Configure the Database

#

# Create a PostgreSQL database named `retail\_dw` if it does not already exist.

#

# Create a root `.env` file in the project directory with the following variables:

#

# ```dotenv

# DB\_HOST=localhost

# DB\_PORT=5432

# DB\_NAME=retail\_dw

# DB\_USER=your\_postgres\_username

# DB\_PASSWORD=your\_postgres\_password

# ```

#

# Replace the example username and password with your local PostgreSQL credentials. Do not commit this file to GitHub.

#

# For the Airflow containers, configure the database connection variables in `airflow/.env`. Use `host.docker.internal` as `DB\_HOST` when connecting from Docker containers to PostgreSQL running on the Windows host.

#

# \### 5. Prepare the Dataset

#

# Place the original UCI Online Retail Excel dataset at:

#

# ```text

# data/raw/Online Retail.xlsx

# ```

#

# Make sure the file name and location match the paths expected by the project scripts.

#

# \### 6. Run the Individual Pipeline Stages

#

# From the project root, run the scripts in sequence:

#

# ```powershell

# python src/ingestion/ingest.py

# python src/ingestion/stage\_data.py

# python src/validation/validate\_data.py

# python src/transformation/clean\_data.py

# python src/database/load\_dimensions.py

# python src/database/load\_fact\_sales.py

# ```

#

# \*\*Important:\*\* The fact-loading script is not fully idempotent. Do not rerun it against a populated `fact\_sales` table without first implementing and verifying an appropriate duplicate-prevention or reload strategy. For the orchestrated workflow, use the Airflow DAG's fact-table safety check.

#

# \### 7. Start the Dashboard

#

# ```powershell

# streamlit run dashboard/app.py

# ```

#

# \### 8. Run the Orchestrated Pipeline

#

# With Docker Desktop running and the Airflow environment configured:

#

# ```powershell

# docker compose -f airflow/docker-compose.yaml up -d --build

# ```

#

# Open `http://localhost:8080`, locate `retail\_analytics\_etl`, and trigger the DAG.

#

# \## Data Quality and Validation

#

# Data quality checks are applied before records enter the cleaned dataset.

#

# The validation stage checks for:

#

# \- Cancelled invoices.

# \- Invalid or non-positive quantities.

# \- Invalid or non-positive unit prices.

# \- Missing customer identifiers.

#

# Rejected records are stored separately with rejection reasons. The transformation stage then prepares valid transactions for analytical use, calculates revenue, and removes duplicate records.

#

# These steps help maintain consistency between the source dataset and the warehouse while retaining information about records excluded from the cleaned dataset.

#

# \## Key Business Insights

#

# The dashboard provides an overview of sales performance and customer purchasing activity.

#

# \- \*\*Revenue analysis:\*\* Monthly trends help identify changes in sales performance.

# \- \*\*Product analysis:\*\* Ranking products by revenue highlights the items contributing most to total sales.

# \- \*\*Customer analysis:\*\* Customer-level data supports segmentation and repeat-purchase analysis.

# \- \*\*Retention analysis:\*\* The repeat customer rate provides an overview of returning customer activity.

# \- \*\*Geographical analysis:\*\* Country-level sales comparisons help examine the distribution of transactions.

#

# The dashboard values are based on the warehouse data available when the project was validated and may change if the dataset or warehouse is reloaded.

#

# \## Limitations and Future Improvements

#

# Potential improvements to the platform include:

#

# \- Adding automated unit and integration tests for the ingestion, validation, transformation, and loading stages.

# \- Implementing stronger idempotency for fact-table loading.

# \- Adding automated refresh tasks for the sales and customer analytical marts.

# \- Adding explicit database schema creation and version-controlled SQL scripts.

# \- Introducing data quality monitoring and pipeline failure alerts.

# \- Adding incremental data loading for new transactions.

# \- Extending the project with customer churn or repeat-purchase prediction.

# \- Integrating MLflow for model tracking and model registry management.

# \- Exposing prediction services through FastAPI and packaging them with Docker.

# \- Adding monitoring metrics and defined retraining criteria for future ML workflows.

#

# \## Learning Outcomes

#

# This project demonstrates practical experience with:

#

# \- Building a multi-stage ETL pipeline.

# \- Working with structured transactional datasets using Pandas.

# \- Validating and transforming data for analytical use.

# \- Designing and querying a PostgreSQL data warehouse.

# \- Organizing data into dimension and fact tables.

# \- Orchestrating data workflows using Apache Airflow.

# \- Containerizing pipeline services with Docker Compose.

# \- Developing interactive analytics dashboards using Streamlit.

# \- Managing configuration and database credentials using environment variables.

# \- Documenting pipeline results and data quality checks.

#

# \## Author

#

# \*\*Nikita Prabhudesai\*\*

