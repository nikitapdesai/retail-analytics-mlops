import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
STAGING_FILE = PROJECT_ROOT / "data" / "staging" / "online_retail_staging.csv"


def stage_data():
    print("Reading raw dataset...")

    df = pd.read_excel(RAW_FILE)

    print(f"Rows read: {len(df)}")

    df.to_csv(STAGING_FILE, index=False)

    print("Staging successful")
    print(f"Staging file: {STAGING_FILE}")
    print(f"Rows written: {len(df)}")


if __name__ == "__main__":
    stage_data()