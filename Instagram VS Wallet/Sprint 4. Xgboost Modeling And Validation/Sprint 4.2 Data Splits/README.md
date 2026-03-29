# Sprint 4.2

**Instagram vs Wallet**
**Data Splits**

---

### 1. Objective

Design a data splitting strategy that **mirrors reality**, not convenience.

If your split is wrong:

* Validation looks great
* Production collapses

This sprint ensures the model learns from the past and is judged on the future.

---

### 2. Core Principle

> You cannot train on the future and pretend it’s prediction.

Time is not just a column.
It is the **direction of causality**.

---

### 3. Why Random Split Fails

Random splitting:

* mixes past and future
* leaks temporal patterns
* inflates performance

Example failure:

* Model sees late-stage trend patterns in training
* Uses them to “predict” earlier periods

Result:

* Fake accuracy

---

### 4. Correct Strategy: Temporal Split

Split data based on time:

* **Train Set** → oldest data
* **Validation Set** → recent past
* **Test Set** → most recent unseen data

---

### 5. Example Split (2021 Data)

| Dataset    | Time Range | Purpose          |
| ---------- | ---------- | ---------------- |
| Train      | Jan – Aug  | Learn patterns   |
| Validation | Sep – Oct  | Tune model       |
| Test       | Nov – Dec  | Final evaluation |

---

### 6. Implementation Logic

Sort by:

```python
purchase_timestamp
```

Then split sequentially:

* First 60% → Train
* Next 20% → Validation
* Last 20% → Test

---

### 7. Code Example (Python)

```python
df = df.sort_values("purchase_timestamp")

train_size = int(len(df) * 0.6)
val_size = int(len(df) * 0.2)

train = df.iloc[:train_size]
val = df.iloc[train_size:train_size + val_size]
test = df.iloc[train_size + val_size:]
```

---

### 8. Advanced Strategy: Rolling Window Validation

Instead of one split:

Train multiple times:

* Train: Jan–Jun → Validate: Jul
* Train: Jan–Jul → Validate: Aug
* Train: Jan–Aug → Validate: Sep

Purpose:

* Test stability across time
* Detect drift

---

### 9. Stratification Considerations

Standard stratification (balancing classes) is risky here.

Why:

* It breaks temporal structure

Better approach:

* Accept imbalance
* Use class weights

---

### 10. Leakage Checks

After splitting, verify:

* No overlap in time
* No feature leakage across splits
* Similar feature distributions

Critical check:

* Ensure no future-derived aggregates exist

---

### 11. Distribution Monitoring

Compare across splits:

* regret rate
* trend velocity distribution
* discount distribution

If distributions shift heavily:

* model may struggle
* consider drift handling

---

### 12. Edge Case: Cold Start Products

New products appear only in test set.

Implication:

* Model must generalize
* Cannot rely on product history alone

Mitigation:

* Use category-level features
* Use trend signals

---

### 13. Failure Modes

#### 1. Temporal Leakage

Future data in training

#### 2. Overfitting to Time Period

Model learns seasonal quirks

#### 3. Ignoring Drift

Model performs well in past, fails in future

---

### 14. Unorthodox but High-Leverage Addition

#### “Stress Test Split”

Create a test set with:

* extreme trends
* high-velocity spikes
* unusual conditions

Purpose:

* Evaluate model under pressure
* Not just average performance

---

### 15. Metrics by Split

Track separately:

* Train performance
* Validation performance
* Test performance

Red flags:

* Huge gap → overfitting
* Sudden drop → drift

---

### 16. Definition of Done

* Temporal split implemented
* No leakage verified
* Validation strategy defined
* Distribution checked
* Edge cases considered

---

### 17. What This Enables

Proper splits ensure:

* Honest evaluation
* Reliable deployment
* Stable model behavior

---

Bad splits don’t just mislead you.
They give you confidence right before failure.
