# End-to-end conceptualization: SQL schema and ETL for bookings → weather merge

Below is a complete, practical blueprint you can hand to engineers and data analysts. It covers the data warehouse schema, raw/staging layers, example SQL for merging bookings with hourly weather, dbt model structure, orchestration (Airflow DAG sketch), operational considerations, monitoring, and a sample API call budget. Where external facts matter I cite authoritative docs.

---

## 1. Overview and objectives

* Objective: create a reproducible pipeline that joins resort bookings with historical and forecasted hourly weather so models and dashboards can score cancellation risk 72 hours before check-in.
* Requirements:

  * Raw retention of source payloads for traceability.
  * Deterministic merges by resort and local timestamp.
  * Ability to join forecasts (72h) and historical hourly observations.
  * Lightweight retry and fallback to secondary weather provider when rate limited.
* Key references: Airflow orchestration best practices, dbt transformation patterns, and weather API options. ([Apache Airflow][1])

---

## 2. Data model (warehouse / star schema)

### Fact and dimension overview

* Fact tables

  * `fact_bookings` — grain: one row per booking
  * `fact_ancillary_sales` — grain: one row per sale
* Dimension tables

  * `dim_resort` — resort metadata and timezone
  * `dim_channel`, `dim_guest_type`, `dim_date` (classic date dim)
* Weather table (time-series)

  * `weather_hourly` — grain: one row per resort per UTC hour

### Create table samples (SQL DDL)

Use your warehouse SQL dialect; sample below is ANSI-ish with comments. Adjust types.

```sql
-- dimension: resort
CREATE TABLE analytics.dim_resort (
  resort_id        INT PRIMARY KEY,
  resort_name      VARCHAR(200),
  latitude         NUMERIC(9,6),
  longitude        NUMERIC(9,6),
  timezone         VARCHAR(64),
  capacity_rooms   INT
);

-- fact: bookings (staging canonicalized)
CREATE TABLE raw.fact_bookings_raw (
  booking_id         VARCHAR(64) PRIMARY KEY,
  resort_id          INT,
  check_in_date      TIMESTAMP,    -- local resort time normalized on ingestion
  check_out_date     TIMESTAMP,
  booked_rate_cents  BIGINT,
  paid_rate_cents    BIGINT,
  channel_id         INT,
  guest_type_id      INT,
  booking_created_at TIMESTAMP,
  cancelled_flag     BOOLEAN,
  cancellation_date  TIMESTAMP,
  cancellation_reason VARCHAR(400),
  payload_json       VARIANT,      -- raw payload for traceability
  ingestion_ts       TIMESTAMP DEFAULT current_timestamp
);

-- weather hourly store
CREATE TABLE raw.weather_hourly_raw (
  resort_id          INT,
  observed_at_utc    TIMESTAMP,     -- canonical UTC hour
  precip_mm          NUMERIC(6,2),
  temp_c             NUMERIC(5,2),
  wind_kph           NUMERIC(6,2),
  provider           VARCHAR(64),   -- provider name
  forecast_horizon_h INT,           -- 0 for observed, 24/48/72 for forecast slices
  forecast_certainty NUMERIC(5,2),  -- normalized 0..100
  payload_json       VARIANT,
  ingestion_ts       TIMESTAMP DEFAULT current_timestamp
);

-- merged bookings to hourly weather (materialized mart)
CREATE TABLE analytics.mart_bookings_weather_hourly (
  booking_id         VARCHAR(64),
  resort_id          INT,
  check_in_date      TIMESTAMP,
  check_in_date_utc  TIMESTAMP,
  weather_observed_at TIMESTAMP,
  precip_mm          NUMERIC(6,2),
  temp_c             NUMERIC(5,2),
  forecast_horizon_h INT,
  forecast_certainty NUMERIC(5,2),
  cancellation_flag  BOOLEAN,
  cancellation_reason VARCHAR(400),
  booking_value_cents BIGINT,
  lead_time_days     INT,
  ingestion_ts       TIMESTAMP,
  PRIMARY KEY (booking_id, weather_observed_at)
);
```

---

## 3. ETL / ELT architecture (conceptual)

* Extraction:

  * Bookings and ancillaries: incremental extracts from PMS via CDC or daily batch exports to S3 / blob storage.
  * Weather: hourly pulls from primary provider (OpenWeather or provider of choice) and a fallback provider (NOAA or secondary vendor) for gaps. Use bulk historical for backfills. ([openweathermap.org][2])
* Load:

  * Landing raw JSON into object storage (S3 / GCS) and raw tables (`raw.*`) in the warehouse.
* Transform:

  * Use dbt for canonicalization and transformations: `stg_bookings`, `stg_weather_hourly`, then `mart_bookings_weather_hourly`.
  * Models run daily or hourly as appropriate.
* Orchestration:

  * Airflow controls sensor-based triggers, retries, and alerting. Use modular DAGs and avoid heavy computation in DAG code. ([Apache Airflow][1])
* Serving:

  * Materialized marts feed Power BI and model scoring services.

---

## 4. Example ETL SQL: canonicalize and merge

### 4.1 Staging booking canonicalization (`stg_bookings.sql` — dbt model)

```sql
with src as (
  select
    booking_id,
    resort_id,
    parse_timestamp(check_in_date, 'YYYY-MM-DD"T"HH24:MI:SS') as check_in_raw,
    parse_timestamp(booking_created_at, 'YYYY-MM-DD"T"HH24:MI:SS') as created_raw,
    cancelled_flag,
    cancellation_date,
    cancellation_reason,
    booked_rate_cents
  from raw.fact_bookings_raw
  where ingestion_ts > dateadd(day, -7, current_date)  -- incremental window example
)

, with_tz as (
  select
    booking_id,
    resort_id,
    convert_timezone(dim.timezone, 'UTC', check_in_raw) as check_in_utc,
    -- lead time in days
    datediff(day, created_raw, check_in_raw) as lead_time_days,
    cancelled_flag,
    cancellation_date,
    cancellation_reason,
    booked_rate_cents
  from src
  join analytics.dim_resort dim using(resort_id)
)

select * from with_tz;
```

### 4.2 Staging weather (`stg_weather_hourly.sql`)

```sql
with src as (
  select
    resort_id,
    observed_at_utc,
    precip_mm,
    temp_c,
    wind_kph,
    provider,
    forecast_horizon_h,
    forecast_certainty
  from raw.weather_hourly_raw
  where ingestion_ts > dateadd(day, -30, current_date)  -- incremental
)

-- optional: quality filters
select * from src
where precip_mm is not null
and observed_at_utc is not null;
```

### 4.3 Merge bookings to nearest hourly weather (mart model)

Logic:

* For each booking, attach the weather row where `weather.observed_at_utc` equals the check_in UTC hour or the nearest hour within ±1 hour.
* Also attach forecast slices (72h, 48h, 24h) by matching `forecast_horizon_h` values.

SQL (dbt materialized view/table):

```sql
with bookings as (
  select booking_id, resort_id, check_in_utc, booked_rate_cents, lead_time_days
  from {{ ref('stg_bookings') }}
)

, weather as (
  select resort_id, observed_at_utc, precip_mm, temp_c, wind_kph, provider, forecast_horizon_h, forecast_certainty
  from {{ ref('stg_weather_hourly') }}
)

-- match exact hour first
, exact as (
  select
    b.booking_id,
    b.resort_id,
    b.check_in_utc,
    w.observed_at_utc,
    w.precip_mm,
    w.temp_c,
    w.forecast_horizon_h,
    w.forecast_certainty,
    b.booked_rate_cents,
    b.lead_time_days
  from bookings b
  left join weather w
    on b.resort_id = w.resort_id
   and date_trunc('hour', b.check_in_utc) = date_trunc('hour', w.observed_at_utc)
)

-- fallback to nearest hour within 1 hour
, fallback as (
  select
    e.*
  from exact e
  where e.observed_at_utc is not null

  union all

  select
    b.booking_id,
    b.resort_id,
    b.check_in_utc,
    w.observed_at_utc,
    w.precip_mm,
    w.temp_c,
    w.forecast_horizon_h,
    w.forecast_certainty,
    b.booked_rate_cents,
    b.lead_time_days
  from bookings b
  left join lateral (
     select * from weather w2
     where w2.resort_id = b.resort_id
     order by abs(datediff(second, b.check_in_utc, w2.observed_at_utc)) asc
     limit 1
  ) w
  where not exists (select 1 from exact ex where ex.booking_id = b.booking_id and ex.observed_at_utc is not null)
)

select * from fallback;
```

Notes:

* The lateral nearest-hour join pattern is presented conceptually; adapt to your SQL dialect.
* Materialize as a table for fast reads by BI and the model scoring service.

---

## 5. dbt project layout and examples

* Recommended dbt structure

  * `models/staging/stg_bookings.sql`
  * `models/staging/stg_weather_hourly.sql`
  * `models/marts/mart_bookings_weather_hourly.sql`
  * `models/tests/` — add schema and data tests for nulls, uniqueness, and foreign keys
* Example tests:

  * uniqueness test on `booking_id` in `stg_bookings`
  * not_null tests for `resort_id`, `check_in_utc`
* Use dbt ephemeral models for complex but small intermediate steps to avoid unnecessary tables. Follow dbt staging patterns to keep transformations modular. ([dbt Labs][3])

---

## 6. Orchestration sketch (Airflow DAG)

High-level DAG tasks and sequence:

* `sensor_pms_extract` — sensor or scheduled task that lands latest bookings file to object storage
* `task_load_bookings_raw` — load raw bookings into `raw.fact_bookings_raw`
* `task_fetch_weather` — call weather API for resorts; write payload to object storage and `raw.weather_hourly_raw`
* `task_dbt_run_staging` — run dbt models for staging
* `task_dbt_run_marts` — build marts
* `task_run_scoring` — invoke model scoring service for bookings within next 72 hours
* `task_push_alerts` — send Teams/Slack alerts via Power Automate or webhook
* `task_monitoring` — run data quality checks, alert on failure

DAG considerations:

* Parameterize DAGs by resort or date windows.
* Keep heavy work in XCom-free tasks and in external workers.
* Use retries and exponential backoff for API calls. Follow Airflow best practices to avoid top-level DB calls in DAG file. ([Apache Airflow][1])

Example Airflow task pseudo Python:

```python
with DAG('bookings_weather_pipeline', schedule_interval='@hourly', catchup=False) as dag:
    extract_bookings = BashOperator(...)

    fetch_weather = PythonOperator(
        task_id='fetch_weather',
        python_callable=fetch_weather_for_resorts,
        op_kwargs={'resort_ids': RESORT_IDS, 'providers': ['openweather','nws']},
    )

    load_raw = PythonOperator(...)

    dbt_staging = BashOperator(command='dbt run --models +staging')
    dbt_marts = BashOperator(command='dbt run --models marts')

    scoring = PythonOperator(...)

    extract_bookings >> fetch_weather >> load_raw >> dbt_staging >> dbt_marts >> scoring
```

---

## 7. Weather API strategy and fallback

* Primary provider: use a paid provider offering hourly historical and forecast slices, for example OpenWeather History and Forecast APIs. These typically require subscription for full history and high request rate. ([openweathermap.org][2])
* Fallback: NOAA / NWS datasets for US locations for backfills and redundancy. Note NOAA has rate limits and may not be global or as granular in all regions. ([ncdc.noaa.gov][4])
* Caching: store fetched hourly records in `raw.weather_hourly_raw` and avoid re-requesting the same hour for 7 days unless your provider indicates an update.

---

## 8. API call budgeting example

Scenario: poll forecast slices for 15 resorts every 6 hours for 72-hour forecast.

Digit-by-digit arithmetic to compute calls per day:

* Number of polls per day = 24 / 6 = 4 polls per resort per day.

  * Calculation: 24 ÷ 6 = 4.
* Total calls per day = polls per day × number of resorts = 4 × 15 = 60.

  * Calculation: 4 × 15 = 60.
* Total calls per month (30 days) = 60 × 30 = 1,800.

  * Calculation: 60 × 30 = 1,800.

If you also fetch hourly observed data once per hour:

* Observed hourly calls per day = 24 × 15 = 360.

  * Calculation: 24 × 15 = 360.
* Combined calls per day = 60 + 360 = 420.

  * Calculation: 60 + 360 = 420.
* Combined monthly calls = 420 × 30 = 12,600.

  * Calculation: 420 × 30 = 12,600.

Action: pick a subscription tier that covers the monthly call volume or implement batching / bulk history pulls for cost efficiency. Use local caching to reduce repeated calls.

---

## 9. Data quality, testing, and monitoring

* Tests to implement (dbt + warehouse checks)

  * Uniqueness: `booking_id` is unique in staging.
  * Not null: `resort_id`, `check_in_utc`, `observed_at_utc` in merged mart.
  * Referential integrity: `resort_id` exists in `dim_resort`.
  * Anomaly detection: sudden dips in weather observations or spike in null forecasts.
* Monitoring

  * Model performance: track AUC, precision, and calibration daily.
  * Pipeline health: success rates, lag metrics, and API error rate.
  * Alerting: Slack/Teams for extraction or transformation failures and for concept drift.

---

## 10. Deployment, CI/CD and runbooks

* CI: Use GitHub Actions / GitLab CI to run dbt tests and linting on PRs.
* CD: On merge to main, run dbt in prod target and Airflow DAGs pick up new artifacts.
* Runbooks: document steps to reprocess a date range, backfill weather, and rotate API keys.
* Access controls: restrict write access to `raw.*` and production `analytics.*` to data engineering role.

---

## 11. Security, compliance, and governance

* PII: do not store guest payment card data. Mask or tokenize any guest personal data stored for analytics.
* Logging: keep raw payloads for 90 days in raw layer then move to cold storage for auditability.
* Data retention: align with company policy and local regulations for guest data.

---

## 12. Cost and operational tradeoffs

* Tradeoff: real-time hourly ingest increases API cost and compute but improves model freshness.
* Mitigation: use bulk historical pulls for backfills and cache forecasts; lower granularity for low-impact resorts.
* Recommendation: pilot with 4 resorts to measure the balance of cost vs value before chainwide rollout.

---

## 13. Short, concise explanation of reasoning steps taken

* I converted the project requirement into a layered data architecture: raw landing, staging canonicalization, and analytics mart.
* I defined a deterministic merge strategy matching bookings to hourly weather by resort and normalized UTC timestamps.
* I proposed orchestrator and transformation technologies and gave concrete SQL and dbt patterns to make the pipeline reproducible.
* I included operational considerations: API budgeting, failover, testing, monitoring, and governance.

---

## 14. Items requiring verification or decisions to make

1. Confirm actual available fields and formats from your PMS export or API.
2. Confirm whether you prefer hourly forecast polling or bulk forecast snapshots for cost reasons.
3. Verify provider availability and licensing for historical hourly data in all resort geographies. I cannot verify these for your accounts. ([openweathermap.org][2])
4. Agree retention policy for raw payloads and PII masking rules.
5. Approve pilot resort list and pilot budget to estimate real costs.

---

## 15. Suggested next artifact I will produce if you say go

* Fully parameterized dbt models and `schema.yml` tests for `stg_bookings`, `stg_weather_hourly`, and `mart_bookings_weather_hourly`.
* A runnable Airflow DAG Python file (skeleton) with tasks and clear operator configs.
* A sample Python module for `fetch_weather_for_resorts` implementing provider failover and retries.

Tell me which of the three you'd like me to generate first and I will produce the full artifact for immediate use.

[1]: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html?utm_source=chatgpt.com "Best Practices — Airflow 3.1.6 Documentation"
[2]: https://openweathermap.org/api?utm_source=chatgpt.com "Weather API"
[3]: https://www.getdbt.com/blog/data-transformation-best-practices?utm_source=chatgpt.com "Data transformation: Six critical best practices"
[4]: https://www.ncdc.noaa.gov/cdo-web/webservices/v2?utm_source=chatgpt.com "Climate Data Online: Web Services Documentation"
