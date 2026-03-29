## Sprint 3.2

**Instagram vs Wallet**
**Feature Engineering Principles**

---

### 1. Objective

Define the **rules that govern feature creation**, so the system learns from reality instead of accidentally cheating.

This is not about creativity.
It is about **discipline under temptation**.

---

### 2. First Principle: Temporal Integrity

> A feature can only use information available at or before the purchase moment.

Violation example:

* Using return rates updated after the purchase
* Using trend peaks that occur after purchase

Effect:

* Model becomes unrealistically accurate
* Fails in production

**Implementation Rule**
Every feature must have:

* `feature_timestamp <= purchase_timestamp`

---

### 3. Causality Over Correlation

Features must represent **causal pathways**, not just statistical patterns.

Bad feature:

* “Top 10 returned products”

Good feature:

* `size_fit_issue_rate`
* `trend_velocity_24h`

Reason:
The model should learn *why* regret happens, not memorize *where* it happened.

---

### 4. Stationarity Awareness

Features must behave consistently over time.

Problem:

* Trends change
* User behavior shifts
* Seasonal effects

Example:

* Holiday discounts inflate impulse behavior

**Rule**

* Use rolling windows (7d, 30d, 90d)
* Avoid lifetime aggregates

---

### 5. Granularity Discipline

Choose the correct level of detail.

Too coarse:

* Monthly averages → hide spikes

Too fine:

* Raw event logs → noisy

Correct:

* Time-windowed aggregates aligned to purchase

Example:

* `velocity_24h` instead of raw engagement stream

---

### 6. Signal-to-Noise Control

Not all data is signal.

Sources of noise:

* Bot-driven engagement spikes
* Outlier purchases
* Sparse features

**Rules**

* Cap extreme values (p99 winsorization)
* Remove low-frequency features
* Normalize across creators and categories

---

### 7. Feature Independence (Avoid Redundancy)

Do not flood the model with variations of the same signal.

Bad:

* `velocity_1h`, `velocity_2h`, `velocity_3h`, `velocity_4h`

Better:

* Select meaningful windows (e.g., 6h, 24h)

Why:

* Redundancy reduces model clarity
* Increases overfitting risk

---

### 8. Interaction Over Isolation

Most predictive power comes from **interactions**, not single features.

Examples:

* `velocity × discount`
* `prior_return_rate × trend_velocity`

Rule:
If two features logically interact in reality, encode that interaction.

---

### 9. Interpretability Constraint

Every feature must answer:

> Can a human understand and act on this?

Bad:

* Arbitrary embedding dimension

Good:

* `discount_pct`
* `hours_since_trend_peak`

Why:

* Features drive interventions
* Black-box features limit trust

---

### 10. Feature Stability vs Freshness Tradeoff

Two competing forces:

* Stability → reliable patterns
* Freshness → capture new trends

**Strategy**

* Core features: stable (customer behavior, product risk)
* Dynamic features: fresh (trend velocity, exposure)

Balance both.

---

### 11. Leakage Detection as a System

Do not rely on intuition.

**Checks**

* Time-based splits (train on past, test on future)
* Feature importance anomalies
* Unrealistic performance spikes

If AUC is suspiciously high, assume leakage first.

---

### 12. Missing Data Strategy

Missingness is not always bad.

Types:

* Random missing → impute
* Systematic missing → signal

Example:

* No exposure data → may indicate non-Instagram purchase

Rule:

* Create missing flags when meaningful

---

### 13. Feature Lifecycle Management

Features are not permanent.

Each feature should have:

* Creation logic
* Validation metrics
* Deprecation criteria

Remove features that:

* Add no predictive value
* Drift too much
* Cannot be computed reliably

---

### 14. Unorthodox but High-Leverage Principle

#### Negative Feature Engineering

Most systems only learn from purchases.

Add:

* **non-purchase exposure data**

Example features:

* `seen_not_purchased_flag`
* `exposure_without_conversion_rate`

Why:

* Defines decision boundary
* Prevents survivorship bias

Tradeoff:

* Data complexity increases significantly

---

### 15. Feature Testing Framework

Every feature must pass:

1. **Leakage Test**
2. **Distribution Test**
3. **Stability Test**
4. **Incremental Value Test**

If it fails any:

* Remove or redesign

---

### 16. Common Failure Modes

#### 1. Leakage Disguised as Insight

Model looks brilliant, fails in production

#### 2. Feature Explosion

Too many features, no real signal

#### 3. Static Thinking

Features don’t adapt to changing trends

---

### 17. Definition of Done

* Feature rules documented
* Temporal integrity enforced
* Leakage checks implemented
* Interaction strategy defined
* Feature validation framework ready

---

### 18. What This Enables

These principles ensure:

* Reliable model training
* Stable production behavior
* Trustworthy insights

---

Feature engineering is where you decide whether the model learns reality or memorizes accidents.
