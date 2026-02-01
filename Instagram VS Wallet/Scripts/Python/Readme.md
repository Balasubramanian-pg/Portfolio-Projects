# Production-Ready XGBoost Training Notebook with Hyperparameter Tuning and SHAP Explainability for TrendBuy

**Context**: This notebook is designed to be **exportable to MLflow**, support **systematic hyperparameter tuning**, and generate **SHAP explainability artifacts**. It assumes data is already prepared in a Snowflake or similar environment and available as a feature table (`feature_trendbuy_v1`). The model predicts `returned_within_30d` or another regret label. The notebook is structured into logical sections with clear headings, examples, and operational details suitable for use in a real data science workflow.

Where applicable, factual claims about tools and libraries are supported with citations from authoritative sources.

## Notebook Overview and Objectives

### Purpose

This notebook will:

* Load features from the warehouse
* Prepare training, validation, and test splits following temporal logic
* Train a baseline model
* Perform hyperparameter tuning with MLflow and cross-validation
* Evaluate model performance
* Save tuned model to MLflow
* Compute and visualize SHAP explainability
* Export model artifacts and explanations

### Requirements

Install the following Python packages (example install commands; confirm versions match environment policy):

```bash
pip install xgboost scikit-learn shap mlflow pandas snowflake-connector-python mlflow-extras
```

* `xgboost`: gradient boosted trees algorithm widely used for tabular data classification tasks.
* `shap`: SHAP (SHapley Additive exPlanations) for model explainability.
* `mlflow`: for experiment tracking and model versioning.

## 1. Environment Setup and Imports

```python
import os
import pandas as pd
import numpy as np
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import roc_auc_score, precision_recall_curve, classification_report
import xgboost as xgb
import shap
import joblib
```

### Notes on MLflow

* MLflow tracks parameters, metrics, and artifacts.
* This notebook uses an experiment named `TrendBuy_XGB_RegretRisk`.
* Use `mlflow ui` to inspect runs locally or configured remote server.

## 2. Load Training Data

### Reasoning Summary

* Queries the feature table using Snowflake Python connector.
* Uses a temporal split: training on older data, validation on recent, and test on newest to avoid leakage.
* Ensures all features are present and aligned with modeling.

### Example Code

```python
import snowflake.connector

# Snowflake connection settings from environment
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database="TRENDBUY_MART",
    schema="FEATURES"
)

query = """
SELECT
  order_id,
  returned_within_30d AS label,
  feature_discount_pct,
  feature_velocity_24h,
  feature_hours_since_trend_peak,
  feature_creator_reliability,
  feature_cust_prior_return_rate_90d,
  feature_cust_avg_order_value_90d,
  feature_prod_size_fit_rate,
  feature_device_type
FROM feature_trendbuy_v1
WHERE purchase_timestamp < CURRENT_TIMESTAMP() - INTERVAL '7' DAY
"""

df = pd.read_sql(query, conn)
conn.close()
```

**Assumption**: A feature table exists with label and engineered features in the warehouse.

## 3. Train, Validation, Test Split

### Reasoning Summary

* A temporal split mitigates leakage.
* Latest data reserved for validation and test.
* Example uses last 10–20% for validation/test.

```python
df = df.sort_values("purchase_timestamp")

# Define splits
n = len(df)
train_end = int(n * 0.7)
val_end = int(n * 0.85)

df_train = df.iloc[:train_end]
df_val = df.iloc[train_end:val_end]
df_test = df.iloc[val_end:]

X_train = df_train.drop(columns=["label", "order_id"])
y_train = df_train["label"]

X_val = df_val.drop(columns=["label", "order_id"])
y_val = df_val["label"]

X_test = df_test.drop(columns=["label", "order_id"])
y_test = df_test["label"]
```

## 4. Baseline XGBoost Model

### Reasoning Summary

* Start with a default XGBoost classifier to establish a baseline.
* Later refined with hyperparameter tuning.

```python
baseline_model = xgb.XGBClassifier(
    objective="binary:logistic",
    eval_metric="auc",
    use_label_encoder=False
)

baseline_model.fit(X_train, y_train)
val_pred_proba = baseline_model.predict_proba(X_val)[:, 1]
```

### Evaluate Baseline

```python
val_auc = roc_auc_score(y_val, val_pred_proba)
print(f"Baseline Validation AUC: {val_auc:.4f}")
```

## 5. Hyperparameter Tuning with Grid Search and MLflow

### Reasoning Summary

* Use time series aware cross-validation when possible.
* Use `GridSearchCV` with temporal splits.
* Record parameters and metrics in MLflow.

### Grid Search Setup

```python
param_grid = {
    "max_depth": [4, 6, 8],
    "learning_rate": [0.01, 0.05, 0.1],
    "subsample": [0.8, 1.0],
    "colsample_bytree": [0.8, 1.0],
    "n_estimators": [200, 500, 1000]
}

tscv = TimeSeriesSplit(n_splits=5)

grid_search = GridSearchCV(
    estimator=xgb.XGBClassifier(
        objective="binary:logistic",
        eval_metric="auc",
        use_label_encoder=False
    ),
    param_grid=param_grid,
    scoring="roc_auc",
    cv=tscv,
    verbose=2
)
```

### Run Tuning and Log with MLflow

```python
mlflow.set_experiment("TrendBuy_XGB_RegretRisk")
with mlflow.start_run(run_name="grid_search"):
    grid_search.fit(X_train, y_train)
    
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    mlflow.log_params(best_params)
    mlflow.log_metric("best_cv_auc", best_score)

    best_model = grid_search.best_estimator_
    joblib.dump(best_model, "best_xgb_model.pkl")
    mlflow.log_artifact("best_xgb_model.pkl")
```

## 6. Final Model Evaluation

### Validation and Test Performance

```python
val_pred = best_model.predict_proba(X_val)[:,1]
test_pred = best_model.predict_proba(X_test)[:,1]

val_auc = roc_auc_score(y_val, val_pred)
test_auc = roc_auc_score(y_test, test_pred)

print(f"Tuned Validation AUC: {val_auc:.4f}")
print(f"Test AUC: {test_auc:.4f}")

mlflow.log_metric("val_auc", val_auc)
mlflow.log_metric("test_auc", test_auc)
```

## 7. SHAP Explainability

### Reasoning Summary

* SHAP values quantify each feature’s contribution to each model prediction.
* Global and local explanations are useful for actionable insights.

### Compute SHAP Values

```python
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_train)

shap.summary_plot(shap_values, X_train)
```

### Save SHAP Artifacts

```python
shap.summary_plot(shap_values, X_train, show=False)
plt.savefig("shap_summary.png")
mlflow.log_artifact("shap_summary.png")
```

## 8. Explainability for Individual Predictions

```python
idx = 5  # example index
shap.force_plot(
    explainer.expected_value,
    shap_values[idx,:],
    X_train.iloc[idx,:],
    matplotlib=True
)
plt.savefig("shap_force_plot.png")
mlflow.log_artifact("shap_force_plot.png")
```

---

## 9. Model Registration in MLflow

```python
model_uri = f"runs:/{mlflow.active_run().info.run_id}/best_xgb_model.pkl"
mlflow.register_model(model_uri, "TrendBuy_XGB_RegretModel")
```

## 10. Export Model for Serving

### Save with Joblib

```python
joblib.dump(best_model, "trendbuy_xgb_model_v1.pkl")
```

### Optionally Save Scikit-Compatible Pipeline

If you wrap preprocessing and model in a `Pipeline`, save that.

## 11. Notes on Validation and Drift Monitoring

* Monitor model performance periodically using rolling AUC or calibration curves.
* A decline in performance may indicate feature drift.
* Drift detection may require additional tooling such as **Evidently.ai** or custom monitoring. I cannot verify drift levels without live data; next step is to build automated data quality dashboards.

## 12. Deployment Considerations

* Package the model and preprocessing logic into a REST API for real-time scoring (FastAPI, Seldon Core, or equivalent).
* Use versioned artifacts from MLflow for reproducibility.

Technical documentation for deploying XGBoost models in production: XGBoost documentation covers model persistence formats. SHAP usage and visualization references from SHAP documentation.
Citations:

* XGBoost docs: [https://xgboost.readthedocs.io/en/stable/](https://xgboost.readthedocs.io/en/stable/)
* SHAP docs: [https://shap.readthedocs.io/en/latest/](https://shap.readthedocs.io/en/latest/)
* MLflow docs: [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)

## 13. What Requires Verification or Is Uncertain

1. Exact time windows used to define `returned_within_30d` should be verified with business definitions. I cannot verify this.
2. Distribution and cardinality of categorical features like `feature_device_type` may require encoding adjustments.
3. Drift thresholds and retraining cadence should be aligned with operational KPIs.
4. MLflow tracking server configuration and artifact storage settings require environment validation.

This notebook provides a complete conceptualization, structured implementation, and exportable model workflow for real-world use in TrendBuy’s regret risk prediction system. If you want, I can now generate a fully runnable `.py` script or a parameterized Jupyter notebook template including cells ready for execution in your environment.
