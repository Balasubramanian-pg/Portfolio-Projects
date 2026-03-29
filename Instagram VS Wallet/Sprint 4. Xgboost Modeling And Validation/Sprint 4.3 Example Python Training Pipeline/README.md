## Sprint 4.3

**Instagram vs Wallet**
**Example Python Training Pipeline**

---

### 1. Objective

Build a **production-aligned training pipeline** that:

* Trains a regret prediction model
* Respects temporal splits
* Handles imbalance
* Produces calibrated probabilities
* Outputs interpretable signals

This is not a notebook.
This is a **repeatable system**.

---

### 2. Pipeline Overview

Stages:

1. Load feature table
2. Sort and split (time-aware)
3. Prepare features and labels
4. Train XGBoost model
5. Validate with early stopping
6. Calibrate probabilities
7. Evaluate business metrics
8. Extract feature importance

---

### 3. Assumptions

* Input table: `ml.feature_instagram_wallet_v1`
* Target: `regret_flag`
* No leakage in features
* One row per `order_id`

---

### 4. Full Training Pipeline

```python
# =========================================
# 1. Imports
# =========================================
import pandas as pd
import numpy as np
import xgboost as xgb

from sklearn.metrics import (
    roc_auc_score,
    precision_recall_curve,
    average_precision_score
)
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

# =========================================
# 2. Load Data
# =========================================
df = pd.read_parquet("feature_instagram_wallet_v1.parquet")

# Sort by time (critical)
df = df.sort_values("purchase_timestamp")

# =========================================
# 3. Feature / Target Split
# =========================================
TARGET = "regret_flag"

DROP_COLS = [
    "order_id",
    "customer_id",
    "product_id",
    "purchase_timestamp",
    "return_flag",
    "return_type"
]

feature_cols = [c for c in df.columns if c not in DROP_COLS + [TARGET]]

X = df[feature_cols]
y = df[TARGET].astype(int)

# =========================================
# 4. Temporal Split
# =========================================
train_size = int(len(df) * 0.6)
val_size = int(len(df) * 0.2)

X_train = X.iloc[:train_size]
y_train = y.iloc[:train_size]

X_val = X.iloc[train_size:train_size + val_size]
y_val = y.iloc[train_size:train_size + val_size]

X_test = X.iloc[train_size + val_size:]
y_test = y.iloc[train_size + val_size:]

# =========================================
# 5. Handle Class Imbalance
# =========================================
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

# =========================================
# 6. Train XGBoost Model
# =========================================
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)

params = {
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "eta": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "scale_pos_weight": scale_pos_weight,
    "seed": 42
}

model = xgb.train(
    params,
    dtrain,
    num_boost_round=2000,
    evals=[(dtrain, "train"), (dval, "val")],
    early_stopping_rounds=50,
    verbose_eval=100
)

# =========================================
# 7. Calibration (Critical)
# =========================================
# Convert to sklearn-like wrapper for calibration
class XGBWrapper:
    def __init__(self, model):
        self.model = model
    
    def predict_proba(self, X):
        dmatrix = xgb.DMatrix(X)
        preds = self.model.predict(dmatrix)
        return np.vstack([1 - preds, preds]).T

wrapper = XGBWrapper(model)

calibrator = CalibratedClassifierCV(
    base_estimator=wrapper,
    method="isotonic",
    cv="prefit"
)

calibrator.fit(X_val, y_val)

# =========================================
# 8. Predictions
# =========================================
y_val_pred = calibrator.predict_proba(X_val)[:, 1]
y_test_pred = calibrator.predict_proba(X_test)[:, 1]

# =========================================
# 9. Evaluation Metrics
# =========================================
val_auc = roc_auc_score(y_val, y_val_pred)
test_auc = roc_auc_score(y_test, y_test_pred)

val_pr_auc = average_precision_score(y_val, y_val_pred)
test_pr_auc = average_precision_score(y_test, y_test_pred)

print(f"Validation AUC: {val_auc:.4f}")
print(f"Test AUC: {test_auc:.4f}")
print(f"Validation PR-AUC: {val_pr_auc:.4f}")
print(f"Test PR-AUC: {test_pr_auc:.4f}")

# =========================================
# 10. Precision@K (Business Metric)
# =========================================
def precision_at_k(y_true, y_scores, k=1000):
    idx = np.argsort(y_scores)[::-1][:k]
    return y_true.iloc[idx].mean()

print("Precision@1000:", precision_at_k(y_test, y_test_pred, k=1000))

# =========================================
# 11. Feature Importance
# =========================================
importance = model.get_score(importance_type="gain")
importance_df = pd.DataFrame({
    "feature": list(importance.keys()),
    "importance": list(importance.values())
}).sort_values("importance", ascending=False)

print(importance_df.head(15))
```

---

### 5. Key Design Choices

#### A. Temporal Split

* Prevents leakage
* Simulates real-world deployment

---

#### B. Scale Pos Weight

* Handles class imbalance
* Prevents trivial “all-zero” predictions

---

#### C. Early Stopping

* Avoids overfitting
* Uses validation set as guardrail

---

#### D. Probability Calibration

* Raw XGBoost outputs are not reliable probabilities
* Calibration ensures:

  * better threshold decisions
  * better business alignment

---

### 6. What This Pipeline Produces

* Calibrated regret probability per purchase
* Ranked list of risky transactions
* Feature importance for explainability

---

### 7. Failure Modes

#### 1. Skipping Calibration

* Thresholds become meaningless

#### 2. Ignoring Temporal Order

* Model learns future patterns

#### 3. Overfitting via Deep Trees

* Great validation, poor test performance

---

### 8. Unorthodox but High-Leverage Extension

#### Train Two Models

* Model A: Predict regret
* Model B: Predict intervention success

Final score:

```python
final_score = regret_probability * intervention_uplift
```

Why:

* Not all regret is preventable

---

### 9. Definition of Done

* Pipeline runs end-to-end
* Metrics computed on validation and test
* Model calibrated
* Feature importance extracted
* Ready for deployment

---

### 10. What This Enables

This pipeline feeds:

* Real-time scoring
* Intervention engine
* ROI estimation

---

At this point, the system stops being theoretical.
It starts making decisions that can cost or save real money.
