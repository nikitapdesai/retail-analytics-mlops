import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


# --------------------------------------------------
# 2. Database connection
# --------------------------------------------------

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()


# --------------------------------------------------
# 3. Load cleaned dataset
# --------------------------------------------------

cleaned_file = PROJECT_ROOT / "data" / "processed" / "cleaned_retail.csv"

print("Reading cleaned dataset...")
df = pd.read_csv(cleaned_file)

print(f"Rows loaded: {len(df)}")


# --------------------------------------------------
# 4. Prepare date dimension
# --------------------------------------------------

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

unique_dates = df["InvoiceDate"].dt.date.unique()

print(f"Loading {len(unique_dates)} dates...")


for date_value in unique_dates:

    date_timestamp = pd.Timestamp(date_value)

    date_key = int(date_timestamp.strftime("%Y%m%d"))

    year = date_timestamp.year
    quarter = date_timestamp.quarter
    month = date_timestamp.month
    month_name = date_timestamp.strftime("%B")
    week = int(date_timestamp.isocalendar().week)
    day = date_timestamp.day
    day_name = date_timestamp.strftime("%A")

    cursor.execute(
        """
        INSERT INTO dim_date
        (
            date_key,
            full_date,
            year,
            quarter,
            month,
            month_name,
            week,
            day,
            day_name
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date_key) DO NOTHING;
        """,
        (
            date_key,
            date_value,
            year,
            quarter,
            month,
            month_name,
            week,
            day,
            day_name
        )
    )


# --------------------------------------------------
# 5. Prepare customer dimension
# --------------------------------------------------

print("Loading customers...")

customers = (
    df[["CustomerID", "Country"]]
    .drop_duplicates(subset=["CustomerID"])
)

for _, row in customers.iterrows():

    cursor.execute(
        """
        INSERT INTO dim_customer
        (
            customer_id,
            country
        )
        VALUES (%s, %s)
        ON CONFLICT (customer_id) DO NOTHING;
        """,
        (
            int(row["CustomerID"]),
            row["Country"]
        )
    )


# --------------------------------------------------
# 6. Prepare product dimension
# --------------------------------------------------

print("Loading products...")

products = (
    df[["StockCode", "Description"]]
    .drop_duplicates(subset=["StockCode"])
)

for _, row in products.iterrows():

    description = row["Description"]

    if pd.isna(description):
        description = None

    cursor.execute(
        """
        INSERT INTO dim_product
        (
            stock_code,
            description
        )
        VALUES (%s, %s)
        ON CONFLICT (stock_code) DO NOTHING;
        """,
        (
            str(row["StockCode"]),
            description
        )
    )


# --------------------------------------------------
# 7. Prepare geography dimension
# --------------------------------------------------

print("Loading countries...")

countries = df["Country"].dropna().unique()

for country in countries:

    cursor.execute(
        """
        INSERT INTO dim_geography
        (
            country
        )
        VALUES (%s)
        ON CONFLICT (country) DO NOTHING;
        """,
        (country,)
    )


# --------------------------------------------------
# 8. Commit changes
# --------------------------------------------------

conn.commit()

print()
print("Dimension loading successful!")


# --------------------------------------------------
# 9. Display row counts
# --------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM dim_date;")
print("dim_date rows:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM dim_customer;")
print("dim_customer rows:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM dim_product;")
print("dim_product rows:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM dim_geography;")
print("dim_geography rows:", cursor.fetchone()[0])


# --------------------------------------------------
# 10. Close connection
# --------------------------------------------------

cursor.close()
conn.close()

print("Database connection closed.")