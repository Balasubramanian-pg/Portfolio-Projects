## Sprint 1.2

**Instagram vs Wallet**
**Data Joining Strategy**

---

### 1. Objective

Design a joining strategy that preserves **causality, sequence, and signal integrity** across:

* Instagram exposure
* Purchase decision
* Return outcome

If this step is wrong, everything downstream becomes high-accuracy fiction.

---

### 2. Problem Reframing

This is not a join problem.
It is a **causal attribution problem**.

Naive thinking:

> “Join tables on product_id”

Correct thinking:

> “Which signals were available to the user at the moment of decision?”

---

### 3. Core Constraint: Time Direction

All joins must obey:

> **No data created after purchase can influence that purchase**

This single rule eliminates:

* Data leakage
* Inflated model performance
* False causal conclusions

---

### 4. Joining Layers

You are not doing one join. You are constructing layers:

1. **Exposure Attribution Layer**
2. **Purchase Context Layer**
3. **Outcome Alignment Layer**

Each has different rules.

---

### 5. Exposure Attribution (Hardest Part)

#### Problem

A product can trend multiple times.
A user may see multiple exposures.

Which one matters?

#### Strategy

For each purchase:

1. Filter all trends:

   * `trend_timestamp <= purchase_timestamp`

2. Choose attribution method:

**Option A: Last Touch (Baseline)**

* Select most recent trend before purchase

**Option B: Weighted Exposure (Better)**

* Aggregate multiple exposures:

  * Weight by recency
  * Weight by engagement

**Option C: Session-Based Attribution (Best but expensive)**

* Link exposure events within user session

---

### 6. SQL Pattern (Last-Touch Attribution)

```sql
WITH ranked_trends AS (
  SELECT
    p.order_id,
    t.trend_id,
    t.product_id,
    t.trend_timestamp,
    p.purchase_timestamp,
    ROW_NUMBER() OVER (
      PARTITION BY p.order_id
      ORDER BY t.trend_timestamp DESC
    ) AS rn
  FROM purchases p
  JOIN trends t
    ON p.product_id = t.product_id
   AND t.trend_timestamp <= p.purchase_timestamp
)
SELECT *
FROM ranked_trends
WHERE rn = 1;
```

This is the minimum viable causal join.

---

### 7. Multi-Exposure Aggregation (Better Signal)

Instead of picking one trend:

Create features like:

* `avg_velocity_last_24h`
* `max_velocity_last_6h`
* `num_exposures_last_12h`

This captures:

* Intensity
* Recency
* Repetition

---

### 8. Purchase Context Join

This is straightforward but still error-prone.

Join:

* transactions
* customer features
* product features

Key rule:
All features must exist **before purchase timestamp**

Common mistake:

* Using post-purchase aggregates

---

### 9. Outcome Alignment

Join returns to purchases using:

* `order_id`

Then derive:

* `return_flag`
* `regret_flag` (from Sprint 0 logic)

Important:
Do not leak:

* Return timestamp
* Future behavior

---

### 10. Final Join Pipeline

Conceptual flow:

1. Start with purchases
2. Attach exposure signals (time-filtered)
3. Attach customer + product context
4. Attach outcome labels

Output:
`fact_instagram_purchase_outcomes`

---

### 11. Failure Modes

#### 1. Future Leakage

Using trends after purchase

Effect:

* Unrealistically strong model performance

---

#### 2. Many-to-Many Explosion

Multiple trends × multiple purchases

Effect:

* Duplicate rows
* Biased learning

---

#### 3. Incorrect Attribution

Assigning irrelevant trend

Effect:

* Signal dilution

---

### 12. Validation Checks

You need hard tests, not assumptions:

**Test 1: Temporal Integrity**

* No trend_timestamp > purchase_timestamp

**Test 2: Row Uniqueness**

* One row per order_id

**Test 3: Distribution Check**

* Exposure features vary meaningfully across data

**Test 4: Sanity Slice**

* Compare TikTok-driven vs non-TikTok purchases

---

### 13. Unorthodox but High-Leverage Strategy

#### Counterfactual Join

Include:

* Products viewed but not purchased

Create dataset:

* exposure_without_purchase

Why:

* Enables contrast learning
* Prevents survivorship bias

Tradeoff:

* Data size explodes
* Requires session tracking

---

### 14. Design Tradeoffs

| Approach      | Accuracy | Complexity | Risk                      |
| ------------- | -------- | ---------- | ------------------------- |
| Last-touch    | Low      | Low        | Misses multi-exposure     |
| Weighted      | Medium   | Medium     | Feature engineering heavy |
| Session-based | High     | High       | Data availability         |

Start simple. Upgrade only if signal demands it.

---

### 15. Definition of Done

* Temporal join logic implemented
* Attribution method selected
* No leakage verified
* Dataset is one-row-per-purchase
* Validation checks passed

---

### 16. What This Enables

This step creates:

* Trustworthy training data
* Valid causal relationships
* Stable model behavior

---

Most pipelines fail here quietly.
They don’t crash. They just learn the wrong world.
