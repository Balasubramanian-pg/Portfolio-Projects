# Production-ready `feature_trendbuy_v1` SQL templates for Snowflake

Below you will find a complete, production-ready set of Snowflake SQL artifacts to build, maintain, and serve the `feature_trendbuy_v1` feature table for TrendBuy. This includes staging best-practices, change-data-capture with Snowflake Streams, automated Tasks, stored procedures for incremental merges, backfill scripts, clustering recommendations, data-quality checks, and serving queries. Where appropriate I cite Snowflake documentation for Streams, Tasks, materialized artifacts, and clustering. TikTok is referenced as the trend source in examples.

Read the short reasoning summary before the templates so you know why each piece exists and how they work together.

## Short, concise explanation of reasoning steps taken

* Identify the minimal end-to-end pieces needed to produce reliable, low-latency features: raw staging, CDC capture, transformation logic, feature materialization, serving endpoint, monitoring and rollback.
* Use Snowflake Streams to capture inserts/updates on ingestion tables, and Tasks to schedule or trigger incremental processing. This keeps compute usage efficient and supports near real-time updates. ([Snowflake][1]).
* Use MERGE-based upserts into a canonical feature table so features remain idempotent and auditable.
* Add clustering keys and retention policies tuned for common query patterns to optimize micro-partition pruning and cost. ([Snowflake][2]).
* Provide backfill patterns that run in controlled batches, separate from streaming Tasks, to avoid contention.
* Provide data quality checks and playbooks to detect and react to drift and pipeline failures.

## High-level object map

* Database / Schemas

  * `TRENDBUY_RAW` - ingestion staging area for raw feeds
  * `TRENDBUY_STG` - normalized staging and enriched staging tables
  * `TRENDBUY_MART` - materialized feature tables and marts
  * `TRENDBUY_META` - streams, tasks, logs, audit
* Tables and artifacts

  * `raw.tiktok_events` (external stage or pipe into table)
  * `stg.purchases` and `stg.returns`
  * `stg.trends_at_event` (preprocessed trends attributed to times)
  * `meta.purchases_stream`, `meta.trends_stream`
  * `mart.feature_trendbuy_v1` (canonical feature table)
  * `meta.feature_update_task` (task to process CDC)
  * Stored procedure `meta.sp_process_feature_updates`

## Assumptions to keep in mind

* ASSUMPTION: TikTok trend feed has been landed to `raw.tiktok_events` via Snowpipe or external ingestion and includes `product_id`, `trend_timestamp`, and velocity metrics.
* ASSUMPTION: Purchase and returns are captured in `stg.purchases` and `stg.returns` with event-level timestamps and identifiers.
* If any of the above assumptions are false, adjust source table names and ingestion patterns accordingly.

## Important Snowflake concepts used and authoritative references

* Streams record change deltas for tables and are central to CDC in Snowflake. ([Snowflake][1])
* Tasks run SQL or stored procedures and can be scheduled or triggered by stream activity. ([Snowflake][3])
* Clustering keys and micro-partition pruning improve query performance for large fact tables. ([Snowflake][2])
* Materialized views and dynamic tables are available alternatives for specific caching scenarios; use only if they match SLA and edition constraints. ([Snowflake][4])

# Part A: Staging and CDC setup

## 1. Create staging schemas and raw tables

Use a separate raw schema to hold raw ingested data. Keep raw data immutable.

```sql
CREATE OR REPLACE DATABASE trendbuy;
CREATE OR REPLACE SCHEMA trendbuy_raw;
CREATE OR REPLACE SCHEMA trendbuy_stg;
CREATE OR REPLACE SCHEMA trendbuy_mart;
CREATE OR REPLACE SCHEMA trendbuy_meta;
```

Create raw tables. These are simple landing tables that Snowpipe or batch jobs populate.

```sql
CREATE OR REPLACE TABLE trendbuy_raw.tiktok_events (
  event_id          VARCHAR,
  product_id        VARCHAR,
  creator_id        VARCHAR,
  trend_timestamp   TIMESTAMP_NTZ,
  views             NUMBER,
  likes             NUMBER,
  comments          NUMBER,
  velocity_1h       NUMBER,
  velocity_24h      NUMBER,
  sentiment_score   FLOAT,
  raw_payload       VARIANT,
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE trendbuy_raw.raw_purchases (
  order_id          VARCHAR,
  product_id        VARCHAR,
  customer_id       VARCHAR,
  purchase_timestamp TIMESTAMP_NTZ,
  paid_price        NUMBER(12,2),
  list_price        NUMBER(12,2),
  discount_code     VARCHAR,
  device_type       VARCHAR,
  channel_source    VARCHAR,
  raw_payload       VARIANT,
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE trendbuy_raw.raw_returns (
  return_id         VARCHAR,
  order_id          VARCHAR,
  product_id        VARCHAR,
  customer_id       VARCHAR,
  return_timestamp  TIMESTAMP_NTZ,
  return_reason     VARCHAR,
  refund_amount     NUMBER(12,2),
  raw_payload       VARIANT,
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

## 2. Normalize to staging tables

Design normalized staging tables that the rest of the pipeline will use. Normalization simplifies stream definitions.

```sql
CREATE OR REPLACE TABLE trendbuy_stg.trends (
  trend_id          VARCHAR,
  product_id        VARCHAR,
  creator_id        VARCHAR,
  trend_timestamp   TIMESTAMP_NTZ,
  velocity_1h       NUMBER,
  velocity_24h      NUMBER,
  sentiment_score   FLOAT,
  trend_peak_ts     TIMESTAMP_NTZ,
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE trendbuy_stg.purchases (
  order_id          VARCHAR PRIMARY KEY,
  product_id        VARCHAR,
  customer_id       VARCHAR,
  purchase_timestamp TIMESTAMP_NTZ,
  paid_price        NUMBER(12,2),
  list_price        NUMBER(12,2),
  device_type       VARCHAR,
  channel_source    VARCHAR,
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE trendbuy_stg.returns (
  return_id         VARCHAR PRIMARY KEY,
  order_id          VARCHAR,
  product_id        VARCHAR,
  customer_id       VARCHAR,
  return_timestamp  TIMESTAMP_NTZ,
  return_reason     VARCHAR,
  refund_amount     NUMBER(12,2),
  loaded_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

Normalization note

* Keep `trend_peak_ts` in the trends table computed by your trend processor. The later feature attribution step will join trends effective at or before the purchase timestamp.

## 3. Create Streams on staging tables for CDC

Create Snowflake Streams for the staging tables to capture INSERT/UPDATE/DELETE deltas.

```sql
CREATE OR REPLACE STREAM trendbuy_meta.stream_purchases
  ON TABLE trendbuy_stg.purchases
  APPEND_ONLY = FALSE
  SHOW_INITIAL_ROWS = FALSE;

CREATE OR REPLACE STREAM trendbuy_meta.stream_trends
  ON TABLE trendbuy_stg.trends
  APPEND_ONLY = FALSE
  SHOW_INITIAL_ROWS = FALSE;

CREATE OR REPLACE STREAM trendbuy_meta.stream_returns
  ON TABLE trendbuy_stg.returns
  APPEND_ONLY = FALSE
  SHOW_INITIAL_ROWS = FALSE;
```

Operational note

* `APPEND_ONLY = FALSE` tracks updates and deletes as well as inserts. Use `APPEND_ONLY = TRUE` only if the source genuinely only inserts.

Reference for streams usage: Snowflake Streams documentation. ([Snowflake][5])

# Part B: Feature table design

## 1. Feature table schema

Design `feature_trendbuy_v1` as a denormalized, append-or-update table keyed by `order_id`. Include metadata for lineage and explainability.

```sql
CREATE OR REPLACE TABLE trendbuy_mart.feature_trendbuy_v1 (
  order_id                  VARCHAR PRIMARY KEY,
  customer_id               VARCHAR,
  product_id                VARCHAR,
  purchase_timestamp        TIMESTAMP_NTZ,
  risk_label                BOOLEAN,        -- returned within X days (for training backfills)
  risk_score                FLOAT,          -- model score if available, else null
  feature_discount_pct      FLOAT,
  feature_velocity_24h      FLOAT,
  feature_trend_half_life_h FLOAT,
  feature_hours_since_trend_peak FLOAT,
  feature_creator_reliability FLOAT,
  feature_cust_prior_return_rate_90d FLOAT,
  feature_cust_avg_order_value_90d FLOAT,
  feature_prod_size_fit_rate FLOAT,
  feature_category          VARCHAR,
  feature_device_type       VARCHAR,
  feature_text_sentiment    FLOAT,
  top_shap_contrib_1        VARCHAR,
  top_shap_contrib_2        VARCHAR,
  top_shap_contrib_3        VARCHAR,
  model_version             VARCHAR,
  updated_at                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  created_at                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY (purchase_timestamp, product_id);
```

Clustering rationale

* Cluster by `purchase_timestamp` and `product_id` to optimize common time-range queries and product-level lookups. Micro-partition and clustering guidance from Snowflake docs. ([Snowflake][2])

## 2. Feature naming conventions and types

* Prefix features with `feature_` to separate from metadata.
* Use stable numeric types for model features (FLOAT).
* Keep textual explainability in `top_shap_contrib_*` with friendly user mappings.

# Part C: Incremental processing stored procedure and Task

The following stored procedure consumes Stream deltas and merges computed features into `feature_trendbuy_v1`. Use Snowflake Scripting or a Python stored procedure when logic needs Snowpark.

Below is an example stored procedure in Snowflake Scripting (SQL) that:

* Reads new purchase rows from `stream_purchases`.
* Joins to the latest applicable trend rows (trend_timestamp <= purchase_timestamp).
* Computes the derived features (discount_pct, hours_since_trend_peak, etc).
* MERGEs upsert into the feature table.
* Records processing metadata into `meta.feature_process_log`.

### 1. Create processing log table

```sql
CREATE OR REPLACE TABLE trendbuy_meta.feature_process_log (
  process_id      VARCHAR DEFAULT UUID_STRING(),
  started_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  finished_at     TIMESTAMP_NTZ,
  processed_orders NUMBER,
  note            VARCHAR
);
```

### 2. Stored procedure: `sp_process_feature_updates`

```sql
CREATE OR REPLACE PROCEDURE trendbuy_meta.sp_process_feature_updates()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  v_processed INTEGER DEFAULT 0;
  v_started TIMESTAMP_NTZ := CURRENT_TIMESTAMP();
BEGIN
  -- Insert a log row start
  INSERT INTO trendbuy_meta.feature_process_log(started_at) VALUES (v_started);

  -- Transform and merge from the purchases stream
  MERGE INTO trendbuy_mart.feature_trendbuy_v1 tgt
  USING
  (
    SELECT
      p.order_id,
      p.customer_id,
      p.product_id,
      p.purchase_timestamp,
      CASE WHEN p.list_price IS NULL OR p.list_price = 0 THEN 0
           ELSE (p.list_price - p.paid_price) / p.list_price END AS discount_pct,
      t.velocity_24h,
      t.sentiment_score,
      DATEDIFF('hour', t.trend_peak_ts, p.purchase_timestamp) AS hours_since_trend_peak,
      -- Example lookup of creator reliability. Assume table exists:
      cr.creator_reliability,
      cu.prior_return_rate_90d,
      cu.avg_order_value_90d,
      pr.size_fit_issue_rate,
      p.device_type,
      -- shims for explainability fields, set to placeholders
      NULL::VARCHAR as top_shap_contrib_1,
      NULL::VARCHAR as top_shap_contrib_2,
      NULL::VARCHAR as top_shap_contrib_3,
      NULL::VARCHAR as model_version
    FROM trendbuy_meta.stream_purchases sp
    JOIN trendbuy_stg.purchases p
      ON p.order_id = sp.ORDER_ID
    LEFT JOIN LATERAL
    (
      SELECT *
      FROM trendbuy_stg.trends tt
      WHERE tt.product_id = p.product_id
        AND tt.trend_timestamp <= p.purchase_timestamp
      ORDER BY tt.trend_timestamp DESC
      LIMIT 1
    ) t
      ON TRUE
    LEFT JOIN trendbuy_mart.creator_reliability cr
      ON cr.creator_id = t.creator_id
    LEFT JOIN trendbuy_mart.customer_aggregates cu
      ON cu.customer_id = p.customer_id
    LEFT JOIN trendbuy_mart.product_aggregates pr
      ON pr.product_id = p.product_id
  ) src
  ON tgt.order_id = src.order_id
  WHEN MATCHED THEN UPDATE SET
    tgt.customer_id = src.customer_id,
    tgt.product_id = src.product_id,
    tgt.purchase_timestamp = src.purchase_timestamp,
    tgt.feature_discount_pct = src.discount_pct,
    tgt.feature_velocity_24h = src.velocity_24h,
    tgt.feature_text_sentiment = src.sentiment_score,
    tgt.feature_hours_since_trend_peak = src.hours_since_trend_peak,
    tgt.feature_creator_reliability = src.creator_reliability,
    tgt.feature_cust_prior_return_rate_90d = src.prior_return_rate_90d,
    tgt.feature_cust_avg_order_value_90d = src.avg_order_value_90d,
    tgt.feature_prod_size_fit_rate = src.size_fit_issue_rate,
    tgt.feature_device_type = src.device_type,
    tgt.top_shap_contrib_1 = src.top_shap_contrib_1,
    tgt.top_shap_contrib_2 = src.top_shap_contrib_2,
    tgt.top_shap_contrib_3 = src.top_shap_contrib_3,
    tgt.model_version = src.model_version,
    tgt.updated_at = CURRENT_TIMESTAMP()
  WHEN NOT MATCHED THEN INSERT (
    order_id,
    customer_id,
    product_id,
    purchase_timestamp,
    feature_discount_pct,
    feature_velocity_24h,
    feature_text_sentiment,
    feature_hours_since_trend_peak,
    feature_creator_reliability,
    feature_cust_prior_return_rate_90d,
    feature_cust_avg_order_value_90d,
    feature_prod_size_fit_rate,
    feature_device_type,
    top_shap_contrib_1,
    top_shap_contrib_2,
    top_shap_contrib_3,
    model_version,
    created_at,
    updated_at
  ) VALUES (
    src.order_id,
    src.customer_id,
    src.product_id,
    src.purchase_timestamp,
    src.discount_pct,
    src.velocity_24h,
    src.sentiment_score,
    src.hours_since_trend_peak,
    src.creator_reliability,
    src.prior_return_rate_90d,
    src.avg_order_value_90d,
    src.size_fit_issue_rate,
    src.device_type,
    src.top_shap_contrib_1,
    src.top_shap_contrib_2,
    src.top_shap_contrib_3,
    src.model_version,
    CURRENT_TIMESTAMP(),
    CURRENT_TIMESTAMP()
  );

  GET DIAGNOSTICS v_processed = ROW_COUNT;
  -- Update process log
  UPDATE trendbuy_meta.feature_process_log
    SET finished_at = CURRENT_TIMESTAMP(), processed_orders = v_processed
    WHERE started_at = v_started;

  RETURN 'Processed: ' || v_processed;
END;
$$;
```

Operational notes

* The stored procedure reads from `trendbuy_meta.stream_purchases`. In Snowflake, reading the stream consumes the change set; the next run will read only new deltas. This pattern implements exactly-once consumption semantics when tasks and stored procedures complete successfully. See Streams and Tasks docs. ([Snowflake][1])
* Use `LATERAL` join pattern shown above to pick the most recent trend prior to the purchase timestamp and avoid temporal leakage.

### 3. Create a Task to run the stored procedure

You can schedule this task to run frequently or create a task with a stream dependency to be event-driven.

Scheduled every minute example:

```sql
CREATE OR REPLACE TASK trendbuy_meta.task_process_features
  WAREHOUSE = "WH_SMALL"
  SCHEDULE = 'USING CRON * * * * * UTC'  -- every minute
AS
  CALL trendbuy_meta.sp_process_feature_updates();
```

Event-driven example: tasks can be set to run when a stream has data by setting `WHEN` clause, but currently the documented pattern is to poll the stream on a schedule or to construct a task tree where the parent task monitors the stream. See Tasks documentation. ([Snowflake][3])

Start the task:

```sql
ALTER TASK trendbuy_meta.task_process_features RESUME;
```

# Part D: Backfill and historical rebuild procedure

Backfills must be separate from the streaming Tasks to avoid excessive load.

## Backfill strategy

* Create a temporary staging table containing a snapshot of historical purchases to reprocess.
* Process in time-windowed batches (for example by month) to control resource use.
* When backfill completes, mark the backfill run in a metadata table.

## Backfill SQL pattern

```sql
-- 1. create batch staging for a given date range
CREATE OR REPLACE TABLE trendbuy_meta.backfill_batch AS
SELECT p.*
FROM trendbuy_stg.purchases p
WHERE p.purchase_timestamp >= '2025-01-01' AND p.purchase_timestamp < '2025-02-01';

-- 2. process the batch with the same transformation logic used by the proc but reading the batch table
MERGE INTO trendbuy_mart.feature_trendbuy_v1 tgt
USING (
  SELECT
    b.order_id,
    b.customer_id,
    b.product_id,
    b.purchase_timestamp,
    CASE WHEN b.list_price IS NULL OR b.list_price = 0 THEN 0
         ELSE (b.list_price - b.paid_price) / b.list_price END AS discount_pct,
    -- same joins to trends and aggregates as in the stored proc
    ...
  FROM trendbuy_meta.backfill_batch b
  LEFT JOIN trendbuy_stg.trends t
    ON t.product_id = b.product_id
    AND t.trend_timestamp <= b.purchase_timestamp
  QUALIFY ROW_NUMBER() OVER (PARTITION BY b.order_id ORDER BY t.trend_timestamp DESC) = 1
) src
ON tgt.order_id = src.order_id
WHEN MATCHED THEN UPDATE ...
WHEN NOT MATCHED THEN INSERT ...;
```

Batch size control

* Break backfills into daily or weekly windows to reduce likelihood of long-running transactions and to maintain concurrency.

# Part E: Feature store maintenance, versioning, and promotion

## 1. Model-versioned features

* Keep a `model_version` column and a `created_at` / `updated_at` audit trail.
* When promoting a new feature schema or model, create `feature_trendbuy_v2` and run a parallel pipeline until validated.

## 2. Schema changes

* Use `CREATE OR REPLACE TABLE ... CLONE` or `ALTER TABLE ADD COLUMN` patterns to evolve schema.
* When adding new heavy computed features, prefer adding columns with nullable defaults and backfilling in batches.

## 3. Materialized caching alternatives

* If a particular feature query is expensive and used constantly, consider a materialized view or dynamic table. Note that materialized views require appropriate Snowflake edition and have constraints. Validate with Snowflake docs before using. ([Snowflake][4])

# Part F: Serving patterns and read APIs

Two common serving patterns:

* Batch scoring for model training and offline analytics: read entire `feature_trendbuy_v1` table with appropriate filters.
* Low-latency lookups during scoring: use a narrow SELECT with `order_id` or `product_id` and `purchase_timestamp` filters. Example:

```sql
SELECT *
FROM trendbuy_mart.feature_trendbuy_v1
WHERE order_id = 'ORDER12345';
```

Best practices

* Avoid SELECT * in production-serving functions. Specify required columns to minimize data scanned.
* Use clustering keys and date filters to exploit micro-partition pruning.

# Part G: Data quality checks and monitoring

Implement automated checks to detect problems early.

## 1. Row-count sanity checks

```sql
-- Expected rate of purchases per hour; alert if far outside
SELECT DATE_TRUNC('hour', loaded_at) hour, COUNT(*) cnt
FROM trendbuy_stg.purchases
WHERE loaded_at >= DATEADD('hour', -6, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY 1 DESC;
```

## 2. Null and cardinality checks

* Null ratio for product_id, customer_id, purchase_timestamp should be zero or very small.
* Cardinality growth for `product_id` should be monitored.

## 3. Stream lag check

* If `trendbuy_meta.stream_purchases` shows no rows consumed for N cycles, alert.

## 4. Model feature distribution drift

* Compute rolling means and percentiles for numeric features and alert when they shift beyond thresholds.

# Part H: Rollback and safety playbook

* If a processing run corrupts features, restore the feature table from a clone taken before the run. Use `CREATE TABLE feature_trendbuy_v1_restore CLONE trendbuy_mart.feature_trendbuy_v1 AT (TIMESTAMP => '<timestamp>');`
* Maintain frequent copies or use Time Travel with a retention policy determined by your Snowflake edition.
* Keep the stored procedure code in source control and use CI to validate merges into main.

# Part I: Example end-to-end test queries

1. Validate that each new purchase produces a feature row after the task runs:

```sql
SELECT p.order_id, f.order_id AS in_feature
FROM trendbuy_stg.purchases p
LEFT JOIN trendbuy_mart.feature_trendbuy_v1 f
  ON p.order_id = f.order_id
WHERE p.loaded_at >= DATEADD('hour', -1, CURRENT_TIMESTAMP())
  AND f.order_id IS NULL;
```

Rows returned indicate missing feature materialization.

2. Validate temporal join correctness

```sql
-- For a given purchase, show the trend picked
SELECT p.order_id, p.purchase_timestamp, t.trend_timestamp, t.velocity_24h
FROM trendbuy_stg.purchases p
JOIN trendbuy_stg.trends t
  ON t.product_id = p.product_id
  AND t.trend_timestamp <= p.purchase_timestamp
QUALIFY ROW_NUMBER() OVER (PARTITION BY p.order_id ORDER BY t.trend_timestamp DESC) = 1
ORDER BY p.purchase_timestamp DESC
LIMIT 20;
```

# Part J: Which points require verification or are uncertain

* TikTok feed schema and latency characteristics. I cannot verify this; confirm the actual feed fields and how soon after a video posts the velocity metrics are available.
* Snowflake edition and feature availability in your environment. Materialized views, dynamic tables, and Time Travel retention depend on edition and account settings. Confirm edition or consult Snowflake account team. I cannot verify this. ([Snowflake][4])
* Warehouse sizing and cost constraints for running tasks at the desired frequency. Confirm allowable concurrency and budget.
* Data retention and PII masking policies for customer-level features. Confirm with legal and privacy teams.
* Creator reliability table availability. If not already computed, build a scheduled aggregate that computes `creator_reliability` with a defined window.

# Part K: Next concrete deliverables I will produce if you want them

* A ready-to-run Snowflake SQL file containing all DDL and procedure code, with parameterized variables for schema names and warehouse names.
* A Snowpark Python stored procedure version that computes advanced features (text sentiment aggregation, embeddings joins) if you use Snowpark.
* A CI-friendly SQL test suite for the data-quality checks above.
* A sample Airflow DAG or orchestration spec that triggers Snowflake Tasks and backfills safely.

Tell me which deliverable you want first and I will generate it immediately as a runnable SQL file and CI-friendly artifact.

References used while producing these templates

* Snowflake Streams and Tasks introduction. ([Snowflake][1])
* CREATE STREAM syntax and usage. ([Snowflake][5])
* Micro-partitions, clustering, and best practices for partition pruning. ([Snowflake][2])
* Materialized views and dynamic tables overview. ([Snowflake][4])

If you want, I will now generate a single, complete SQL file with parameter placeholders, comments for each step, and a short README that you can drop into your repo and run after adjusting database, schema, and warehouse names.

[1]: https://docs.snowflake.com/en/user-guide/data-pipelines-intro?utm_source=chatgpt.com "Introduction to Streams and Tasks"
[2]: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions?utm_source=chatgpt.com "Micro-partitions & Data Clustering"
[3]: https://docs.snowflake.com/en/user-guide/tasks-intro?utm_source=chatgpt.com "Introduction to tasks"
[4]: https://docs.snowflake.com/en/sql-reference/sql/create-materialized-view?utm_source=chatgpt.com "CREATE MATERIALIZED VIEW"
[5]: https://docs.snowflake.com/en/sql-reference/sql/create-stream?utm_source=chatgpt.com "CREATE STREAM"
