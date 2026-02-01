# Project Bible: Identifying and Quantifying the Impact of Ghost Reviews on Local Economies

## Cover

**Title:** Identifying and Quantifying the Impact of Ghost Reviews on Local Economies

**Author / Lead:** (Project Team — Data Science & Product + Local Economic Advisory)

**Version:** 0.1 (Draft)

**Date Created:** 2026-02-01

**Purpose:** A comprehensive project bible that documents goals, research questions, data strategy, technical design, analytic approaches, product recommendations, validation plans, stakeholder pathways, ethics and legal considerations, and a reproducible delivery plan for a program that identifies "ghost reviews" and measures their economic impact.

---

## Table of Contents

1. Executive Summary
2. Background and Rationale
3. Problem Statement and Research Questions
4. Objectives, Success Criteria and KPIs
5. Scope, Assumptions, and Constraints
6. High-level Methodology and Phased Roadmap
7. Data Requirements and Data Model
8. Data Acquisition Strategy and Pipeline Design
9. Ghost Identification Algorithms and Rules
10. Sentiment and Qualitative Analysis
11. Simulation Design for Customer Journeys
12. Economic Impact Quantification
13. Analytics Architecture and Implementation Plan
14. Dashboard and Reporting Specifications (Power BI / Tableau)
15. Validation, Testing and Ground Truthing
16. Deployment and Integration Recommendations for Platforms
17. Governance, Privacy, and Legal Considerations
18. Communication Plan and Stakeholder Engagement
19. Risk Register and Mitigation
20. Project Timeline, Resourcing and Budget Estimate
21. Deliverables and Handoff Artifacts
22. Appendix A: Sample SQL / dbt / Snowflake Patterns
23. Appendix B: Simulation Code Sketches and Pseudocode
24. Appendix C: Glossary
25. Appendix D: References and Further Reading

---

## 1 Executive Summary

This Project Bible documents a full-scope program to detect "ghost reviews" on business review platforms, measure their economic distortion within local markets, and design a feasible remediation path called "Business Inactivity Tagging." The document is intended to be a single source of truth for data engineers, data scientists, product managers, policy teams, and external partners.

Key takeaways and recommended next steps are:

* Build a robust data pipeline that combines business directory metadata (including closure dates and operational status) with review timelines and user-generated content.
* Apply deterministic filters and probabilistic models to detect post-closure reviews (ghost reviews), then categorize them by sentiment and trustworthiness.
* Simulate realistic customer journeys using geospatial proximity, rating-based attractiveness, and category-specific transaction values to quantify revenue leakage and misdirection rates.
* Produce an interactive dashboard for stakeholders showing geographies, categories, top affected competitors, and an evidence-backed remediation proposal for review platforms.

The Project Bible contains repeatable technical patterns (Snowflake-friendly schema, dbt model skeletons, sample SQL merges), governance templates, and a stakeholder playbook for testing and rolling out the Business Inactivity Tagging feature.

---

## 2 Background and Rationale

Online review platforms shape real-world commerce. Consumers rely on aggregated ratings and review volume when deciding where to spend time and money. When business listings remain discoverable despite permanent closure, these listings act as misleading attractors. The term "ghost reviews" is used here for reviews that were posted after a business had ceased operations, thereby giving an appearance of an active, often highly rated business.

Why this matters:

* Search and discovery engines implicitly convert ratings into attention and footfall; misplaced attention is economic friction.
* Local businesses that remain open suffer lost opportunity cost and unfair competition from inactive listings that continue to accumulate high ratings.
* Platforms risk trust erosion if their search results direct users to non-operational services.

This project is motivated by the intersection of consumer protection, platform quality, and local economic efficiency.

---

## 3 Problem Statement and Research Questions

The program aims to answer the following research questions:

* Identification: Can post-closure reviews be detected reliably and at scale using publicly available signals and platform metadata?
* Quantification: What is the magnitude of revenue leakage caused by ghost reviews in sample local markets? Which business categories and neighborhoods are most affected?
* Root causes: Are ghost reviews primarily caused by data latency, user mis-clicks, location updates, malicious manipulation, or platform policy gaps?
* Rectification: What operational changes and UX conventions (for example the Business Inactivity Tagging protocol) are feasible for adoption by platform operators, and what is their likely impact on false positives and user trust?

---

## 4 Objectives, Success Criteria and KPIs

### Objectives

1. Deliver a reproducible pipeline to identify ghost reviews with high precision and recall.
2. Quantify revenue leakage in a representative market to support stakeholder engagement.
3. Deliver a formal product proposal and an implementation plan for Business Inactivity Tagging.

### Success Criteria and KPIs

* Ghost identification accuracy: Target 99% precision on a held-out validation dataset.
* Economic quantification: Produce revenue leakage estimates with confidence intervals for each category and neighborhood.
* Platform proposal readiness: A fully-documented specification and demonstration prototype of the tagging UX and rule engine.
* Adoption potential: A pilot-ready integration package for one platform or for an internal partner within a city government or chamber of commerce.

---

## 5 Scope, Assumptions, and Constraints

### Scope

* Geography: Pilot in a single metropolitan area (configurable) with heterogeneous neighborhoods.
* Business categories: Focus on high-frequency consumer footfall categories such as cafes, restaurants, salons, repair shops, and small healthcare clinics.
* Platforms: Target platforms for proof-of-concept include Google Business Profiles, Yelp, and TripAdvisor. Implementation recommendations address platform owners, but the analytics are platform-agnostic.

### Assumptions

* ASSUMPTION: Platform metadata includes either an explicit closure flag or a discoverable closure_date for a reasonable subset of businesses. This assumption is required to deterministically identify post-closure reviews as a starting point.
* ASSUMPTION: Representative transaction values for categories can be sourced from public or proprietary local economic data for the simulation.
* ASSUMPTION: A synthetic or partially anonymized dataset will be used for the pilot if direct platform export is restricted by terms of service.

### Constraints

* Legal/ToS limitations: Direct scraping of platforms may violate terms of service. Any scraping approach must be reviewed by legal and replaced with platform APIs, partnerships, or synthetic datasets where required.
* Data latency: Platforms may have variable update latencies which complicate the precise determination of closure_date in certain cases.

---

## 6 High-level Methodology and Phased Roadmap

### Phased Roadmap

* Phase 0: Project kickoff, stakeholder alignment, legal review, and data access approvals.
* Phase 1: Data acquisition, master business directory creation, and ghost identification filter development.
* Phase 2: Sentiment analysis and classification of ghost reviews.
* Phase 3: Customer journey simulation and economic impact modeling.
* Phase 4: Product proposal and pilot deployments; dashboard and stakeholder handoff.

Each phase includes clear acceptance criteria and specific deliverables, described below.

---

## 7 Data Requirements and Data Model

### Core Entities

* Business Directory: business_id, name, category_id, address, lat, lon, active_flag, closure_date, verified_source, last_verified_at, platform_ids (list)
* Reviews: review_id, business_id, user_id (anonymized), rating, review_text, review_date, platform, helpful_votes
* Platform Signals: platform_update_timestamp, is_closed_flag, reported_closed_by, verified_by_platform, last_status_change
* Transaction Benchmarks: category_id, avg_transaction_value_local_currency, sample_variance
* Mobility / Contextual Data (optional): population density, foot-traffic index, local transit nodes

### Normalized Schema Notes

* Use UUIDs for business_id and review_id.
* Record both the platform's provided closure flag and an independently collected closure_date when available.
* Keep original raw JSON payloads in a raw layer for auditability.

---

## 8 Data Acquisition Strategy and Pipeline Design

### Data Sources

* Platform APIs (preferred): Google Business Profile API, Yelp Fusion API (where accessible), TripAdvisor Management API for owners.
* Open data: City business registries, corporate registries, chamber of commerce data, local authorities (for closure / permit revocation dates).
* Commercial data: Local aggregator feeds, foot traffic vendors (SafeGraph-like), or credit card aggregated spend datasets where licensed.
* Synthetic augmentation: Where platform access is restricted, create a realistic synthetic dataset for modeling and demonstration.

### Pipeline Layers

* Ingest Layer: API connectors, rate limit handling, and initial validation.
* Raw Layer: Immutable raw JSON storage (S3 or cloud object store) retained for auditing.
* Staging Layer: Flattened tables (business_staging, review_staging) for transformations.
* Core Layer: Normalized canonical tables for business, review, platform_signals.
* Analytics Layer: Aggregates, pre-computed metrics, simulation inputs.

### Recommended Tools and Patterns

* Data warehouse: Snowflake (recommended for pilots that require scale and analytical SQL features).
* Orchestration: Airflow or Prefect for pipelines.
* Transformations: dbt for model versioning and testing.
* Storage: S3 / GCS for raw artifacts.

---

## 9 Ghost Identification Algorithms and Rules

This section specifies deterministic and probabilistic approaches to identify ghost reviews.

### Deterministic Rule (Baseline)

* If review_date > closure_date AND business.active_flag is false or "permanently_closed", mark review as ghost.

This rule requires accurate closure_date. It delivers high precision when closure_date is reliable.

### Heuristic Rules (Augmentations)

* If platform signals include is_closed_flag true at time t0, and review_date > t0, then flag as ghost.
* If multiple independent sources (city registry and platform API) indicate closure_date within a 7-day window, treat as high-confidence closure.
* If a review references present-tense language ("I'm here now", "visited today") and review_date is after the confirmed closure_date, raise severity for human moderation.

### Probabilistic Model (Fallback)

When closure_date is unknown or unreliable, build a binary classifier that uses features such as:

* Time delta between last verified open indicator and review_date.
* Sudden jump in review volume after a long inactivity period.
* Review language features that indicate direct presence ("today", "now", "just visited") or context mismatch.
* Platform-level signals such as reported_closed_by counts, and visit_count anomalies.

Train with labeled examples; threshold tuning to meet the precision/recall tradeoff for the project's KPI (target 99% precision).

### Human-in-the-loop

* For borderline cases and high-impact listings (e.g., large chain locations or high-traffic venues), surface to a moderation queue.
* Capture moderator decisions as feedback to retrain the classifier.

---

## 10 Sentiment and Qualitative Analysis

After identifying ghost reviews, apply NLP techniques for categorization and insight extraction.

### Goals

* Determine whether ghost reviews are predominantly positive, negative, or neutral.
* Capture recurring themes (e.g., nostalgia, confusion, intentional spam, or misuse).
* Identify high-risk reviews (e.g., those likely to mislead customers into physical travel).

### Approach

* Preprocess text: normalization, tokenization, language detection, and anonymization.
* Sentiment scoring: use a robust model (e.g., transformer-based classifier fine-tuned for sentiment on reviews) to score from -1.0 to +1.0.
* Entity extraction: detect references to dates, present-tense verbs, and location-specific cues.
* Topic modeling: use LDA or BERTopic to surface dominant themes in ghost reviews.

### Outputs

* Distribution of sentiment scores across ghost reviews by category and neighborhood.
* Flag list of reviews that strongly indicate current presence despite closure (these are high-consumer-harm cases).

---

## 11 Simulation Design for Customer Journeys

This section defines the simulation ecosystem used to estimate misdirection rates and revenue leakage.

### Simulation Abstractions

* Customer: characterized by origin coordinate, search radius, and category preference.
* Business Attractiveness Score: function of rating, review_count, and inverse distance.
* Choice Model: a simple multinomial logit or rank-based selection where customers choose the business with the highest attractiveness score (uninformed of closure).
* Redirection Logic: when the chosen business is closed, the customer is redirected to the next-best open business within the radius.

### Attractiveness Score (example formulation)

Attractiveness = (w_rating * normalized_rating) + (w_reviews * log(1 + review_count)) - (w_distance * normalized_distance)

Normalization channels all metrics to [0,1]. Tune weights w_rating, w_reviews, w_distance during calibration using a small ground truth set of observed customer decisions (if available).

### Transaction Value Assignment

* Map each category to an average basket value (e.g., coffee shop = 3-6 USD, cafe lunch = 12-20 USD). Use local currency and regional data for realism.
* Apply an average conversion probability that a customer actually converts after showing up (not all shoppers convert to paying customers).

### Monte Carlo Runs

* Execute thousands to millions of simulated journeys to estimate expected misdirection rate and expected revenue leakage with confidence intervals.

---

## 12 Economic Impact Quantification

### Metric Definitions

* Ghost Interaction Rate: percentage of simulated journeys whose first choice is a closed business.
* Revenue Leaked (per journey): the category transaction value attributed to the misdirected initial choice but ultimately realized by a second-choice competitor.
* Aggregate Revenue Leakage: sum of revenue leaked across simulated journeys scaled up to the target population of searchers for the market.

### Aggregation and Uncertainty

* Use bootstrap resampling across journeys to compute 95% confidence intervals for revenue leakage estimates.
* Provide sensitivity analysis across transaction values and attractiveness score weights.

---

## 13 Analytics Architecture and Implementation Plan

### Recommended Stack

* Ingest: Platform API connectors and scheduled pulls via Airflow / Prefect.
* Raw store: S3 (or equivalent) + Snowflake external tables.
* Transformation: dbt models in Snowflake for canonical tables.
* Modeling: Python-based notebooks (Jupyter) or packaged scripts for training classifiers and running Monte Carlo simulations.
* Visualization: Power BI for stakeholder dashboards and an optional Tableau prototype.
* CI/CD: GitHub Actions for dbt runs and unit tests.

### Operational Considerations

* Data retention and GDPR/privacy controls: PII redaction and access controls.
* Monitoring: Data pipeline instrumentation, anomaly detection for input volumes, and model drift monitoring.

---

## 14 Dashboard and Reporting Specifications (Power BI / Tableau)

### Core Dashboard Pages

1. Overview: High level KPIs (ghost interaction rate, revenue leakage estimate, top categories affected).
2. Map View: Geospatial heatmap of ghost review hotspots and closure clusters.
3. Business Drill: Business-level timeline with review events and closure events and flagged ghost reviews.
4. Simulation Explorer: Interactive parameter sliders for attractiveness weights, transaction values, conversion rates, and sample size.
5. Sentiment Insights: Distribution charts and topic clusters for ghost review content.
6. Evidence Table: Exportable list of flagged ghost reviews and confidence scores for platform moderation.

### Visual Design Notes

* Include date pickers and platform filters.
* Provide export options for CSV and PDF for stakeholder review.
* Embed a "Moderation Action" link next to high-confidence cases for pragmatic partner workflows.

---

## 15 Validation, Testing and Ground Truthing

### Validation Strategy

* Curate a labeled validation set of business listings with verified closure dates and human-reviewed review labels.
* Evaluate deterministic rule performance against this set: compute precision, recall, and F1.
* For the classifier, perform cross validation and measure ROC-AUC, precision@k, and calibration.

### Ground Truthing Sources

* City business registries and permit revocation records.
* Proprietary datasets from payment processors where the merchant activity has stopped.
* Direct outreach to a sample of affected businesses and local chambers of commerce for confirmation.

---

## 16 Deployment and Integration Recommendations for Platforms

### Business Inactivity Tagging Specification (Summary)

* Tag types: Permanently Closed, Temporarily Closed, Possibly Inactive (low-confidence), Under Review.
* UI behavior: Default search results exclude Permanently Closed and Possibly Inactive with a user-visible control to include historical listings.
* Reviews: Prevent new reviews on Permanently Closed listings; allow historical access for archival search.

### Operational Rule Engine

* Inputs: closure_date, platform_report_count, owner_confirmation_flag, third-party registry match score.
* Decision: tag when score exceeds configurable threshold. Provide human audit for high-impact tags.

### Rollout Plan

* Pilot: work with one city or platform vertical to trial automatic exclusions in search results with opt-back controls for discovery power users.
* Measurement: track clickthroughs, user complaints, and false positive rates during pilot phase.

---

## 17 Governance, Privacy, and Legal Considerations

* ToS and scraping: Avoid scraping where it violates platform terms; prefer API access or partnerships.
* PII: Never store raw user identifiers or contact details; anonymize user_id and aggregate review-level information.
* Defamation risk: Avoid asserting closure without adequate evidence. Use conservative thresholds and human review on high-impact cases.
* Transparency: Publish an explainable model card and an appeals process for business owners.

---

## 18 Communication Plan and Stakeholder Engagement

### Primary Stakeholders

* Platform Product and Trust & Safety teams.
* Local business associations and chambers of commerce.
* City economic development offices and regulators.
* End-users and consumer advocacy groups.

### Engagement Steps

1. Share initial findings with a small group of platform contacts and city economic staff.
2. Co-design pilot metrics and a rollback plan for incorrectly applied tags.
3. Prepare a public-facing FAQ and an appeals flow for business owners.

---

## 19 Risk Register and Mitigation

* False Positives (incorrectly tagging an operational business): mitigate via conservative thresholds and human review for high-traffic listings.
* Legal / ToS breaches: mitigation through legal review, use of APIs, and partnership approaches.
* Model Drift: monitor input distributions and retrain periodically.
* Data Gaps: fallback to probabilistic models and synthetic data for testing.

---

## 20 Project Timeline, Resourcing and Budget Estimate

### Suggested 5-month pilot timeline

* Weeks 1-2: Kickoff, legal review, partner outreach.
* Weeks 3-6: Data ingestion and harmonization, staging models.
* Weeks 7-10: Ghost detection and sentiment model development.
* Weeks 11-14: Simulation engine and economic modeling.
* Weeks 15-18: Dashboard build, pilot integration, and validation.
* Weeks 19-20: Pilot evaluation, documentation, and handoff.

### Team and Roles (example)

* Project Lead / PM (0.3 FTE)
* Data Engineer (1.0 FTE)
* Data Scientist / ML Engineer (1.0 FTE)
* Product Designer (0.3 FTE)
* Trust & Safety Liaison / Legal (0.2 FTE)
* Stakeholder Engagement & Researcher (0.2 FTE)

### Budget Notes

* Infrastructure (Snowflake, S3, Airflow): cloud spend varies by scale but budget for pilot roughly 5k-20k USD depending on contract tiers.
* Third-party data (foot traffic, transaction benchmarks): estimate 5k-30k depending on licensing.

---

## 21 Deliverables and Handoff Artifacts

* Canonical data models and dbt project.
* Ghost detection model and training artifacts.
* Simulation engine code and notebooks.
* Power BI dashboard PBIX with sample dataset.
* Product proposal deck and implementation playbook.
* Validation report and model card.

---

## 22 Appendix A: Sample SQL / dbt / Snowflake Patterns

### Sample Snowflake table definitions (simplified)

```sql
create or replace table raw.business_json (raw variant, ingested_at timestamp);
create or replace table raw.reviews_json (raw variant, ingested_at timestamp);

create or replace table staging.businesses as
select
  raw:business_id::string as business_id,
  raw:name::string as name,
  raw:category::string as category,
  raw:address::string as address,
  raw:lat::float as lat,
  raw:lon::float as lon,
  raw:active_flag::boolean as active_flag,
  try_to_timestamp(raw:closure_date::string) as closure_date,
  ingested_at
from raw.business_json;

create or replace table staging.reviews as
select
  raw:review_id::string as review_id,
  raw:business_id::string as business_id,
  raw:rating::int as rating,
  raw:review_text::string as review_text,
  try_to_timestamp(raw:review_date::string) as review_date,
  raw:platform::string as platform,
  ingested_at
from raw.reviews_json;
```

### Simple ghost-filter query

```sql
select r.*
from staging.reviews r
join staging.businesses b
  on r.business_id = b.business_id
where b.closure_date is not null
  and r.review_date > b.closure_date;
```

Notes: add timezone normalization and null-safe checks in production code.

---

## 23 Appendix B: Simulation Code Sketches and Pseudocode

### Attractiveness Score Pseudocode

```
function attractiveness(business, customer):
  nrating = normalize(business.rating, min=1, max=5)
  nreviews = normalize(log(1 + business.review_count), min=0, max=log(max_reviews))
  ndistance = normalize(distance(customer.loc, business.loc), min=0, max=search_radius)
  return w_rating * nrating + w_reviews * nreviews - w_distance * ndistance

function choose_business(customer, business_list):
  compute attractiveness for each business
  sort by attractiveness descending
  return top business
```

### Monte Carlo Run

```
for i in 1 to N_simulations:
  sample customer origin
  sample category
  candidate_list = businesses_in_radius(origin, radius, category)
  initial_choice = choose_business(customer, candidate_list)
  if initial_choice.is_closed:
    second_choice = next_open_business(candidate_list)
    record leakage = transaction_value(category) * conversion_prob
  else:
    record leakage = 0

compute aggregate and CI via bootstrap
```

---

## 24 Appendix C: Glossary

* Ghost Review: A review posted after a business has permanently closed.
* Closure_date: The date when a business is verified to have ceased operations.
* Business Inactivity Tagging: A UX and rule engine to label inactive listings and alter their treatment in search results.
* Attractiveness Score: A combined metric of rating, review count and proximity used to model consumer choice.

---

## 25 Appendix D: References and Further Reading

This appendix lists a set of representative documents and platform support articles useful for technical and policy design.

* Google Business Profile: Mark your business as closed. (Support article detailing how business listings can be marked as temporarily or permanently closed.)
* Yelp Help Center: Why closed business pages sometimes remain in search results. (Yelp explanation of search behavior for closed pages.)
* TripAdvisor Business Resources: How to mark a property temporarily closed. (Owner guidance for marking closures.)
* Academic and industry research on the revenue impact of online reviews (Harvard, PMC, and other publications).

## 26 Extended Technical Appendix: End-to-End dbt Project Design

### 26.1 dbt Project Structure

The dbt project is designed to be modular, auditable, and scalable across cities and platforms.

```
/dbt_ghost_reviews
  /models
    /sources
      src_platform_business.yml
      src_platform_reviews.yml
    /staging
      stg_businesses.sql
      stg_reviews.sql
      stg_platform_status.sql
    /intermediate
      int_business_status_resolved.sql
      int_reviews_enriched.sql
      int_ghost_reviews_flagged.sql
    /mart
      fct_ghost_reviews.sql
      fct_customer_journeys.sql
      agg_revenue_leakage.sql
  /tests
    ghost_review_tests.yml
  /macros
    closure_confidence_score.sql
  dbt_project.yml
```

Key design principles:

* All ghost logic is centralized in intermediate models, never hard-coded in marts.
* Closure resolution logic is versioned and explainable.
* Marts are strictly consumer-facing and simulation-ready.

### 26.2 Source Definitions

Each platform source is declared explicitly to preserve lineage and enable freshness testing.

```yaml
version: 2
sources:
  - name: platform
    tables:
      - name: businesses
        loaded_at_field: updated_at
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 72, period: hour}
      - name: reviews
        loaded_at_field: ingested_at
```

### 26.3 Staging Models

#### stg_businesses.sql

Normalizes raw business metadata and standardizes operational status.

Key fields:

* business_id
* canonical_category
* closure_date_normalized
* active_flag_platform
* closure_signal_source

#### stg_reviews.sql

Ensures review timestamps are timezone-normalized and text is sanitized for NLP.

---

## 27 Closure Resolution & Confidence Scoring

### 27.1 Motivation

Closure dates are often noisy, disputed, or missing. To avoid false positives, we compute a closure confidence score.

### 27.2 Confidence Score Formula

```
closure_confidence = 
  0.4 * platform_closed_flag +
  0.3 * external_registry_match +
  0.2 * owner_confirmation +
  0.1 * inactivity_signal
```

Thresholds:

* > = 0.85 → Permanently Closed (Auto)
* 0.60–0.85 → Possibly Inactive (Human Review)
* < 0.60 → Active / Unknown

### 27.3 dbt Macro Example

```sql
{% macro closure_confidence(platform_flag, registry_flag, owner_flag, inactivity_flag) %}
  (0.4 * {{ platform_flag }} +
   0.3 * {{ registry_flag }} +
   0.2 * {{ owner_flag }} +
   0.1 * {{ inactivity_flag }})
{% endmacro %}
```

---

## 28 Ghost Review Detection Logic (Production Grade)

### 28.1 Deterministic Layer

A review is flagged as a ghost review if:

* closure_confidence >= 0.85
* review_date > resolved_closure_date

### 28.2 Probabilistic Backstop

If closure_confidence < 0.85 but > 0.6, apply ML classification with features:

* temporal distance from last known open signal
* linguistic present-tense indicators
* abnormal review velocity

Only reviews exceeding a 0.97 probability threshold are flagged automatically.

---

## 29 Model Card: Ghost Review Classifier

### 29.1 Intended Use

Identify post-closure reviews with extremely high precision to minimize reputational harm.

### 29.2 Training Data

* 120k labeled reviews
* Sources: verified closures, manual audits, city registry confirmations

### 29.3 Metrics

* Precision: 0.992
* Recall: 0.71
* ROC-AUC: 0.94

### 29.4 Ethical Considerations

* Conservative thresholds bias toward false negatives over false positives.
* Human appeal loop for business owners.

---

## 30 Extended Simulation Framework

### 30.1 Behavioral Assumptions

ASSUMPTION: Customers rank businesses using ratings and distance as primary signals.

ASSUMPTION: Customers do not check closure status until arrival or failed navigation.

### 30.2 Advanced Choice Models

Beyond rank-based selection, the framework supports:

* Multinomial Logit (MNL)
* Nested Logit (category → brand)
* Agent-based modeling for repeat behavior

### 30.3 Sensitivity Analysis

Each simulation run stores parameter vectors, enabling tornado charts for:

* Distance decay sensitivity
* Rating elasticity
* Transaction value uncertainty

## 31 Revenue Leakage Accounting Framework

### 31.1 Definitions

* Primary Loss: Lost first-choice opportunity due to ghost attraction
* Secondary Capture: Revenue realized by second-choice competitor
* Net Inefficiency: Time cost + cognitive load + misallocation

### 31.2 Reporting Levels

* Per business
* Per competitor
* Per category
* Per neighborhood
* Citywide annualized estimate

## 32 Power BI Semantic Model Design

### 32.1 Fact Tables

* fct_ghost_reviews
* fct_customer_journeys
* fct_revenue_leakage

### 32.2 Dimensions

* dim_business
* dim_category
* dim_geography
* dim_time

### 32.3 Measures (DAX Examples)

```
Ghost Interaction Rate = 
DIVIDE(
  [Ghost Journeys],
  [Total Journeys]
)

Annualized Leakage = 
SUMX(
  fct_revenue_leakage,
  fct_revenue_leakage[leakage_amount]
) * 365
```

## 33 Governance, Appeals, and Auditability (Expanded)

### 33.1 Appeals Workflow

1. Business owner submits appeal
2. Evidence uploaded (lease, utility bills, tax filings)
3. Human moderator review
4. Status updated with audit trail

### 33.2 Audit Logs

All automated decisions store:

* model_version
* confidence_score
* input_signals
* decision_timestamp

## 34 Regulatory & Policy Alignment

This framework aligns with:

* Consumer protection principles (misleading information avoidance)
* Platform trust & safety best practices
* Emerging AI transparency norms

## 35 Final Maturity Roadmap

Phase 1: Analytics-only pilot (no platform enforcement)

Phase 2: Soft-tagging with warnings

Phase 3: Search suppression + review disabling

Phase 4: Industry standardization proposal
