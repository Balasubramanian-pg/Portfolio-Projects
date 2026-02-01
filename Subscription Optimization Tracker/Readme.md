# Subscription Optimization Tracker — Project Bible

## Table of Contents

1. Executive Summary
2. Vision and Goals
3. Scope and Constraints
4. Key Stakeholders and Personas
5. High-Level Architecture
6. Data Model and Schemas
7. Integrations and APIs
8. Recurring Transaction Detection
9. Usage Tracking and Instrumentation
10. Recommendation Engine and ML Design
11. Dashboard and UX Specifications
12. Alerts, Notifications, and Automation
13. Security, Privacy, and Compliance
14. Business Model and Partnerships
15. Operational Plan: DevOps and Monitoring
16. Roadmap, Milestones, and Deliverables
17. Testing, QA, and Acceptance Criteria
18. Risk Assessment and Mitigations
19. Cost Estimates and Sizing
20. Appendix A: Example Code Snippets
21. Appendix B: API Contracts and Wireframes
22. Appendix C: Glossary
23. Next Steps

---

## 1. Executive Summary

The Subscription Optimization Tracker is a privacy-first platform that helps users discover, manage, and optimize recurring subscriptions and memberships across financial accounts, digital services, and physical services. The product's primary goals are to reduce wasted spend, simplify cancellations and plan changes, and surface actionable recommendations that result in measurable annual savings for users.

Core capabilities include:

* Aggregating transaction history from financial institutions to detect recurring charges
* Instrumenting app, web, and device usage to measure actual user engagement
* Analyzing cost versus utility with a hybrid rule-based and machine learning recommendation engine
* Automating routine tasks such as drafting cancellation messages, initiating opt-outs where supported, and surfacing retention offers
* Enforcing industry standard security and privacy controls, and supporting user rights under applicable regulations

This project bible documents the technical design, product requirements, data models, and implementation roadmap needed to deliver an enterprise-ready MVP and a path toward a full featured platform.

## 2. Vision and Goals

### Vision

To make subscription management effortless and transparent. Users regain control of their recurring spending with precise, context-aware suggestions and safe, auditable automation.

### High-level goals

* Save the average user at least 20% of avoidable subscription spend within 6 months of active use.
* Detect and label 95% of recurring charges in supported accounts within the first 90 days after integration.
* Keep user trust through robust privacy controls and minimal manual input.

### Key performance indicators (KPIs)

* Monthly active users (MAU)
* Average savings identified per user per year
* Percentage of recommendations accepted by users
* Time-to-detect for new recurring subscriptions
* False positive rate for cancellation suggestions

## 3. Scope and Constraints

### In scope for MVP

* Bank connectivity via mainstream bank data aggregators
* Basic recurring transaction detection (merchant + amount + cadence)
* Web and mobile usage SDKs for tracking app and website time-on-service
* Dashboards: account-level view, subscription ledger, cost vs usage heatmap
* Renewal reminders and price-change alerts
* Cancelation email draft generation

### Out of scope initially

* Direct cancellation APIs for every merchant
* Deep negotiated retention automation (beyond draft generation)
* Family account billing aggregation across all global billing systems
* Legal representation for disputes

### Constraints

* Must operate within the security and consent requirements of bank data providers
* Data retention and processing must be configurable per jurisdiction
* Cost of external data connectors may scale with number of active users

## 4. Key Stakeholders and Personas

### Stakeholders

* Product Owner: prioritizes experience and feature tradeoffs
* Engineering Lead: responsible for architecture and deployments
* Security and Privacy Officer: approves encryption, data handling, and consent flows
* Data Scientist: designs models for detection and personalization
* Partnerships Manager: negotiates with banks, gyms, and streaming services

### Primary personas

* Emma, the cost conscious professional: wants a low friction way to find unused subscriptions and cancel them
* Raj, the family planner: wants to optimize family plans and spot overlapping services
* Priya, the busy executive: relies on simple recommendations and one-click actions

## 5. High-Level Architecture

This section outlines components, data flow, and integrations.

### Components

* Ingestion Layer: connectors to bank data, card transaction feeds, and optional user-uploaded statements
* Usage Tracking Layer: mobile SDKs, a browser extension, and device integrations for fitness data
* Processing Layer: ETL and event-driven pipelines for transaction normalization, enrichment, and recurring detection
* ML Services: model training pipelines and prediction endpoints
* Application Layer: RESTful APIs, a dashboard frontend, and user action endpoints
* Automation Engine: workflows for reminders, drafts, and conditional automations
* Security & Compliance: key management, audit logging, consent records

### Data flow (simplified)

1. User connects bank account via a secure link flow
2. Ingestion pulls transactions to the processing layer
3. Transactions are normalized and enriched with merchant and category data
4. Recurring detection runs, producing subscription candidates with confidence scores
5. Usage trackers augment subscription candidates with usage signals
6. Recommendation engine scores candidates and generates actions
7. User dashboard receives recommendations; user acts or defers
8. Actions are logged and automations run if permitted

## 6. Data Model and Schemas

The data model focuses on time series transactions, subscription entities, user profiles, and consent records. Below are canonical schemas presented in simplified JSON schema style.

### 6.1 users

```json
{
  "user_id": "uuid",
  "email": "string",
  "created_at": "timestamp",
  "consents": {
    "bank_data": true,
    "usage_tracking": false
  },
  "country": "string",
  "timezone": "string"
}
```

### 6.2 accounts

```json
{
  "account_id": "uuid",
  "user_id": "uuid",
  "provider": "string",
  "mask": "string",
  "currency": "string",
  "last_synced": "timestamp"
}
```

### 6.3 transactions

```json
{
  "transaction_id": "uuid",
  "account_id": "uuid",
  "date": "date",
  "amount": "decimal",
  "merchant": "string",
  "category": "string",
  "raw_description": "string",
  "normalized_merchant": "string",
  "enrichment": {"location": "lat,lng","domain":"string"},
  "metadata": {"is_recurring_candidate": true}
}
```

### 6.4 subscriptions

```json
{
  "subscription_id": "uuid",
  "user_id": "uuid",
  "merchant": "string",
  "normalized_merchant": "string",
  "amount": "decimal",
  "currency":"string",
  "interval":"monthly|yearly|weekly|custom",
  "first_seen":"date",
  "last_seen":"date",
  "confidence_score":"float",
  "usage_metrics":{"last_30_days_usage_minutes": 0}
}
```

### 6.5 events and audit logs

```json
{
  "event_id":"uuid",
  "user_id":"uuid",
  "type":"string",
  "payload":{},
  "timestamp":"timestamp"
}
```

### Time-series storage

Use a time-series optimized extension when storing transaction time-series such as the `timescaledb` extension for PostgreSQL. Index transactional events by user, merchant, and date for fast rollups.

## 7. Integrations and APIs

This product depends on a combination of bank data aggregators, identity and consent SDKs, device APIs, and merchant-facing APIs. The integration layer should be modular so connectors can be added or swapped.

### Key third-party services used in this project

* entity["company","Plaid","financial data platform"]
* entity["company","Yodlee","financial data aggregator"]
* entity["company","Amazon Web Services","cloud provider"]
* entity["company","TimescaleDB","time-series database"]
* entity["company","Plotly","visualization library"]
* entity["organization","XGBoost","ml library"]
* entity["company","Netflix","streaming service"]
* entity["company","Fitbit","wearable vendor"]
* entity["company","Apple","consumer electronics company"]

Note: Each entity above is referenced once in this document for clarity. In the text that follows, these partners and technologies are referred to by plain name without additional entity wrappers.

### 7.1 Bank connectors

* Use provider SDKs to obtain tokenized access. The recommended flow is to host a secure backend that exchanges short lived link tokens with the aggregator SDK and persists provider tokens server side.
* Respect provider rate limits and webhook models. Support incremental updates to transaction history and incremental synchronization.

### 7.2 Usage SDKs

* Mobile: lightweight SDKs that record app session duration for apps and classify domains for webviews. Provide clear OS-level consent prompts and an opt-out option.
* Browser extension: optional, with strict least-privilege manifest, recording only time spent on domains identified as subscription experiences.
* Wearable and gym integrations: opt-in device syncs, e.g. step counts, GPS check-ins, or Gym API webhooks when available.

### 7.3 Merchant and Partner APIs

* Where merchants provide APIs for plan management or retention offers, create adapters to surface one-click actions. For most merchants, the solution will synthesize human readable messages and present them to the user for manual submission.

## 8. Recurring Transaction Detection

### 8.1 Detection goals

* Identify recurring transactions robustly across calendar drift, small amount variations, and currency differences.
* Provide a confidence score and the reasoning features that produced the classification.

### 8.2 Rule-based detection overview

A pragmatic rule-based detector works well as a first-pass and as a feature generator for ML.

Steps:

1. Group transactions by normalized merchant name and currency.
2. Cluster by approximate amount using bucketing to tolerate small variation.
3. Extract event_dates and compute pairwise intervals.
4. Evaluate regularity metrics such as median interval and variance.
5. Require at least three occurrences and a maximum allowed variance to qualify as recurring.

A sample pseudo-implementation is included below.

```python
from collections import defaultdict
from statistics import median, stdev

def is_regular(dates, max_variance_days=7):
    # dates are sorted datetime.date objects
    intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    if not intervals:
        return False
    med = median(intervals)
    # if only one interval, treat as regular if close to common cadence
    if len(intervals) == 1:
        return abs(intervals[0] - med) <= max_variance_days
    try:
        var = stdev(intervals)
    except Exception:
        var = 0
    return var <= max_variance_days


def detect_recurring(transactions):
    grouped = defaultdict(list)
    for t in transactions:
        key = (t['normalized_merchant'], round(float(t['amount']), 2), t['currency'])
        grouped[key].append(t['date'])
    candidates = []
    for key, dates in grouped.items():
        dates_sorted = sorted(dates)
        if len(dates_sorted) < 3:
            continue
        if is_regular(dates_sorted):
            candidates.append({'merchant': key[0], 'amount': key[1], 'dates': dates_sorted})
    return candidates
```

### 8.3 Handling edge cases

* Amount drift due to taxes, regional pricing, or small periodic changes. Use fuzzy bucketing and require a minimum occurrence count.
* Merchant name drift due to payment processors showing parent company names. Apply merchant normalization and enrichment.
* Trials and one-time promotional charges should be labeled separately by observing short-lived recurring patterns.

### 8.4 Enrichment

* Use merchant enrichment to map raw descriptions to canonical merchant and category. Use both aggregator-provided enrichment and custom mapping tables.

## 9. Usage Tracking and Instrumentation

### 9.1 Mobile SDK

* Capture session start and end timestamps for apps with explicit user consent.
* For streaming services, instrument player activity when possible to differentiate background playback from active watching.

### 9.2 Browser extension

* Record domain-level stay time and focus events. Respect privacy: do not record page content or keystrokes.

### 9.3 Physical service signals

* For gyms and paid memberships, ingest check-in data when available through partner APIs. If absent, provide a mechanism to upload proof of visits such as email confirmations.

### 9.4 Signal fusion

* Merge usage signals with transaction candidates to compute a usage-per-dollar metric.

Usage-per-dollar = total_active_minutes_in_period / (monthly_cost)

Define thresholds for under-utilization per subscription type.

## 10. Recommendation Engine and ML Design

### 10.1 Design principles

* Start rule-first, machine-learned next. Use simple deterministic rules for low-risk suggestions and ML to prioritize recommendations.
* Be transparent with confidence scores and explainable features.

### 10.2 Features

* Transaction frequency and variance
* Recent usage trend (last 30, 90, 365 days)
* Relative cost per unit of use compared to category peers
* User tolerance and historical acceptance signals
* Seasonality signals

### 10.3 Model selection

* Train a gradient boosting classifier such as XGBoost to predict whether a subscription is a candidate for cancellation or consolidation.
* Target label: user-accepted action (cancel, downgrade, keep).

Model lifecycle:

* Feature store: daily feature generation from transactional and usage data
* Training pipeline: periodic retrain with stratified sampling
* Evaluation: precision at top K, recall for true cancels, and calibration

### 10.4 Example scoring function

A simple scoring function for early stages:

score = w1 * normalized_usage_score + w2 * price_sensitivity_score + w3 * tenure_penalty

Adjust weights via A/B tests.

## 11. Dashboard and UX Specifications

### 11.1 Core views

* Overview: Aggregated monthly spend, subscriptions at a glance, potential savings
* Subscription Ledger: line items with status, confidence, last charge, usage, and recommended action
* Cost vs Usage Heatmap: subscription types on axes with sizing by spend
* Actions view: drafts, automation history, disputes

### 11.2 Interaction patterns

* Allow bulk actions with safeguards
* Provide clear undo flows for canceled or removed suggestions
* Show provenance for each recommendation: which data points triggered it

### 11.3 Accessibility and localization

* Support WCAG AA for web UI
* Localize currency, date formats, and privacy disclosures per region

## 12. Alerts, Notifications, and Automation

### 12.1 Alert types

* Renewal reminders: configurable, default 3 days before renewal
* Price increase alerts: based on moving average or explicit merchant notifications
* Usage anomaly alerts: sudden drop in usage for paid services

### 12.2 Automation examples

* Auto-snooze a recommendation after user defers for a user-defined period
* Auto-generate cancellation email draft and open in the user's mail client

### 12.3 Delivery channels

* In-app notifications, email digests, and optional push notifications

## 13. Security, Privacy, and Compliance

This product handles sensitive financial and behavioral data. Follow industry best practices.

### 13.1 Data encryption

* At rest: AES-256 for sensitive fields at storage
* In transit: TLS 1.2 minimum, TLS 1.3 preferred
* Key management: hardware backed keystore or managed KMS

### 13.2 Consent and user control

* Capture and log explicit consent for each data category
* Allow users to revoke consent and request deletion of personal data

### 13.3 Regulatory considerations

* Configure data residency and retention per user region
* Implement right to erasure and data portability features for GDPR and CCPA compliance

### 13.4 Anonymization and analytics

* Use pseudonymization for analytics datasets and remove direct identifiers
* Aggregate outputs for business reporting when possible

### 13.5 Audit and logging

* Immutable audit logs for security and compliance events
* Access controls and least privilege enforcement for staff

## 14. Business Model and Partnerships

### 14.1 Monetization options

* Freemium: core detection is free; premium features include negotiation assistant, family plans, and concierge cancellation
* Affiliate: earn referral fees for successful plan switches
* White-label: offer banks a co-branded product via an embeddable SDK or API

### 14.2 Partnership targets

* Financial aggregators and banks
* Streaming services and telecoms for retention offers
* Gym aggregators and fitness platforms for check-in data

## 15. Operational Plan: DevOps and Monitoring

### 15.1 Infrastructure

* Containerized microservices managed via Kubernetes for scaling
* Serverless event handlers for webhook processing and lightweight automations
* Data pipelines on managed PostgreSQL with TimescaleDB for time-series operations

### 15.2 Monitoring and observability

* Define SLOs for API latency and sync freshness
* Logs, traces, and metrics collected centrally and alerted upon

### 15.3 Backup and DR

* Daily incremental backups for transactional stores
* Quarterly DR testing plan

## 16. Roadmap, Milestones, and Deliverables

### Phase 0: Discovery

* Finalize legal and risk assessments
* Integrations feasibility study for target markets

### Q1: MVP

* Bank connector + transaction ingestion
* Rule-based recurring detector
* Basic dashboard and notification system
* Privacy and consent framework

### Q2

* Mobile SDK release and browser extension
* Usage signal fusion
* Savings calculations and simple recommendations

### Q3

* ML recommendation engine rollout
* Partner integrations for retention offers

### Q4

* White-label banking integrations
* Scale optimizations

## 17. Testing, QA, and Acceptance Criteria

### 17.1 Unit and integration testing

* 80% code coverage target for critical backend modules
* Contract tests for connectors and API endpoints

### 17.2 Data quality

* Monitor detection precision and false positive rates
* Validate enrichment mapping accuracy against a labeled dataset

### 17.3 User acceptance

* Pilot with beta users and collect qualitative feedback
* Track conversion and savings acceptance rates

## 18. Risk Assessment and Mitigations

### Top risks

* Connector instability due to third party API changes
* Privacy incidents from improper data usage
* False positives causing user frustration

### Mitigations

* Circuit breakers and adapter patterns for connectors
* Strong data governance, encryption, and least privilege
* Conservative default thresholds and user confirmation for critical actions

## 19. Cost Estimates and Sizing

Provide initial cost buckets and rough sizing. These values are illustrative and should be validated.

* Data aggregator fees: variable per user and per connector
* Cloud infra: compute for API servers and ML training, storage for time-series data
* Operational: monitoring, incident response, customer support

## 20. Appendix A: Example Code Snippets

This appendix contains illustrative snippets for common tasks.

### 20.1 Recurring detection (Python)

(see section 8 for the pseudo-implementation used in production)

### 20.2 Price change detection

```python
import statistics

def detect_price_change(history_amounts, threshold_pct=0.1):
    if len(history_amounts) < 2:
        return False
    prev_avg = statistics.mean(history_amounts[:-1])
    last = history_amounts[-1]
    return last > prev_avg * (1 + threshold_pct)
```

## 21. Appendix B: API Contracts and Wireframes

A separate API contract file should be maintained and version controlled. Wireframes for each dashboard view and the mobile experience should be created in Figma.

## 22. Appendix C: Glossary

* Ingestion: process to pull data from third party providers
* Normalization: mapping raw descriptions to canonical merchant names
* Enrichment: augmenting transaction records with metadata
* Candidate: a transaction group potentially representing a subscription

## 23. Next Steps

* Review this project bible with stakeholders and adjust priorities
* Begin connector sprint with one bank aggregator and one major streaming service
* Build a small labeled dataset for subscriptions to seed ML models

---

# Notes

This README is intended to be a living document. It contains implementation guidelines and reference code for engineers, product managers, and data scientists collaborating on the Subscription Optimization Tracker.
