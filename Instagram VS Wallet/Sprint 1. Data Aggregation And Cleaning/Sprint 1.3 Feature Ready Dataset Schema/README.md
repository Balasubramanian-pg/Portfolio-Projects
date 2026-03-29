## Sprint 1.3

**Instagram vs Wallet**
**Feature-Ready Dataset Schema**

---

### 1. Objective

Design a **single, denormalized dataset** that is:

* Causally valid
* Model-ready
* Reproducible
* Extensible

This dataset is the **contract between data engineering and modeling**.
If this contract is weak, every model becomes fragile.

---

### 2. Core Principle

Each row represents:

> **One purchase decision at a specific moment in time, with all information available at that moment**

Not after. Not aggregated loosely. Not inferred later.

---

### 3. Table Definition

**Table Name:**
`fact_instagram_purchase_outcomes`

**Grain:**

* 1 row = 1 order_id

---

### 4. Schema Overview

Five feature blocks:

1. **Identifiers & Timestamps**
2. **Exposure (Instagram/Trend Signals)**
3. **Transaction Context**
4. **Customer Behavior**
5. **Product Attributes**
6. **Outcome Labels**

---

### 5. Identifiers & Timestamps

| Column             | Description           |
| ------------------ | --------------------- |
| order_id           | Unique transaction ID |
| customer_id        | Unique user ID        |
| product_id         | Purchased product     |
| purchase_timestamp | Decision moment       |

Strict rule:
Everything else must be derived relative to `purchase_timestamp`.

---

### 6. Exposure Features (Trend Layer)

These capture **what influenced the purchase**.

| Column                 | Description                         |
| ---------------------- | ----------------------------------- |
| trend_id               | Attributed trend                    |
| trend_velocity_24h     | Engagement speed before purchase    |
| trend_half_life_hours  | Decay factor                        |
| hours_since_trend_peak | Recency signal                      |
| sentiment_score        | Comment sentiment                   |
| exposure_count_12h     | Number of exposures before purchase |

**Derived Insight**
Velocity matters more than total views.
Decay matters more than peak.

---

### 7. Transaction Context

This captures **how the purchase happened**.

| Column           | Description                |
| ---------------- | -------------------------- |
| price_paid       | Final price                |
| discount_pct     | Discount intensity         |
| channel_source   | Instagram / direct         |
| device_type      | Mobile / desktop           |
| time_of_day      | Hour bucket                |
| session_duration | Time spent before purchase |

**Key Signal**
Discount × velocity interaction is often explosive.

---

### 8. Customer Behavior Features

This captures **who is making the decision**.

| Column                 | Description                |
| ---------------------- | -------------------------- |
| prior_return_rate_90d  | Historical regret tendency |
| avg_order_value_90d    | Spending behavior          |
| purchase_frequency_30d | Activity level             |
| impulse_score          | Derived behavioral metric  |
| recency_days           | Days since last purchase   |

These features introduce **memory into the system**.

---

### 9. Product Attributes

This captures **intrinsic product risk**.

| Column              | Description              |
| ------------------- | ------------------------ |
| category            | Apparel type             |
| price_band          | Low / mid / premium      |
| size_fit_issue_rate | Historical fit problems  |
| product_return_rate | Baseline return rate     |
| trend_sensitivity   | How often product trends |

Important:
Without this, model confuses **bad products with bad decisions**.

---

### 10. Outcome Labels

This is the target layer.

| Column           | Description               |
| ---------------- | ------------------------- |
| return_flag      | 1 if returned             |
| return_timestamp | When return happened      |
| regret_flag      | 1 if classified as regret |
| return_type      | regret / defect / fraud   |

Critical:

* `regret_flag` is the modeling target
* Must follow Sprint 0 taxonomy

---

### 11. Derived Interaction Features

These are not optional. They carry signal.

Examples:

* `velocity × discount_pct`
* `prior_return_rate × trend_velocity`
* `hours_since_trend_peak × impulse_score`

These capture **non-linear behavior**.

---

### 12. Data Constraints

Hard rules:

* No feature uses future information
* One row per order_id
* No nulls in critical fields
* All timestamps aligned

---

### 13. Example Schema (SQL)

```sql id="c2ph0x"
CREATE TABLE fact_instagram_purchase_outcomes AS
SELECT
  -- identifiers
  order_id,
  customer_id,
  product_id,
  purchase_timestamp,

  -- exposure
  trend_id,
  trend_velocity_24h,
  trend_half_life_hours,
  hours_since_trend_peak,
  sentiment_score,

  -- transaction
  price_paid,
  discount_pct,
  channel_source,
  device_type,

  -- customer
  prior_return_rate_90d,
  avg_order_value_90d,

  -- product
  category,
  size_fit_issue_rate,

  -- outcome
  return_flag,
  regret_flag
FROM ...
```

---

### 14. Validation Checklist

Before using this dataset:

**1. Leakage Check**

* No feature timestamp > purchase_timestamp

**2. Row Integrity**

* Count(order_id) == distinct(order_id)

**3. Distribution Check**

* Features vary meaningfully
* No constant columns

**4. Label Sanity**

* Regret rate within expected bounds

---

### 15. Failure Modes

#### 1. Over-Aggregation

* Losing time resolution
  → weak signals

#### 2. Under-Contextualization

* Missing customer/product features
  → biased model

#### 3. Label Noise

* Poor regret definition
  → model learns wrong behavior

---

### 16. Unorthodox but High-Leverage Addition

#### Add “Non-Purchase Rows”

Schema extension:

* Include exposures where purchase = 0

Why:

* Enables true behavioral modeling
* Captures decision boundary

Tradeoff:

* Requires negative sampling strategy

---

### 17. Definition of Done

* Schema finalized
* All feature blocks defined
* Interaction features identified
* Validation checks passed
* Dataset reproducible

---

### 18. What This Enables

This dataset becomes:

* The training foundation
* The scoring input
* The analytics backbone

---

A model is only as good as the story your dataset tells.
Right now, you are deciding whether that story is causal or accidental.
