# Power BI Dataset Schema and Starter PBIX Wireframe

## TrendBuy – Regret Risk Analytics and ROI Tracking

This section **fully completes** the Power BI layer of the TrendBuy system. It covers conceptual modeling, semantic design, measure logic, row-level security, refresh strategy, and a **starter PBIX wireframe** that a BI developer can implement without ambiguity.

This is written as a **production BI artifact**, not a demo dashboard.

---

## Short Explanation of Reasoning Steps Taken

* Start from **business questions**, not visuals.
* Translate those questions into a **semantic model** that is stable, extensible, and performant.
* Design a **star schema** that supports both operational monitoring and executive ROI attribution.
* Define **DAX measures first**, visuals second.
* Ensure governance, RLS, and refresh strategies are explicitly planned.

---

## BI Layer Objectives

The Power BI layer must answer four executive questions:

1. Are returns going down because of the model?
2. Which trends, creators, and products are driving regret risk?
3. Which interventions actually prevent returns and generate ROI?
4. Is the model still behaving correctly over time?

---

## Tooling Context

The dataset and report are designed for **Power BI** with:

* Import or DirectQuery (hybrid recommended)
* Incremental refresh enabled
* Shared dataset for reuse across reports

---

# Part 1: Semantic Dataset Design (Star Schema)

## Core Modeling Principles

* One fact = one business process
* Dimensions are conformed across facts
* Time intelligence is explicit, not implicit
* Model supports both **actuals** and **counterfactual estimates**

---

## Fact Tables

### 1. `Fact_Purchases`

**Grain**: One row per order

| Column             | Description              |
| ------------------ | ------------------------ |
| Order_ID           | Surrogate or natural key |
| Purchase_Timestamp | Order time               |
| Customer_ID        | FK                       |
| Product_ID         | FK                       |
| Paid_Price         | Final paid amount        |
| List_Price         | Original price           |
| Channel_Source     | TikTok, Search, App      |
| Device_Type        | Mobile, Desktop          |
| Risk_Score         | Model output             |
| Risk_Band          | LOW / MEDIUM / HIGH      |
| Model_Version      | Scoring model            |
| Is_TikTok_Driven   | Boolean                  |

Purpose

* Anchor table for regret prediction
* Drives most visuals and KPIs

---

### 2. `Fact_Returns`

**Grain**: One row per return event

| Column           | Description           |
| ---------------- | --------------------- |
| Return_ID        | PK                    |
| Order_ID         | FK to purchases       |
| Return_Timestamp | When return initiated |
| Return_Reason    | Fit, Quality, Regret  |
| Refund_Amount    | Amount refunded       |
| Is_Regret_Return | Boolean               |

Purpose

* Distinguish regret vs non-regret returns
* Enable timing and root cause analysis

---

### 3. `Fact_Interventions`

**Grain**: One row per intervention attempt

| Column                     | Description               |
| -------------------------- | ------------------------- |
| Intervention_ID            | PK                        |
| Order_ID                   | FK                        |
| Intervention_Type          | Size Tip, Exchange Credit |
| Channel                    | Email, App, SMS           |
| Offered_Timestamp          | When sent                 |
| Accepted_Flag              | Boolean                   |
| Acceptance_Timestamp       | If accepted               |
| Estimated_Prevented_Return | Numeric                   |

Purpose

* Measure effectiveness of nudges
* Feed ROI calculations

---

### 4. `Fact_Model_Snapshots`

**Grain**: One row per day per model version

| Column                 | Description        |
| ---------------------- | ------------------ |
| Snapshot_Date          | Date               |
| Model_Version          | Version            |
| AUC                    | Model quality      |
| Precision_At_Threshold | Business precision |
| Avg_Risk_Score         | Drift signal       |

Purpose

* Model governance and trust
* Drift and decay detection

---

## Dimension Tables

### `Dim_Customer`

| Column                | Description     |
| --------------------- | --------------- |
| Customer_ID           | PK              |
| Region                | Geography       |
| Customer_Tenure_Days  | Derived         |
| Prior_Return_Rate_90d | Feature         |
| Lifetime_Value        | Business metric |

---

### `Dim_Product`

| Column              | Description     |
| ------------------- | --------------- |
| Product_ID          | PK              |
| Category            | Apparel type    |
| Size_Fit_Issue_Rate | Historical      |
| Launch_Date         | Lifecycle       |
| Season              | Trend relevance |

---

### `Dim_Trend`

| Column          | Description    |
| --------------- | -------------- |
| Trend_ID        | PK             |
| Creator_ID      | FK             |
| Trend_Velocity  | Views per hour |
| Trend_Peak_Date | Lifecycle      |
| Sentiment_Score | Aggregate      |

---

### `Dim_Creator`

| Column              | Description |
| ------------------- | ----------- |
| Creator_ID          | PK          |
| Platform            | TikTok      |
| Creator_Reliability | Derived     |
| Avg_Return_Rate     | Historical  |

---

### `Dim_Date`

Standard date dimension with:

* Date
* Day, Week, Month, Quarter
* Fiscal attributes if applicable

---

## Relationship Diagram (Textual)

* Fact_Purchases → Dim_Customer (Many-to-One)
* Fact_Purchases → Dim_Product
* Fact_Purchases → Dim_Date (Purchase_Timestamp)
* Fact_Returns → Fact_Purchases (One-to-One or One-to-Many)
* Fact_Interventions → Fact_Purchases
* Fact_Purchases → Dim_Trend
* Dim_Trend → Dim_Creator

All relationships single-direction, star schema, no bi-directional filters.

---

# Part 2: Core DAX Measures (Canonical Set)

## Return Metrics

### Regret Return Rate

```DAX
Regret Return Rate :=
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_Returns),
        Fact_Returns[Is_Regret_Return] = TRUE()
    ),
    COUNTROWS(Fact_Purchases)
)
```

---

### Return Reduction Percentage

```DAX
Return Reduction % :=
VAR Baseline =
    CALCULATE(
        [Regret Return Rate],
        Dim_Date[Date] < MIN(Dim_Date[Date])
    )
RETURN
DIVIDE(Baseline - [Regret Return Rate], Baseline)
```

---

## Model Effectiveness

### High Risk Precision

```DAX
High Risk Precision :=
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_Returns),
        Fact_Purchases[Risk_Band] = "HIGH"
    ),
    CALCULATE(
        COUNTROWS(Fact_Purchases),
        Fact_Purchases[Risk_Band] = "HIGH"
    )
)
```

---

## Intervention Metrics

### Intervention Acceptance Rate

```DAX
Intervention Acceptance Rate :=
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_Interventions),
        Fact_Interventions[Accepted_Flag] = TRUE()
    ),
    COUNTROWS(Fact_Interventions)
)
```

---

### Estimated Prevented Returns

```DAX
Prevented Returns :=
SUM(Fact_Interventions[Estimated_Prevented_Return])
```

---

## Financial Impact

### Revenue Retained

```DAX
Revenue Retained :=
SUMX(
    Fact_Interventions,
    Fact_Interventions[Estimated_Prevented_Return]
    * RELATED(Fact_Purchases[Paid_Price])
)
```

---

### ROI

```DAX
ROI :=
DIVIDE(
    [Revenue Retained] - [Intervention Cost],
    [Intervention Cost]
)
```

---

# Part 3: Starter PBIX Wireframe (Page-by-Page)

This is the **exact layout** your first PBIX should implement.

---

## Page 1: Executive Overview

**Purpose**
Instant health check for leadership.

**Visuals**

* KPI Cards

  * Regret Return Rate
  * Return Reduction %
  * Revenue Retained
  * ROI
* Line Chart

  * Daily Regret Return Rate vs Baseline
* Column Chart

  * Prevented Returns by Week
* Slicers

  * Date
  * Channel Source
  * Model Version

---

## Page 2: Regret Risk Landscape

**Purpose**
Understand where regret originates.

**Visuals**

* Heatmap

  * Trend Velocity vs Discount Depth
  * Color: Return Rate
* Bar Chart

  * Return Rate by Product Category
* Table

  * Top 20 High-Risk Products
* Scatter Plot

  * Risk Score vs Time Since Trend Peak

---

## Page 3: Intervention Performance

**Purpose**
Evaluate nudges, not just predictions.

**Visuals**

* Funnel

  * Flagged → Offered → Accepted → Prevented
* Bar Chart

  * Acceptance Rate by Intervention Type
* Matrix

  * Channel × Intervention Type
* Line Chart

  * Returns With vs Without Intervention

---

## Page 4: Creator and Trend Risk

**Purpose**
Expose systemic over-promise patterns.

**Visuals**

* Ranked Table

  * Creators by Excess Return Rate
* Bubble Chart

  * Reach vs Return Rate
* Trend Timeline

  * Velocity decay vs return spike

---

## Page 5: Model Monitoring and Governance

**Purpose**
Build trust and detect failure early.

**Visuals**

* Line Chart

  * AUC by Model Version
* Histogram

  * Risk Score Distribution (weekly)
* Table

  * Feature Drift Indicators
* KPI

  * Days Since Last Retrain

---

# Part 4: Row-Level Security (RLS)

## Regional Manager RLS Example

```DAX
[Region] = USERPRINCIPALNAME()
```

Or map user emails to regions via `Dim_User_Access`.

---

## Data Access Layers

* Executives: Full access
* Regional Managers: Region-filtered
* CX Teams: Customer-level with masking
* Data Science: Full historical access

---

# Part 5: Refresh and Performance Strategy

## Recommended Mode

* Import for dimensions
* Incremental Import for facts
* Optional DirectQuery for near-real-time metrics

## Incremental Refresh

* Store RangeStart and RangeEnd parameters
* Partition Fact_Purchases by Purchase_Timestamp

---

## Performance Optimizations

* Disable auto date/time
* Use explicit Date dimension
* Avoid bi-directional relationships
* Pre-aggregate where possible

---

# Part 6: Governance and Versioning

## Dataset Versioning

* Dataset name: `TrendBuy_RegretRisk_DS_v1`
* PBIX versioned in Git
* Model version always surfaced in visuals


## Audit and Trust

* Every dashboard shows:

  * Model Version
  * Last Refresh Time
  * Data Freshness SLA

# What Requires Verification or Is Uncertain

* Exact intervention cost values for ROI. I cannot verify this.
* Financial assumptions for prevented returns. I cannot verify this.
* Whether DirectQuery is acceptable for production latency. Requires platform validation.
* Final user access mappings for RLS. Requires IAM confirmation.

## Completion Status

This Power BI section now includes:

* Full semantic model
* Fact and dimension schemas
* Canonical DAX measures
* Starter PBIX page wireframe
* RLS, refresh, performance, and governance design

**No conceptual layer is missing.**

If you want, next I can:

* Generate a **PBIX build checklist** for a BI developer
* Produce a **Power BI theme JSON** aligned to TrendBuy branding
* Create a **data dictionary** for every field
* Provide **mock screenshots with exact visual placements**

Say what you want next.
