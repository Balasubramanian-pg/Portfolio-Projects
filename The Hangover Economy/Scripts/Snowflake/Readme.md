# Snowflake Data Warehouse Schema and Task Orchestration Plan

**Project:** The Hangover Economy – Post-Party Purchase Analyzer
**Platform:** Snowflake
**Purpose:** Production-grade analytical backbone supporting segmentation, promotion optimization, and Power BI consumption


## 1. Design Principles and Architectural Goals

### Core Design Goals

* Enable **hour-level and basket-level analytics** at national scale.
* Support **incremental ingestion** and **idempotent processing**.
* Separate **raw, cleaned, and business-ready data** clearly.
* Minimize downstream BI logic by pushing transformations upstream.
* Maintain **auditability, reproducibility, and compliance**.

### Snowflake-Specific Principles

* Use **schema layering** instead of physical databases for cost control.
* Favor **ELT** over ETL, leveraging Snowflake compute.
* Use **Tasks + Streams** for incremental processing.
* Design facts at the **lowest useful grain**, aggregate later.
* Avoid over-normalization in marts intended for Power BI.


## 2. Environment and Database Layout

### Databases

| Database       | Purpose                                  |
| -------------- | ---------------------------------------- |
| `RAW_DB`       | Immutable raw ingested data              |
| `STAGING_DB`   | Cleaned, standardized, deduplicated data |
| `ANALYTICS_DB` | Star schema and business-ready marts     |
| `UTIL_DB`      | Logging, monitoring, metadata            |


### Schemas per Database

#### RAW_DB

* `POS_RAW`
* `LOYALTY_RAW`
* `SURVEY_RAW`
* `CATALOG_RAW`

#### STAGING_DB

* `POS_STG`
* `LOYALTY_STG`
* `SURVEY_STG`
* `DIM_STG`

#### ANALYTICS_DB

* `DIMENSIONS`
* `FACTS`
* `MARTS`

#### UTIL_DB

* `METADATA`
* `LOGS`


## 3. RAW Layer Schema Definitions

### 3.1 RAW_DB.POS_RAW.TRANSACTIONS_RAW

**Purpose:** Exact copy of incoming POS files.

```sql
CREATE TABLE RAW_DB.POS_RAW.TRANSACTIONS_RAW (
    load_timestamp TIMESTAMP,
    source_file_name STRING,
    row_number INTEGER,
    timestamp_raw STRING,
    store_id STRING,
    product_id STRING,
    price NUMBER(10,2),
    payment_method STRING,
    transaction_id STRING,
    user_id STRING
);
```

Rules:

* No updates or deletes.
* Retained for 24 months.
* Used only for replay or forensic audits.


### 3.2 RAW_DB.LOYALTY_RAW.USERS_RAW

```sql
CREATE TABLE RAW_DB.LOYALTY_RAW.USERS_RAW (
    load_timestamp TIMESTAMP,
    user_id STRING,
    age INTEGER,
    gender STRING,
    enrollment_date DATE
);
```


### 3.3 RAW_DB.SURVEY_RAW.RESPONSES_RAW

```sql
CREATE TABLE RAW_DB.SURVEY_RAW.RESPONSES_RAW (
    load_timestamp TIMESTAMP,
    survey_id STRING,
    user_id STRING,
    hangover_frequency INTEGER,
    top_purchase STRING,
    self_reported_spend NUMBER(10,2)
);
```


## 4. STAGING Layer Schema Definitions

### 4.1 STAGING_DB.POS_STG.TRANSACTIONS_CLEAN

**Purpose:** Cleaned, typed, deduplicated transactions.

```sql
CREATE TABLE STAGING_DB.POS_STG.TRANSACTIONS_CLEAN (
    transaction_id STRING,
    transaction_timestamp_utc TIMESTAMP,
    local_hour INTEGER,
    transaction_date DATE,
    store_id STRING,
    product_id STRING,
    price NUMBER(10,2),
    payment_method STRING,
    user_id STRING,
    is_weekend BOOLEAN,
    record_hash STRING,
    load_timestamp TIMESTAMP
);
```

Cleaning logic:

* Timestamp normalization.
* Duplicate removal using `record_hash`.
* Invalid prices filtered.
* Product_id standardized.


### 4.2 STAGING_DB.DIM_STG.PRODUCTS_CLEAN

```sql
CREATE TABLE STAGING_DB.DIM_STG.PRODUCTS_CLEAN (
    product_id STRING,
    product_name STRING,
    category STRING,
    sub_category STRING,
    hangover_tag STRING,
    base_price NUMBER(10,2),
    margin_pct NUMBER(5,2),
    effective_date DATE,
    expiry_date DATE
);
```


### 4.3 STAGING_DB.DIM_STG.STORES_CLEAN

```sql
CREATE TABLE STAGING_DB.DIM_STG.STORES_CLEAN (
    store_id STRING,
    region STRING,
    store_format STRING,
    opening_time TIME,
    closing_time TIME,
    latitude NUMBER(9,6),
    longitude NUMBER(9,6),
    effective_date DATE,
    expiry_date DATE
);
```


## 5. ANALYTICS Layer Star Schema

### 5.1 Dimension Tables

#### DIM_DATE

```sql
CREATE TABLE ANALYTICS_DB.DIMENSIONS.DIM_DATE (
    date_key INTEGER,
    calendar_date DATE,
    day_of_week INTEGER,
    day_name STRING,
    week_of_year INTEGER,
    month INTEGER,
    month_name STRING,
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);
```


#### DIM_PRODUCT

```sql
CREATE TABLE ANALYTICS_DB.DIMENSIONS.DIM_PRODUCT (
    product_key INTEGER AUTOINCREMENT,
    product_id STRING,
    product_name STRING,
    category STRING,
    sub_category STRING,
    hangover_tag STRING,
    margin_pct NUMBER(5,2)
);
```


#### DIM_STORE

```sql
CREATE TABLE ANALYTICS_DB.DIMENSIONS.DIM_STORE (
    store_key INTEGER AUTOINCREMENT,
    store_id STRING,
    region STRING,
    store_format STRING,
    latitude NUMBER(9,6),
    longitude NUMBER(9,6)
);
```


#### DIM_USER

```sql
CREATE TABLE ANALYTICS_DB.DIMENSIONS.DIM_USER (
    user_key INTEGER AUTOINCREMENT,
    user_id STRING,
    age_bucket STRING,
    gender STRING,
    loyalty_flag BOOLEAN
);
```


#### DIM_PROMO

```sql
CREATE TABLE ANALYTICS_DB.DIMENSIONS.DIM_PROMO (
    promo_key INTEGER AUTOINCREMENT,
    promo_name STRING,
    promo_type STRING,
    discount_pct NUMBER(5,2),
    start_date DATE,
    end_date DATE
);
```


### 5.2 Fact Tables

#### FACT_TRANSACTIONS

**Grain:** One row per product per transaction.

```sql
CREATE TABLE ANALYTICS_DB.FACTS.FACT_TRANSACTIONS (
    transaction_id STRING,
    date_key INTEGER,
    store_key INTEGER,
    product_key INTEGER,
    user_key INTEGER,
    promo_key INTEGER,
    local_hour INTEGER,
    quantity INTEGER,
    revenue NUMBER(12,2),
    is_post_party BOOLEAN,
    load_timestamp TIMESTAMP
);
```


#### FACT_BASKETS

**Grain:** One row per transaction.

```sql
CREATE TABLE ANALYTICS_DB.FACTS.FACT_BASKETS (
    transaction_id STRING,
    date_key INTEGER,
    store_key INTEGER,
    user_key INTEGER,
    local_hour INTEGER,
    total_items INTEGER,
    total_spend NUMBER(12,2),
    electrolyte_count INTEGER,
    pain_relief_count INTEGER,
    breakfast_count INTEGER,
    snack_count INTEGER,
    is_post_party BOOLEAN
);
```


#### FACT_PROMO_PERFORMANCE

**Grain:** Store, promo, week.

```sql
CREATE TABLE ANALYTICS_DB.FACTS.FACT_PROMO_PERFORMANCE (
    promo_key INTEGER,
    store_key INTEGER,
    week_start_date DATE,
    baseline_sales NUMBER(12,2),
    actual_sales NUMBER(12,2),
    incremental_sales NUMBER(12,2),
    roi NUMBER(10,4)
);
```


## 6. Business Mart Views (Power BI Ready)

### MART_POST_PARTY_HOURLY

```sql
CREATE VIEW ANALYTICS_DB.MARTS.MART_POST_PARTY_HOURLY AS
SELECT
    d.calendar_date,
    f.local_hour,
    s.region,
    SUM(f.revenue) AS revenue,
    COUNT(DISTINCT f.transaction_id) AS transactions
FROM ANALYTICS_DB.FACTS.FACT_TRANSACTIONS f
JOIN ANALYTICS_DB.DIMENSIONS.DIM_DATE d
    ON f.date_key = d.date_key
JOIN ANALYTICS_DB.DIMENSIONS.DIM_STORE s
    ON f.store_key = s.store_key
WHERE f.is_post_party = TRUE
GROUP BY 1,2,3;
```


## 7. Task Orchestration Overview

### Orchestration Philosophy

* **Tasks** for transformation
* **Streams** for incremental detection
* **One task per logical step**
* Downstream tasks depend on upstream completion


## 8. Streams Configuration

### Example Stream on Clean Transactions

```sql
CREATE OR REPLACE STREAM STAGING_DB.POS_STG.TRANSACTIONS_STREAM
ON TABLE STAGING_DB.POS_STG.TRANSACTIONS_CLEAN
APPEND_ONLY = TRUE;
```


## 9. Task Dependency Graph

### High-Level Flow

1. Raw load tasks
2. Staging clean tasks
3. Dimension build tasks
4. Fact build tasks
5. Mart refresh tasks
6. Logging and monitoring


## 10. Task Definitions

### 10.1 Task: Clean Transactions

```sql
CREATE OR REPLACE TASK STAGING_DB.POS_STG.TASK_CLEAN_TRANSACTIONS
WAREHOUSE = ETL_WH
SCHEDULE = 'USING CRON 0 * * * * UTC'
AS
INSERT INTO STAGING_DB.POS_STG.TRANSACTIONS_CLEAN
SELECT
    transaction_id,
    TO_TIMESTAMP_NTZ(timestamp_raw) AS transaction_timestamp_utc,
    HOUR(TO_TIMESTAMP_NTZ(timestamp_raw)) AS local_hour,
    CAST(timestamp_raw AS DATE) AS transaction_date,
    store_id,
    product_id,
    price,
    payment_method,
    user_id,
    DAYOFWEEK(timestamp_raw) IN (6,7) AS is_weekend,
    HASH(transaction_id, product_id, price) AS record_hash,
    CURRENT_TIMESTAMP
FROM RAW_DB.POS_RAW.TRANSACTIONS_RAW
WHERE transaction_id IS NOT NULL;
```


### 10.2 Task: Build Fact Transactions Incrementally

```sql
CREATE OR REPLACE TASK ANALYTICS_DB.FACTS.TASK_FACT_TRANSACTIONS
WAREHOUSE = ETL_WH
AFTER STAGING_DB.POS_STG.TASK_CLEAN_TRANSACTIONS
AS
INSERT INTO ANALYTICS_DB.FACTS.FACT_TRANSACTIONS
SELECT
    t.transaction_id,
    d.date_key,
    s.store_key,
    p.product_key,
    u.user_key,
    NULL AS promo_key,
    t.local_hour,
    1 AS quantity,
    t.price AS revenue,
    CASE
        WHEN t.local_hour BETWEEN 0 AND 4 THEN TRUE
        WHEN t.local_hour BETWEEN 7 AND 11 AND t.is_weekend THEN TRUE
        ELSE FALSE
    END AS is_post_party,
    CURRENT_TIMESTAMP
FROM STAGING_DB.POS_STG.TRANSACTIONS_STREAM t
JOIN ANALYTICS_DB.DIMENSIONS.DIM_DATE d
    ON t.transaction_date = d.calendar_date
JOIN ANALYTICS_DB.DIMENSIONS.DIM_STORE s
    ON t.store_id = s.store_id
JOIN ANALYTICS_DB.DIMENSIONS.DIM_PRODUCT p
    ON t.product_id = p.product_id
LEFT JOIN ANALYTICS_DB.DIMENSIONS.DIM_USER u
    ON t.user_id = u.user_id;
```


## 11. Error Handling and Monitoring

### Task Failure Logging

```sql
CREATE TABLE UTIL_DB.LOGS.TASK_FAILURE_LOG (
    task_name STRING,
    error_message STRING,
    error_timestamp TIMESTAMP
);
```

Use Snowflake task history views to populate this table nightly.


## 12. Security and Access Control

### Roles

* `RAW_READ_ONLY`
* `ANALYTICS_READ`
* `ETL_EXECUTE`
* `BI_CONSUMER`

### Row-Level Security

* Mask `user_id` using masking policies.
* Apply RLS in Power BI where required.


## 13. Cost Control and Performance Optimization

* Separate warehouses for ingestion, transformation, and BI.
* Use auto-suspend aggressively.
* Materialize marts only where latency matters.
* Avoid tasks with schedules under 15 minutes unless justified.


## 14. Validation and Reconciliation Checks

### Example

* Daily revenue reconciliation between RAW and FACT.
* Count of transactions per day must match within 0.5 percent tolerance.
* Post-party flag logic tested with sampled queries.


## 15. What This Enables

* Near real-time post-party insights.
* Reliable segmentation and promo attribution.
* Scalable experimentation framework.
* Portfolio-grade Snowflake implementation suitable for interviews or production pilots.


## Next Possible Expansions

* Feature store schema for ML models.
* Snowflake Cortex integration for text survey analysis.
* Dynamic data masking policies per region.
* CI/CD pipeline for Snowflake using GitHub Actions.

If you want, I can continue by creating:

* A **full DAG diagram described step by step**
* **Power BI semantic model mapping**
* Or **Snowflake cost and warehouse sizing estimates**

Tell me what you want next.