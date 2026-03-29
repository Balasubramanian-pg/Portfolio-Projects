## Sprint 1.1

**Instagram vs Wallet**
**Data Source Description**

---

### 1. Objective

Define the **minimum viable data universe** required to reconstruct the causal chain:

> Exposure → Desire → Purchase → Regret → Return

If any link is missing or weak, the system degenerates into correlation guessing.

---

### 2. Core Principle

You are not collecting data.
You are reconstructing **decision context at the moment of purchase**.

That means:

* What the user saw
* What state they were in
* What pushed them over the edge

---

### 3. Data Source Architecture

Four primary data domains:

1. **Instagram / Trend Exposure Data**
2. **E-commerce Transaction Data**
3. **Return & Outcome Data**
4. **Customer Behavioral Data**

Optional but high leverage:
5. **Product & Catalog Data**

---

### 4. Instagram / Trend Exposure Data

This is the ignition source.

**Key Fields**

* `trend_id`
* `product_id`
* `creator_id`
* `engagement_velocity`
* `view_count`
* `like_rate`
* `comment_sentiment_score`
* `trend_start_timestamp`
* `trend_half_life`

**Derived Signals**

* Velocity spike (rate of change, not raw views)
* Sentiment polarity
* Trend decay curve

**Critical Insight**
Raw views are useless.
Velocity and decay tell you whether the user is buying into hype or stability.

---

### 5. E-commerce Transaction Data

This is the commitment event.

**Key Fields**

* `order_id`
* `customer_id`
* `product_id`
* `purchase_timestamp`
* `price_paid`
* `discount_pct`
* `channel_source` (Instagram, direct, etc.)
* `device_type`
* `session_duration`

**Derived Signals**

* Time between exposure and purchase
* Discount-triggered impulse likelihood
* Multi-session vs instant purchase

---

### 6. Return & Outcome Data

This defines the target.

**Key Fields**

* `order_id`
* `return_flag`
* `return_timestamp`
* `return_reason_code`
* `refund_amount`
* `resale_eligibility_flag`

**Derived Signals**

* Time-to-return
* Regret classification (from Sprint 0)
* Return intensity by cohort

---

### 7. Customer Behavioral Data

This provides context and memory.

**Key Fields**

* `customer_id`
* `prior_return_rate_90d`
* `avg_order_value`
* `purchase_frequency`
* `category_affinity`
* `device_usage_pattern`

**Derived Signals**

* Impulse propensity score
* Risk tolerance
* Repeat regret behavior

---

### 8. Product & Catalog Data (Optional but Critical)

This is where most teams underinvest.

**Key Fields**

* `product_id`
* `category`
* `price_band`
* `size_variability`
* `fit_issue_rate`
* `return_rate_by_sku`

**Derived Signals**

* Intrinsic product risk
* Fit uncertainty
* Category volatility

---

### 9. The Hard Part: Data Joining

Naive joins will destroy the dataset.

Wrong approach:

* Join on `product_id` only

This creates:

* Temporal leakage
* False attribution of trends

---

### 10. Correct Join Logic (Causal Alignment)

For each purchase:

1. Identify all prior trend exposures
2. Filter:

   * `trend_timestamp <= purchase_timestamp`
3. Select:

   * Most recent relevant trend
     OR
   * Aggregate exposure window

---

### 11. Example Causal Scenario

* Product trends at 10:00, 14:00, 20:00
* User purchases at 15:30

Valid signal:

* 14:00 trend

Invalid:

* 20:00 trend (future leakage)

---

### 12. Feature-Ready Dataset

Final output table:

`fact_instagram_purchase_outcomes`

**Schema Categories**

* Trend features
* Transaction features
* Customer features
* Product features
* Outcome label

---

### 13. Data Quality Rules

Non-negotiable constraints:

* Drop records with missing `product_id`
* Cap extreme engagement values (bot noise)
* Normalize sentiment across creators
* Enforce timestamp consistency

---

### 14. Failure Modes

#### 1. Temporal Leakage

Using future trend data
→ Model becomes unrealistically accurate

#### 2. Attribution Noise

Wrong trend linked to purchase
→ Signal dilution

#### 3. Missing Exposure Data

Assuming all purchases are influenced by trends
→ False positives

---

### 15. Unorthodox but High-Leverage Addition

**Negative Exposure Data**

Capture:

* Products seen but NOT purchased

Why:

* True learning requires contrast
* Without this, model only sees success cases

Tradeoff:

* Data volume explosion
* Requires session-level tracking

---

### 16. Definition of Done

* All data sources identified and documented
* Join logic defined with temporal constraints
* Feature-ready schema designed
* Data quality rules established
* Edge cases acknowledged

---

### 17. What This Enables

This sprint enables:

* Valid feature engineering
* Trustworthy modeling
* Causal interpretation

---

Bad data does not give wrong answers.
It gives **confidently wrong answers that look right**.
