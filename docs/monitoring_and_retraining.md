# Model Monitoring and Retraining Strategy

## 1. Prediction Monitoring

The FastAPI churn prediction service records each prediction in `data/monitoring/predictions.csv`. Each record includes the timestamp, input features, predicted churn label, and churn probability.

The monitored fields are:

* `order_count`
* `total_quantity`
* `frequency`
* `monetary_value`
* `churn_prediction`
* `churn_probability`

This log supports tracking API prediction activity and reviewing model outputs over time.

## 2. Retraining Criteria

The model should be evaluated for retraining when one or more of the following conditions occur:

1. **Performance degradation:** Evaluation on newly labelled customer data shows a meaningful decline in F1-score, recall, or ROC-AUC compared with the current model.
2. **Data drift:** The distribution of customer behaviour features changes substantially from the training data.
3. **Business changes:** Changes in customer purchasing patterns or the business definition of churn make the existing model less suitable.
4. **Scheduled review:** Review model performance periodically and retrain when new, representative labelled data is available.

These criteria are proposed operational guidelines. They are not automatic triggers currently implemented in the API.

## 3. Retraining Workflow

1. Collect updated retail transaction and customer data.
2. Apply the existing data cleaning and feature engineering pipeline.
3. Retrain candidate models and evaluate them using consistent validation metrics.
4. Compare candidates against the currently registered model.
5. Register and deploy a new model version only if it meets the selected performance and validation requirements.
6. Retain the previous model version so the deployment can be rolled back if necessary.

## 4. Current Implementation and Future Work

The current implementation logs prediction inputs and outputs to a CSV file mounted from the host into the Docker container. MLflow is used for experiment tracking and model registry, and FastAPI exposes the prediction endpoint.

Future improvements include automated data-drift checks, performance monitoring using newly labelled outcomes, configurable retraining thresholds, and an automated retraining pipeline.
