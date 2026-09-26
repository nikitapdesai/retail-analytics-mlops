import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_FILE = PROJECT_ROOT / "data" / "staging" / "online_retail_staging.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_retail.csv"


def clean_data():

    print("Reading staging data...")

    df = pd.read_csv(STAGING_FILE)

    print(f"Initial rows: {len(df)}")

    # Remove cancelled invoices
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

    # Remove invalid quantities
    df = df[df["Quantity"] > 0]

    # Remove invalid prices
    df = df[df["UnitPrice"] > 0]

    # Remove records without customer ID
    df = df.dropna(subset=["CustomerID"])

    # Convert data types
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["Quantity"] = df["Quantity"].astype(int)
    df["UnitPrice"] = df["UnitPrice"].astype(float)

    # Calculate revenue
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Remove duplicate records
    before_duplicates = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_duplicates - len(df)

    # Save processed data
    df.to_csv(PROCESSED_FILE, index=False)

    print("Cleaning successful")
    print(f"Final rows: {len(df)}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Processed file: {PROCESSED_FILE}")


if __name__ == "__main__":
    clean_data()