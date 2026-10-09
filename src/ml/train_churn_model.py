import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv
import mlflow
import mlflow.sklearn
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("customer_churn")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


print("ENV CHECK:")
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD loaded:", bool(os.getenv("DB_PASSWORD")))

def load_customer_data():
    query = """
        SELECT
            customer_id,
            order_count,
            total_quantity,
            frequency,
            monetary_value,
            recency_days
        FROM customer_mart
    """

    conn = psycopg2.connect(**DB_CONFIG)

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def prepare_data(df):
    # Churn = no purchase for more than 90 days
    df["churn"] = (df["recency_days"] > 90).astype(int)

    return df
FEATURES = [
    "order_count",
    "total_quantity",
    "frequency",
    "monetary_value"
]

TARGET = "churn"
def split_data(df):
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test

def train_logistic_regression(X_train, y_train):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            random_state=42,
            max_iter=1000
        ))
    ])

    model.fit(X_train, y_train)

    return model
    
def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities)
    }

    return metrics

if __name__ == "__main__":
    df = load_customer_data()

    print(f"Loaded {len(df)} customers")

    df = prepare_data(df)

    print("\nChurn distribution:")
    print(df["churn"].value_counts())

    X_train, X_test, y_train, y_test = split_data(df)

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    with mlflow.start_run(run_name="logistic_regression_churn"):

        model = train_logistic_regression(X_train, y_train)

        metrics = evaluate_model(
            model,
            X_test,
            y_test
        )

        mlflow.log_params({
            "model": "Logistic Regression",
            "test_size": 0.2,
            "random_state": 42,
            "max_iter": 1000,
            "features": ", ".join(FEATURES),
            "churn_threshold_days": 90
        })

        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(
            model,
            "model"
        )

        print("\nLogistic Regression Results:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

    rf_model = train_random_forest(X_train, y_train)

    rf_metrics = evaluate_model(
        rf_model,
        X_test,
        y_test
    )

    print("\nRandom Forest Results:")
    for metric, value in rf_metrics.items():
        print(f"{metric}: {value:.4f}")