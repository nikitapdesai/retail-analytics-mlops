import pandas as pd
from pathlib import Path
from datetime import datetime
import json


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
LOG_FILE = PROJECT_ROOT / "data" / "raw" / "ingestion_log.json"


def ingest_data():

    extraction_date = datetime.now().isoformat()

    log = {
        "source": "UCI Online Retail Dataset",
        "file_name": RAW_FILE.name,
        "extraction_date": extraction_date,
        "status": "FAILED",
        "row_count": 0,
        "error": None
    }

    try:

        # Check whether source file exists
        if not RAW_FILE.exists():
            raise FileNotFoundError(
                f"Source file not found: {RAW_FILE}"
            )

        # Read the raw dataset
        df = pd.read_excel(RAW_FILE)

        # Record successful ingestion
        log["status"] = "SUCCESS"
        log["row_count"] = len(df)

        print("Ingestion successful")
        print(f"Source: {log['source']}")
        print(f"File: {log['file_name']}")
        print(f"Rows: {log['row_count']}")
        print(f"Extraction date: {log['extraction_date']}")

    except Exception as e:

        log["error"] = str(e)

        print("Ingestion failed")
        print(f"Error: {e}")

    # Save ingestion metadata
    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(log, file, indent=4)

    return df if log["status"] == "SUCCESS" else None


if __name__ == "__main__":
    ingest_data()