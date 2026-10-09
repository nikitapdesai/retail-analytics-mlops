import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

LOG_FILE = BASE_DIR / "data" / "monitoring" / "predictions.csv"


def record_prediction(
    order_count,
    total_quantity,
    frequency,
    monetary_value,
    churn_prediction,
    churn_probability
):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    new_record = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "order_count": order_count,
        "total_quantity": total_quantity,
        "frequency": frequency,
        "monetary_value": monetary_value,
        "churn_prediction": churn_prediction,
        "churn_probability": churn_probability
    }])

    if LOG_FILE.exists():
        new_record.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        new_record.to_csv(
            LOG_FILE,
            index=False
        )


def generate_monitoring_report():
    if not LOG_FILE.exists():
        print("No prediction data available yet.")
        return

    df = pd.read_csv(LOG_FILE)

    print("\n===== MODEL MONITORING REPORT =====")
    print(f"Total predictions: {len(df)}")

    print("\nPrediction distribution:")
    print(df["churn_prediction"].value_counts())

    print(
        f"\nAverage churn probability: "
        f"{df['churn_probability'].mean():.4f}"
    )

    print(
        f"Maximum churn probability: "
        f"{df['churn_probability'].max():.4f}"
    )

    print(
        f"Minimum churn probability: "
        f"{df['churn_probability'].min():.4f}"
    )


if __name__ == "__main__":
    generate_monitoring_report()