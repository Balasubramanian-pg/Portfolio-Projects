# Enterprise-grade Data Model and Operational Design — Pet Wellness Tracker

Below is a comprehensive, operational, enterprise-ready design built from the core entities you provided. It covers logical model, physical schema (Snowflake-oriented DDL), ingestion patterns, storage and retention strategy, SCD handling, feature store and ML-serving patterns, data governance, monitoring, and operational runbooks. The goal is to move from a loose model to a production implementation that supports analytics, ML, realtime alerts, and Power BI consumption at scale.


## 1. Architecture overview (high level)

* Edge devices (collars) -> Gateways / mobile phones -> Message broker (MQTT or Kafka)
* Stream processor / ingestion lambda -> Raw landing area (cloud object storage, Parquet)
* Snowflake via Snowpipe or bulk loads - raw schema, staging schema, curated schema, analytics schema
* dbt for transformation, feature engineering, and SCD handling
* Model training notebooks + model registry -> containerized model serving (FastAPI)
* Feature tables surfaced to ML serving and Power BI via curated schemas and materialized views
* Observability: Prometheus / Grafana for infra + Data quality tools (Great Expectations / dbt tests)
* Governance: RBAC, masking policies, audit logs, consent management

Rationale: separate raw/staging/curated layers enables traceability, replay, simple rollback, auditability, and fits CI/CD for data code.


## 2. Logical data model (expanded)

Entities and key relationships:

* `owners` 1 - n `pets`
* `pets` 1 - n `clinic_visits`
* `pets` 1 - n `telemetry_events` (time-series)
* `pets` 1 - n `computed_features` (time-windowed aggregates)
* `clinic_visits` 1 - n `visit_documents` (original PDFs / scans metadata)
* `devices` 1 - 1 `pets` or 1 - n mapping depending on multi-pet usage per device

Important notes:

* Separate device identity (`device_id`, `hardware_serial`) from `pet_id`. Devices may move between pets.
* Keep an audit trail for changes to `owners`, `pets`, and `clinic_visits` using SCD Type 2 for clinical correctness.

Core entities (summary with explanation)

* `owners` - contact and consent metadata, used for communication and PII control.
* `pets` - profile used for joins and stable identifiers.
* `devices` - telemetry source metadata, battery and firmware status.
* `telemetry_events` - high cardinality time-series; keep raw events minimal and compress.
* `clinic_visits` - canonical clinical events and diagnosis codes.
* `visit_documents` - pointer to raw PDFs/images, OCR outputs and confidence.
* `computed_features` - engineered features for ML and reporting: activity deltas, sleep metrics, lick rates, weight_trend, etc.


## 3. Physical schema and Snowflake DDL (recommended)

Structure schemas:

* `raw` - raw ingested records as-is (VARIANT for semi-structured)
* `staging` - parsed raw fields, minimal cleanup
* `curated` - canonical tables and SCD2 histories
* `analytics` - denormalized wide tables for Power BI and ML serving

### 3.1 Naming conventions and standards

* Lowercase snake_case for names.
* Prefix schemas: `raw_`, `stg_`, `cur_`, `anl_`.
* Column names: `*_ts` for timestamps, ISO-8601 UTC.
* Use `surrogate_id` for technical keys and keep `source_id` for origin mapping.

### 3.2 Example Snowflake DDL — curated schema

```sql
-- curated.pets (SCD Type 2)
CREATE TABLE cur.pets (
  pet_sk           BIGINT AUTOINCREMENT PRIMARY KEY,
  pet_id           VARCHAR(64) NOT NULL, -- business id stable across systems
  owner_id         VARCHAR(64) NOT NULL,
  name             VARCHAR(200),
  species          VARCHAR(50),
  breed            VARCHAR(100),
  dob              DATE,
  sex              VARCHAR(10),
  neutered         BOOLEAN,
  microchip_id     VARCHAR(128),
  valid_from       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
  valid_to         TIMESTAMP_NTZ,
  is_current       BOOLEAN DEFAULT TRUE,
  source_system    VARCHAR(100),
  record_md5       VARCHAR(64), -- change detection
  created_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);

-- curated.owners (SCD Type 2 for contact updates)
CREATE TABLE cur.owners (
  owner_sk         BIGINT AUTOINCREMENT PRIMARY KEY,
  owner_id         VARCHAR(64) NOT NULL,
  name             VARCHAR(200),
  contact_phone    VARCHAR(50),
  contact_email    VARCHAR(256),
  consent_flags    VARIANT, -- JSON: {"sms":true,"push":true,"email":false,"share_research":false}
  valid_from       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP,
  valid_to         TIMESTAMP_NTZ,
  is_current       BOOLEAN DEFAULT TRUE,
  source_system    VARCHAR(100),
  record_md5       VARCHAR(64),
  created_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);

-- curated.devices
CREATE TABLE cur.devices (
  device_sk        BIGINT AUTOINCREMENT PRIMARY KEY,
  device_id        VARCHAR(128) NOT NULL, -- hardware id
  model            VARCHAR(64),
  firmware_version VARCHAR(64),
  status           VARCHAR(32), -- active, retired, damaged
  assigned_pet_id  VARCHAR(64),
  last_seen_ts     TIMESTAMP_NTZ,
  created_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);

-- analytics.telemetry_events (time-series table optimized for queries)
CREATE TABLE anl.telemetry_events (
  event_id         VARCHAR(128) PRIMARY KEY,
  device_id        VARCHAR(128) NOT NULL,
  pet_id           VARCHAR(64),
  event_ts         TIMESTAMP_NTZ NOT NULL,
  accel_x          FLOAT,
  accel_y          FLOAT,
  accel_z          FLOAT,
  step_count       INTEGER,
  lick_count       INTEGER,
  gps_lat          FLOAT,
  gps_long         FLOAT,
  battery_pct      FLOAT,
  payload_raw      VARIANT, -- raw JSON if needed
  ingested_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

Notes:

* Use `VARIANT` in raw schema for full fidelity of incoming JSON.
* In `anl.telemetry_events` keep normalized typed columns for analytics. Keep `payload_raw` for replay/debug.

### 3.3 Clustering and performance

* For `anl.telemetry_events` set clustering key on `(pet_id, event_ts)` to improve range queries by pet and time.
* For Snowflake, create clustering on high-cardinality time columns to reduce micro-partition pruning overhead.

```sql
ALTER TABLE anl.telemetry_events CLUSTER BY (pet_id, event_ts);
```

* For `cur.clinic_visits` cluster by `(clinic_id, visit_date)`.

### 3.4 Materialized views and aggregates

* Create materialized views or precomputed aggregates for frequently used KPIs to accelerate Power BI.

Example: daily_activity_by_pet

```sql
CREATE MATERIALIZED VIEW anl.mv_daily_activity_by_pet AS
SELECT
  pet_id,
  CAST(event_ts AS DATE) AS day_date,
  COUNT(*) AS event_count,
  SUM(step_count) AS total_steps,
  AVG(battery_pct) AS avg_battery_pct
FROM anl.telemetry_events
GROUP BY pet_id, day_date;
```

Caveat: materialized views cost compute to maintain. If telemetry is high velocity, use scheduled aggregated tables with dbt and incremental loads.


## 4. Ingestion patterns and recommended pipeline

### 4.1 Device -> Cloud ingestion pattern

* Edge device -> Gateway / phone -> MQTT broker or Kafka cluster
* Stream processor (Kafka Connect, Kinesis Data Streams, or Azure Event Hubs)
* Stream consumer -> Transform and write to S3/Blob in compacted Parquet with partitioning by date, clinic_id, device_id
* Snowpipe or scheduled COPY INTO to load raw files into `raw` schema

Advantages:

* S3 as canonical landing zone for raw telemetry ensures immutability and easy reprocessing.
* Parquet compresses numeric telemetry well and reduces storage cost.

### 4.2 Snowpipe + auto-ingest

* Use Snowpipe with event notifications from S3 to achieve near-realtime ingestion.
* Configure Snowpipe to write into `raw.telemetry_events_raw` as VARIANT then run scheduled parsing to `stg` and `cur`.

### 4.3 Staging and transformation

* `raw` schema: store exactly what arrives with source metadata.
* `stg` schema: normalization, data type casting, deduplication.
* `cur` schema: join enrichment, SCD2 handling, commercial business keys.

Use dbt for transformations and to implement idempotent incremental models.


## 5. SCD patterns and example (owners and pets)

* Implement SCD Type 2 for `owners` and `pets` to preserve history for clinical auditing.
* Use hash-based change detection using `record_md5`. If MD5 changes, close prior row and insert new row with `valid_from`/`valid_to` updates.

Example SCD2 pseudo-process using dbt materialization:

1. Compute `record_md5` of incoming record.
2. If `record_md5` differs from `cur` current row, set `valid_to` = ingestion_ts for existing row and mark `is_current` = false. Insert new row with `is_current` = true.

SQL snippet (conceptual):

```sql
-- pseudocode - run in dbt as an incremental model
MERGE INTO cur.owners AS tgt
USING stg.owners AS src
ON tgt.owner_id = src.owner_id AND tgt.is_current = TRUE
WHEN MATCHED AND tgt.record_md5 != src.record_md5 THEN
  UPDATE SET tgt.is_current = FALSE, tgt.valid_to = src.ingested_at
WHEN NOT MATCHED THEN
  INSERT (... columns ..., is_current, valid_from, record_md5) VALUES (..., TRUE, src.ingested_at, src.record_md5);
```


## 6. Telemetry storage strategy and retention

Telemetry is high-volume. Design a tiered storage policy:

* Hot: last 90 days in Snowflake `anl.telemetry_events` for realtime alerts and analytics.
* Warm: 90-365 days aggregated to daily/hourly summaries in `anl.mv_daily_activity_by_pet` or `anl.telemetry_summary_hourly`.
* Cold: raw Parquet files in S3 Glacier or equivalent for >365 days for forensic reprocessing.

Retention rules reduce compute and storage cost while keeping forensic capability.


## 7. Computed features and Feature Store patterns

* `computed_features` table holds time-windowed features with versioning and provenance.

Schema example:

```sql
CREATE TABLE ml.computed_features (
  feature_id       BIGINT AUTOINCREMENT PRIMARY KEY,
  pet_id           VARCHAR(64),
  feature_name     VARCHAR(128),
  start_ts         TIMESTAMP_NTZ,
  end_ts           TIMESTAMP_NTZ,
  value            FLOAT,
  feature_version  VARCHAR(32),
  batch_id         VARCHAR(128),
  created_at       TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);
```

* Use dbt to compute features incrementally and annotate `feature_version`.
* Serve features for real-time inference using a feature cache or an online feature store (Feast) backed by Redis for low-latency lookups. Long-tail features remain in Snowflake for batch scoring.

Feature freshness SLOs:

* Near-real-time features: latency < 5 minutes from ingestion to feature availability.
* Batch features: daily refresh. Choose SLA per use-case.


## 8. ML model lifecycle integration

* Training environment reads features from `ml.computed_features` and `cur.clinic_visits`.
* Register models in model registry with version, training data snapshot, metrics, and feature versions.
* Serve models with containerized microservices. For low-latency inference, serve a lightweight model in edge gateways for critical alerts and central model for complex scoring.

Model explainability:

* Persist SHAP or explanation outputs in `anl.model_explanations` for vet review.


## 9. Data governance, security, and privacy

### 9.1 PII handling

* Mask / encrypt sensitive columns: `contact_phone`, `contact_email` using Snowflake masking policies.
* Store consent flags in `VARIANT` with timestamps for legal audit.

Example masking policy pattern:

```sql
CREATE MASKING POLICY mask_contact AS (val STRING) RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('data_engineer','analytics_readonly') THEN 'xxx-xxx-xxxx'
    ELSE val
  END;
ALTER TABLE cur.owners MODIFY COLUMN contact_phone SET MASKING POLICY mask_contact;
```

### 9.2 Access control and roles

* Principle of least privilege: roles for ingestion, analytics, ML, and ops.
* Separate analytic read-only roles used by Power BI service account. Use service principals instead of user accounts.

### 9.3 Audit and lineage

* Capture metadata on `created_by`, `ingested_at`, `source_system`, and file manifests for raw loads.
* Use Snowflake Information Schema and external catalog (e.g., Amundsen or DataHub) to surface lineage and ownership.

### 9.4 Consent and opt-out

* Enforce opt-out at ingestion time. If `consent_flags.push = false`, filter device-to-owner linking for push notifications. Keep telemetry for analytics only if consent allows.


## 10. Data quality, testing, and monitoring

### 10.1 Data quality rules

* Telemetry event schema validation: non-null `event_ts`, valid `device_id`.
* Device heartbeat ratio per device and clinic: alert if daily heartbeats < 80% expected.
* OCR extraction confidence threshold: route low-confidence rows to human validation queue.

Implement via:

* dbt tests for schema constraints and row-level assertions.
* Great Expectations or similar for threshold checks.

### 10.2 Observability metrics

* Ingestion latency percentile (p50, p95, p99).
* Telemetry throughput events/sec.
* Device dropout rate per clinic per day.
* Feature freshness lag.
* Model prediction latency and accuracy drift.

Set SLOs and SLI alerts in Grafana or a cloud monitoring service.


## 11. Power BI and analytics considerations

* Provide curated analytics schema optimized for Power BI: `anl.pet_daily_summary`, `anl.clinic_kpis`, `anl.owner_engagement`.
* Use materialized views or pre-aggregated tables for high-cardinality joins.
* Use service account with role assigned to minimal privileges. Use row-level security (RLS) on datasets if vets should only see their clinic patients.

Example denormalized analytics table for Power BI:

```sql
CREATE OR REPLACE TABLE anl.pet_daily_summary AS
SELECT
  p.pet_id,
  p.name,
  p.breed,
  d.day_date,
  d.total_steps,
  d.event_count,
  v.last_visit_date,
  v.next_vaccine_due,
  o.owner_id,
  o.consent_flags
FROM cur.pets p
LEFT JOIN anl.mv_daily_activity_by_pet d ON p.pet_id = d.pet_id
LEFT JOIN (
  SELECT pet_id, MAX(visit_date) AS last_visit_date, MAX(next_vaccine_due) AS next_vaccine_due
  FROM cur.clinic_visits GROUP BY pet_id
) v ON p.pet_id = v.pet_id
LEFT JOIN cur.owners o ON p.owner_id = o.owner_id;
```

Power BI tips:

* Avoid live direct queries on massive telemetry tables. Use aggregated views.
* Keep data refresh cadence sensible for dashboards: near-real-time dashboards can rely on incremental refresh and scheduled queries.


## 12. Operational runbook excerpts

### 12.1 Device onboarding

* Steps: register device -> provision device credentials -> assign to clinic/pet -> set initial firmware -> start telemetry.
* Validate: initial heartbeat within 10 minutes, battery status read, firmware matches approved version.

### 12.2 Incident: spike in telemetry dropouts

* Triage: check gateway connectivity, inspect S3 landing for raw files, check stream processor lag.
* Remediation: re-start gateway, re-run failed ingestion files using Snowpipe auto-reload, notify wireless support.

### 12.3 OCR low-confidence backlog

* Auto-route documents below confidence threshold to human validators. Provide a small web UI to review parsed fields and correct values. Keep validation audit with `validator_id` and `validated_at`.


## 13. Sample analytic queries (practical)

1. Compute 24h activity delta for a pet:

```sql
WITH last_24h AS (
  SELECT pet_id, SUM(step_count) AS steps_24h
  FROM anl.telemetry_events
  WHERE event_ts >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
  GROUP BY pet_id
),
prev_24h AS (
  SELECT pet_id, SUM(step_count) AS steps_prev_24h
  FROM anl.telemetry_events
  WHERE event_ts BETWEEN DATEADD(hour, -48, CURRENT_TIMESTAMP()) AND DATEADD(hour, -24, CURRENT_TIMESTAMP())
  GROUP BY pet_id
)
SELECT l.pet_id,
       l.steps_24h,
       p.steps_prev_24h,
       CASE
         WHEN p.steps_prev_24h IS NULL THEN NULL
         ELSE (l.steps_24h - p.steps_prev_24h) / NULLIF(p.steps_prev_24h,0)
       END AS activity_delta_24h
FROM last_24h l
LEFT JOIN prev_24h p ON l.pet_id = p.pet_id;
```

2. No-show rate by clinic for last 90 days:

```sql
SELECT clinic_id,
       COUNT(CASE WHEN status = 'no_show' THEN 1 END) AS no_shows,
       COUNT(*) AS scheduled,
       (COUNT(CASE WHEN status = 'no_show' THEN 1 END) / COUNT(*))::FLOAT AS no_show_rate
FROM cur.clinic_visits
WHERE visit_date >= DATEADD(day, -90, CURRENT_DATE())
GROUP BY clinic_id;
```


## 14. Cost and capacity planning heuristics

* Estimate telemetry event rate per device. Example: 1 event per minute = 1440 events/day/device. For 50,000 active devices this is 72M events/day. This impacts partitioning and storage strategy.
* Use compressed Parquet on S3 for raw storage to control cost.
* Snowflake compute sizing: separate smaller warehouses for ETL and larger warehouses for transformations and Power BI refresh windows. Use multi-cluster warehouses for concurrency.

Recommendation: prototype with realistic data sample to measure actual ingestion and compute cost, then refine retention and aggregation.


## 15. Deliverables and implementation plan (concrete)

Phase 0 - week 0

* Finalize source contracts, device vendor, and data access.
* Provision S3, Snowflake, Kafka/MQTT and CI/CD.

Phase 1 - weeks 1-4

* Implement raw landing and Snowpipe.
* Create `raw` and `stg` schemas plus initial dbt models.
* Build OCR pipeline and human validation UI.

Phase 2 - weeks 5-8

* Implement `cur` tables with SCD2 and device registry.
* Create aggregated tables and materialized views for Power BI.
* Build computed_features ETL and initial ML training.

Phase 3 - weeks 9-12

* Pilot with two clinics. Run QA, monitoring and iterate.
* Deploy Power BI datasets and vet dashboard templates.
* Deliver ops runbook, monitoring dashboards, and knowledge transfer.


## 16. Points that require verification or are uncertain

* Exact telemetry event frequency expected from collar models and device fleet size. This affects storage and compute sizing.
* Device vendor guarantees on battery and replacement rates; chew/damage rates in client population.
* Precise legal/regulatory requirements for pet health data in the jurisdictions of the 50 clinics. Verify with legal.
* Client expectation on retention policy for raw telemetry and clinical history.
* Availability of clinic CRM fields for owner contact and consent flags.
* SLA for real-time alerts and acceptable false positive rate for clinical escalation.

Label these points as blockers to finalize retention, cost, and architecture choices.


## 17. Next steps and immediate actions I can produce now

Pick any of the following and I will produce it immediately:

* Snowflake-ready full DDL for `raw`, `stg`, `cur`, and `anl` schemas including sequences, constraints, clustering, and sample grants.
* dbt model templates for SCD2 handling (owners and pets), telemetry incremental model, and computed feature examples.
* A sample ingestion manifest and Snowpipe configuration + S3 layout recommended for telemetry.
* A short pilot acceptance test plan and monitoring dashboard specification (Grafana/Prometheus or cloud equivalent).

Choose one item and I will output the full artifact now.