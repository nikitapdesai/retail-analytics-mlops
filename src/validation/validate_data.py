import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

STAGING_FILE = PROJECT_ROOT / "data" / "staging" / "online_retail_staging.csv"
REJECTED_FILE = PROJECT_ROOT / "data" / "rejected" / "rejected_records.csv"


def validate_data():

    print("Reading staging data...")

    df = pd.read_csv(STAGING_FILE)

    print(f"Total rows: {len(df)}")

    # Identify invalid records
    cancelled = df["InvoiceNo"].astype(str).str.startswith("C")
    invalid_quantity = df["Quantity"] <= 0
    invalid_price = df["UnitPrice"] <= 0
    missing_customer = df["CustomerID"].isna()

    rejected = df[
        cancelled
        | invalid_quantity
        | invalid_price
        | missing_customer
    ].copy()

    
    def get_reason(row):
        reasons = []

        if str(row["InvoiceNo"]).startswith("C"):
            reasons.append("Cancelled invoice")

        if row["Quantity"] <= 0:
            reasons.append("Invalid quantity")

        if row["UnitPrice"] <= 0:
            reasons.append("Invalid price")

        if pd.isna(row["CustomerID"]):
            reasons.append("Missing customer ID")

        return "; ".join(reasons)

    rejected["rejection_reason"] = rejected.apply(get_reason, axis=1)

    # Save rejected records
    rejected.to_csv(REJECTED_FILE, index=False)

    print(f"Rejected rows: {len(rejected)}")
    print(f"Rejected file: {REJECTED_FILE}")

    # Valid records
    valid = df.drop(rejected.index).copy()

    print(f"Valid rows: {len(valid)}")

    return valid


if __name__ == "__main__":
    validate_data()