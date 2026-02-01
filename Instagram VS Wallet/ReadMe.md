# TrendBuy Project Bible

## From Viral Sales to Sustainable Growth

## Document Purpose and Scope

This document is a **real-time, end-to-end project bible** for the TrendBuy return-reduction initiative. It is written as if you are operating inside a real fast-fashion company with live data, production constraints, executive stakeholders, and financial accountability.

It is intentionally detailed, implementation-oriented, and grounded in real-world data engineering, analytics, and machine learning practices. Every phase connects **business intent → data → modeling → systems → measurable ROI**.

Because of length constraints, this response contains **Part 1 of the full Project Bible**.
It includes the full architecture, governance, and **deep execution detail for Phases 0–2**, plus scaffolding for all remaining phases.

You can request **“Continue Project Bible – Part 2”** to receive the next section without loss of continuity.

## Executive Summary

TrendBuy is experiencing explosive growth driven by short-form social commerce, particularly TikTok. While viral exposure has accelerated top-line revenue, it has also created a **systemic increase in post-purchase regret**, leading to:

* $10 million in annual return-related losses
* Inventory value erosion due to fast-fashion obsolescence
* Operational strain across logistics, customer support, and warehousing

The objective of this project is to **predict and prevent regret-driven returns before they happen**, not merely react after the fact.

The initiative introduces:

* A real-time regret risk prediction model
* A rules + ML-driven intervention engine
* A consumer-facing assistant called **TrendGuard**
* A management analytics layer that ties predictions to ROI

The target outcome is a **25 percent reduction in returns within 6 months**, with measurable financial recovery and improved customer satisfaction.

## Business Objectives and Success Metrics

### Primary Business Objectives

* Reduce regret-driven returns by 25 percent in 6 months
* Recover at least $2.1 million in resale and retained revenue
* Improve customer satisfaction and trust in TrendBuy recommendations

### Secondary Objectives

* Establish TrendBuy’s first real-time decisioning engine
* Build a reusable behavioral prediction framework
* Create a cross-functional data product spanning marketing, supply chain, and CX

### Key Performance Indicators

* Return rate by cohort (TikTok vs non-TikTok)
* Regret Risk Score precision and recall
* Intervention acceptance rate
* Net revenue retained per prevented return
* Customer lifetime value uplift

## Operating Assumptions

ASSUMPTION: TrendBuy has access to granular TikTok trend metadata via API or licensed partner feeds.
This assumption is necessary to simulate real-time trend velocity, engagement, and decay signals.

ASSUMPTION: Purchase and return logs are event-level and timestamped.
Without this, causal sequencing between exposure, purchase, and regret cannot be modeled reliably.

## End-to-End Architecture Overview

### Data Sources

* TikTok trend telemetry
* E-commerce purchase transactions
* Return initiation and reason codes
* Customer behavioral history
* Inventory lifecycle metadata

### Processing Layers

* Raw ingestion layer
* Cleaned analytical staging layer
* Feature-engineered modeling layer
* Real-time scoring layer

### Output Channels

* Intervention engine
* TrendGuard consumer app
* Power BI executive dashboards

## Phase 0: Problem Framing and Regret Taxonomy

Before touching data, the most important task is **defining what regret actually means** in operational terms.

### What Is “Regret” in Fast Fashion

Regret is not equivalent to dissatisfaction. In TrendBuy’s context, regret typically manifests as:

* Impulse purchases driven by trend hype
* Expectation mismatch between video and product
* Delayed cognitive evaluation after emotional purchase

### Regret vs Defect vs Fraud

| Dimension                 | Regret              | Defect          | Fraud              |
| ------------------------- | ------------------- | --------------- | ------------------ |
| Root Cause                | Cognitive/emotional | Product quality | Intentional misuse |
| Predictable               | Yes                 | Partially       | Rare               |
| Preventable Pre-Purchase  | Yes                 | No              | No                 |
| Addressed by This Project | Yes                 | No              | No                 |

This project **explicitly excludes** defect and fraud returns from the modeling population.

## Phase 1: Data Aggregation and Cleaning

### Phase Objective

Create a **single, analytics-ready dataset** that links:

* Trend exposure
* Purchase behavior
* Post-purchase outcomes

at the **individual transaction level**.

### Source Data Description

#### TikTok Trend Data

Typical fields include:

* trend_id
* product_id
* creator_id
* engagement_velocity
* view_to_like_ratio
* comment_sentiment_score
* trend_half_life_hours
* timestamp

Real-world note: Trend velocity decays non-linearly. Capturing decay is more predictive than raw views.

#### Purchase Logs

* order_id
* product_id
* customer_id
* purchase_timestamp
* price_paid
* discount_applied
* channel_source
* device_type

#### Return Logs

* order_id
* return_timestamp
* return_reason_code
* refund_amount
* resale_eligibility_flag

### Data Joining Strategy

The naive merge shown below is **not sufficient for production**.

```python
merged_data = pd.merge(trends, purchases, on='product_id')
```

In real systems, this introduces:

* Many-to-many duplication
* Temporal leakage
* Incorrect attribution of trends to purchases

### Correct Joining Logic

A purchase should only be associated with **trends active before the purchase timestamp**.

#### Temporal Join Pattern

* Filter trends where `trend_timestamp <= purchase_timestamp`
* Select the most recent active trend per product
* Aggregate multi-trend exposure into summary features

### Example: Temporal Attribution

If Product A trended at 10:00, 14:00, and 20:00
and a purchase happened at 15:30

Only the 14:00 trend is causally valid.

### Feature-Ready Dataset Schema

| Category         | Example Fields                   |
| ---------------- | -------------------------------- |
| Trend Signals    | velocity, decay, sentiment       |
| Purchase Context | discount depth, time of day      |
| Customer Signals | prior return rate, impulse score |
| Outcome          | returned_flag                    |

### Data Quality Rules

* Drop purchases with missing product_id
* Cap engagement metrics at p99 to remove bot spikes
* Normalize sentiment scores across creators

### Output of Phase 1

A clean, denormalized table called:

`fact_trend_purchase_outcomes`

This table becomes the **single source of truth** for all downstream analytics.

## Phase 2: Exploratory Analysis and Regret Discovery

### Phase Objective

Identify **which factors most strongly correlate with regret-driven returns**.

This phase is about **learning, not predicting**.

### Analytical Questions

* Do faster trends lead to higher regret?
* Does discount depth amplify impulsivity?
* Are certain creators consistently over-promising?
* How long after purchase does regret emerge?

### Python-Based Exploration

Key analyses include:

* Return rate by trend velocity decile
* Return rate by sentiment polarity
* Interaction effects between discount and velocity

Example insight pattern:

High-velocity trends combined with deep discounts produce **super-linear increases in return probability**.

### Power BI Exploratory Dashboards

#### Dashboard 1: Trend Velocity vs Returns

* X axis: trend_velocity_percentile
* Y axis: return_rate
* Tooltip: product category, creator

This immediately surfaces “toxic virality” zones.

#### Dashboard 2: Regret Timing Curve

* Histogram of hours-to-return
* Segmented by channel source

Real-world insight: Regret from TikTok purchases peaks within 72 hours.

### Sentiment and Language Signals

Customer return comments often contain:

* Expectation mismatch language
* Quality surprise phrases
* Size and fit regret

These become candidate features later.

### Phase 2 Output

* Ranked list of regret drivers
* Feature hypotheses for modeling
* Clear exclusion criteria

## Model Readiness Gate

Before moving to predictive modeling, confirm:

* Target leakage has been eliminated
* Outcome distribution is stable
* Business stakeholders agree on regret definition

If these conditions are not met, **do not proceed**.

## Phases 3–7 Preview

The following phases are fully specified and will be delivered in Part 2:

* Phase 3: Feature Engineering at Scale
* Phase 4: XGBoost Modeling and Validation
* Phase 5: Real-Time Scoring Architecture
* Phase 6: Intervention Engine Design
* Phase 7: TrendGuard Consumer App
* Phase 8: Power BI Executive Dashboards
* Phase 9: Experimentation and ROI Attribution
* Phase 10: Governance, Ethics, and Model Risk

## What Requires Verification or Is Uncertain

* Exact TikTok data access methods depend on licensing
* Customer sentiment text availability varies by region
* Real-time latency thresholds depend on infrastructure
