from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd
import logging
from datetime import datetime
from src.monitoring.monitor import record_prediction
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using the registered MLflow model.",
    version="1.0.0"
)

mlflow.set_tracking_uri("http://host.docker.internal:5000")

MODEL_URI = "models:/CustomerChurnModel/2"

model = mlflow.sklearn.load_model(MODEL_URI)


class CustomerData(BaseModel):
    order_count: int
    total_quantity: int
    frequency: int
    monetary_value: float


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running"
    }


@app.post("/predict")
def predict_churn(customer: CustomerData):

    input_data = pd.DataFrame([{
        "order_count": customer.order_count,
        "total_quantity": customer.total_quantity,
        "frequency": customer.frequency,
        "monetary_value": customer.monetary_value
    }])

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]
    logger.info(
    "Prediction | timestamp=%s | churn_prediction=%s | churn_probability=%.4f",
    datetime.now().isoformat(),
    int(prediction),
    float(probability)
)
    record_prediction(
    order_count=customer.order_count,
    total_quantity=customer.total_quantity,
    frequency=customer.frequency,
    monetary_value=customer.monetary_value,
    churn_prediction=int(prediction),
    churn_probability=float(probability)
)

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4)
    }