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
# 4. Prepare data types
# --------------------------------------------------

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["CustomerID"] = df["CustomerID"].astype(int)

df["Quantity"] = df["Quantity"].astype(int)

df["UnitPrice"] = df["UnitPrice"].astype(float)

df["Revenue"] = df["Revenue"].astype(float)


# --------------------------------------------------
# 5. Create lookup dictionaries
# --------------------------------------------------

print("Loading dimension keys...")

cursor.execute("""
    SELECT date_key, full_date
    FROM dim_date;
""")

date_lookup = {
    row[1]: row[0]
    for row in cursor.fetchall()
}


cursor.execute("""
    SELECT customer_key, customer_id
    FROM dim_customer;
""")

customer_lookup = {
    row[1]: row[0]
    for row in cursor.fetchall()
}


cursor.execute("""
    SELECT product_key, stock_code
    FROM dim_product;
""")

product_lookup = {
    row[1]: row[0]
    for row in cursor.fetchall()
}


cursor.execute("""
    SELECT geography_key, country
    FROM dim_geography;
""")

geography_lookup = {
    row[1]: row[0]
    for row in cursor.fetchall()
}


# --------------------------------------------------
# 6. Prepare fact records
# --------------------------------------------------

print("Preparing fact records...")

records = []

for _, row in df.iterrows():

    invoice_date = row["InvoiceDate"].date()

    date_key = date_lookup.get(invoice_date)

    customer_key = customer_lookup.get(
        int(row["CustomerID"])
    )

    product_key = product_lookup.get(
        str(row["StockCode"])
    )

    geography_key = geography_lookup.get(
        row["Country"]
    )

    if (
        date_key is None
        or customer_key is None
        or product_key is None
        or geography_key is None
    ):
        continue

    records.append(
        (
            str(row["InvoiceNo"]),
            date_key,
            customer_key,
            product_key,
            geography_key,
            int(row["Quantity"]),
            float(row["UnitPrice"]),
            float(row["Revenue"])
        )
    )


print(f"Fact records prepared: {len(records)}")


# --------------------------------------------------
# 7. Insert fact records
# --------------------------------------------------

print("Loading fact_sales...")

insert_query = """
    INSERT INTO fact_sales
    (
        invoice_no,
        date_key,
        customer_key,
        product_key,
        geography_key,
        quantity,
        unit_price,
        revenue
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""


# Insert in batches
batch_size = 5000

for start in range(0, len(records), batch_size):

    batch = records[start:start + batch_size]

    cursor.executemany(
        insert_query,
        batch
    )

    conn.commit()

    print(
        f"Inserted {min(start + batch_size, len(records))}"
        f"/{len(records)} records"
    )


# --------------------------------------------------
# 8. Verify fact table
# --------------------------------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM fact_sales;
""")

fact_count = cursor.fetchone()[0]

print()
print("Fact loading successful!")
print("fact_sales rows:", fact_count)


# --------------------------------------------------
# 9. Close connection
# --------------------------------------------------

cursor.close()
conn.close()

print("Database connection closed.")