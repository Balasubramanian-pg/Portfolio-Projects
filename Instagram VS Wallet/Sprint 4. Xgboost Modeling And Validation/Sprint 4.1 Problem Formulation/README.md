# Sprint 4.1

**Instagram vs Wallet**
**Problem Formulation**

---

### 1. Objective

Define the modeling problem in a way that aligns with **business impact, not academic neatness**.

Most teams ask:

> Can we predict returns?

Wrong.

This project asks:

> Can we identify purchases that will be **regretted and are worth intervening on**?

---

### 2. Core Reframing

You are not predicting:

* all returns

You are predicting:

* **actionable regret risk**

That introduces two filters:

1. Regret, not defect or fraud
2. High-impact, not trivial

---

### 3. Target Variable

**Primary Target**

```
regret_flag = 1
```

Defined as:

* Return classified as regret
* Occurs within defined regret window (e.g., ≤ 7 days)

Everything else:

```
regret_flag = 0
```

---

### 4. Prediction Task

**Type:** Binary Classification

**Output:**

* Probability that a purchase leads to regret

```
P(regret | features_at_purchase)
```

---

### 5. Why Binary and Not Regression

You could predict:

* number of returns
* refund amount

But that optimizes the wrong thing.

Decision systems need:

* **prioritization**, not precision

Binary framing enables:

* ranking
* thresholding
* intervention triggering

---

### 6. Decision Framing (Critical)

The model does not act alone.

It feeds a decision rule:

```
IF P(regret) >= threshold
THEN trigger intervention
```

So the real problem is:

> Find a threshold where intervention cost < prevented loss

---

### 7. Cost Structure

Define two costs:

#### A. False Negative (Missed Regret)

* Customer returns item
* Loss:

  * logistics cost
  * resale loss
  * margin erosion

#### B. False Positive (Unnecessary Intervention)

* Customer would not have returned
* Cost:

  * friction
  * possible conversion drop
  * intervention cost

---

### 8. Objective Function

Standard ML metric:

* AUC

Not enough.

Real objective:

> Maximize **expected net benefit**

```
Net Benefit =
(Prevented Returns × Value per Return)
- (Interventions × Cost per Intervention)
```

---

### 9. Class Imbalance

Regret events are rare relative to purchases.

Implication:

* Model may default to predicting “no regret”

Solution:

* Use class weighting
* Optimize precision-recall, not just accuracy

---

### 10. Time-Aware Data Splitting

Random split is invalid.

Use:

* Train: older data
* Validation: recent data
* Test: latest data

Reason:

* Mimics real deployment
* Prevents leakage

---

### 11. Evaluation Metrics

#### Core Metrics

* **Precision@K**

  * Of top K risky purchases, how many are true regret

* **Recall**

  * How many regret cases captured

* **PR-AUC**

  * Better for imbalanced data

---

#### Business Metrics

* Expected prevented returns
* Intervention load
* Net revenue impact

---

### 12. Threshold Selection

Threshold is not technical.
It is economic.

Steps:

1. Compute precision-recall curve
2. Estimate:

   * value per prevented return
   * intervention cost
3. Choose threshold maximizing net benefit

---

### 13. Model Choice: Why XGBoost

Chosen because:

* Handles non-linear interactions
* Works well with tabular data
* Robust to missing values
* Captures feature interactions implicitly

Alternative models:

* Logistic regression → too linear
* Neural networks → overkill, less interpretable

---

### 14. Explainability Requirement

Model must provide:

* Top contributing features per prediction
* Global feature importance

Reason:

* Drives interventions
* Builds stakeholder trust

---

### 15. Failure Modes

#### 1. Predicting Everything as Safe

* High accuracy, zero usefulness

#### 2. Predicting Everything as Risky

* High recall, operational collapse

#### 3. Optimizing AUC Only

* Ignores business cost

---

### 16. Unorthodox but High-Leverage Shift

#### Predict “Regret Under Intervention”

Instead of:

* P(regret)

Try:

* P(regret | no intervention)

Why:

* Aligns directly with decision-making

Tradeoff:

* Requires experimental data

---

### 17. Definition of Done

* Target variable defined
* Problem framed as binary classification
* Cost structure understood
* Evaluation metrics aligned with business
* Data split strategy defined

---

### 18. What This Enables

This sprint sets:

* What the model learns
* How it is evaluated
* How it is used

---

A poorly framed problem produces a perfectly trained useless model.
