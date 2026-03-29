## Sprint 3.3

**Instagram vs Wallet**
**Example SQL: Create Normalized Feature Table**

---

### 1. Objective

Translate feature design into a **deterministic, production-ready SQL pipeline** that creates a reusable feature table.

This is where theory becomes executable.

---

### 2. Design Philosophy

* One row per `order_id`
* All features computed **as-of purchase timestamp**
* No joins that introduce duplication
* No future leakage

Output table becomes:

> **Single source of truth for modeling and scoring**

---

### 3. Target Table

**Table Name:**
`ml.feature_instagram_wallet_v1`

---

### 4. SQL Implementation

```sql
CREATE OR REPLACE TABLE ml.feature_instagram_wallet_v1 AS

WITH purchase_base AS (
    SELECT
        p.order_id,
        p.customer_id,
        p.product_id,
        p.purchase_timestamp,
        p.price_paid,
        p.list_price,
        p.device_type,
        p.channel_source,

        -- transaction features
        (p.list_price - p.price_paid) / NULLIF(p.list_price, 0) AS discount_pct,
        EXTRACT(HOUR FROM p.purchase_timestamp) AS purchase_hour

    FROM raw.purchases p
    WHERE p.product_id IS NOT NULL
),

-- =========================
-- Trend Attribution Layer
-- =========================
trend_ranked AS (
    SELECT
        p.order_id,
        t.trend_id,
        t.velocity_24h,
        t.half_life_hours,
        t.peak_timestamp,
        t.sentiment_score,
        t.trend_timestamp,

        ROW_NUMBER() OVER (
            PARTITION BY p.order_id
            ORDER BY t.trend_timestamp DESC
        ) AS rn

    FROM purchase_base p
    LEFT JOIN raw.trends t
        ON p.product_id = t.product_id
       AND t.trend_timestamp <= p.purchase_timestamp
),

trend_selected AS (
    SELECT
        order_id,
        trend_id,
        velocity_24h,
        half_life_hours,
        sentiment_score,
        peak_timestamp
    FROM trend_ranked
    WHERE rn = 1
),

-- =========================
-- Customer Aggregates
-- =========================
customer_features AS (
    SELECT
        customer_id,

        AVG(CASE WHEN returned_flag = 1 THEN 1 ELSE 0 END) AS prior_return_rate_90d,
        AVG(order_value) AS avg_order_value_90d,
        COUNT(*) AS purchase_count_90d

    FROM raw.customer_orders
    WHERE order_timestamp >= CURRENT_DATE - INTERVAL '90 DAY'
    GROUP BY customer_id
),

-- =========================
-- Product Features
-- =========================
product_features AS (
    SELECT
        product_id,
        category,
        AVG(CASE WHEN return_reason = 'fit' THEN 1 ELSE 0 END) AS size_fit_issue_rate,
        AVG(return_flag) AS baseline_return_rate
    FROM raw.product_returns
    GROUP BY product_id
),

-- =========================
-- Outcome Labels
-- =========================
return_labels AS (
    SELECT
        r.order_id,
        1 AS return_flag,
        r.return_timestamp,

        CASE
            WHEN r.return_reason IN ('defect', 'damaged', 'wrong_item') THEN 'defect'
            WHEN r.return_reason IN ('fraud_suspected') THEN 'fraud'
            ELSE 'regret'
        END AS return_type,

        CASE
            WHEN r.return_reason NOT IN ('defect', 'damaged', 'wrong_item', 'fraud_suspected')
                 AND r.return_timestamp <= p.purchase_timestamp + INTERVAL '7 DAY'
            THEN 1 ELSE 0
        END AS regret_flag

    FROM raw.returns r
    JOIN raw.purchases p
        ON r.order_id = p.order_id
)

-- =========================
-- Final Feature Table
-- =========================
SELECT
    pb.order_id,
    pb.customer_id,
    pb.product_id,
    pb.purchase_timestamp,

    -- Trend Features
    ts.trend_id,
    ts.velocity_24h AS trend_velocity_24h,
    ts.half_life_hours,
    ts.sentiment_score,
    EXTRACT(EPOCH FROM (pb.purchase_timestamp - ts.peak_timestamp)) / 3600 AS hours_since_trend_peak,

    -- Transaction Features
    pb.price_paid,
    pb.discount_pct,
    pb.device_type,
    pb.channel_source,
    pb.purchase_hour,

    -- Customer Features
    cf.prior_return_rate_90d,
    cf.avg_order_value_90d,
    cf.purchase_count_90d,

    -- Product Features
    pf.category,
    pf.size_fit_issue_rate,
    pf.baseline_return_rate,

    -- Interaction Features
    (ts.velocity_24h * pb.discount_pct) AS velocity_x_discount,
    (ts.velocity_24h * cf.prior_return_rate_90d) AS velocity_x_prior_return,

    -- Outcome Labels
    COALESCE(rl.return_flag, 0) AS return_flag,
    COALESCE(rl.regret_flag, 0) AS regret_flag,
    COALESCE(rl.return_type, 'none') AS return_type

FROM purchase_base pb

LEFT JOIN trend_selected ts
    ON pb.order_id = ts.order_id

LEFT JOIN customer_features cf
    ON pb.customer_id = cf.customer_id

LEFT JOIN product_features pf
    ON pb.product_id = pf.product_id

LEFT JOIN return_labels rl
    ON pb.order_id = rl.order_id;
```

---

### 5. Key Design Decisions

#### A. Last-Touch Attribution

* Simpler, stable baseline
* Upgrade later to weighted exposure

#### B. Time-Bounded Aggregates

* 90-day windows for customer behavior
* Prevents drift and leakage

#### C. Interaction Features in SQL

* Precomputed for consistency
* Avoid runtime computation

---

### 6. Critical Safeguards

* Trend join filtered by `<= purchase_timestamp`
* One row per `order_id` enforced via window function
* Null-safe divisions
* Labels derived without future leakage

---

### 7. Validation Queries

#### Check duplicates

```sql
SELECT order_id, COUNT(*)
FROM ml.feature_instagram_wallet_v1
GROUP BY order_id
HAVING COUNT(*) > 1;
```

#### Check leakage

```sql
SELECT *
FROM ml.feature_instagram_wallet_v1
WHERE hours_since_trend_peak < 0;
```

#### Distribution sanity

```sql
SELECT
    AVG(regret_flag),
    AVG(discount_pct),
    AVG(trend_velocity_24h)
FROM ml.feature_instagram_wallet_v1;
```

---

### 8. Failure Modes

#### 1. Many-to-Many Explosion

Fixed using `ROW_NUMBER()`

#### 2. Leakage via Trend Data

Prevented using timestamp filter

#### 3. Sparse Joins

Handled via LEFT JOIN + COALESCE

---

### 9. Unorthodox Extension

Add a parallel table:

`ml.feature_exposure_no_purchase_v1`

* Same schema
* No purchase
* Label = 0

Purpose:

* Learn decision boundary
* Improve model generalization

---

### 10. Definition of Done

* Feature table created
* No duplicates
* No leakage
* Features aligned with schema
* Ready for modeling

---

### 11. What This Enables

This table feeds:

* Model training
* Real-time scoring
* Analytics dashboards

---

This is the moment the system becomes real.
Everything before this was theory.
