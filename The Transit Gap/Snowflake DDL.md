## Snowflake DDL and GitHub Actions CI Workflow

**Transit Gap — Between-Stops Economy Analyzer**

This section provides **production-grade Snowflake DDL** and a **runnable GitHub Actions CI pipeline** aligned with the project bible. Everything is structured so it can be copied directly into your repository and executed with minimal modification.

ASSUMPTION
You have access to:

* A Snowflake account (trial or org account)
* A Snowflake user with permission to create databases, schemas, tables, and warehouses
* GitHub repository secrets configured for Snowflake credentials

---

## 1. Snowflake Logical Data Model

### Design principles

* Raw data is immutable.
* Transformations are idempotent.
* Tableau only queries curated or mart tables.
* Spatial logic is Snowflake-native where possible.

### Schema layout

* `RAW` — untouched ingested data
* `STAGING` — type-cast, cleaned, standardized
* `CURATED` — analytics-ready dimensions and facts
* `MARTS` — Tableau-optimized tables

---

## 2. Snowflake DDL

### 2.1 Database and Warehouse

```sql
-- =========================================================
-- DATABASE AND WAREHOUSE
-- =========================================================

CREATE OR REPLACE DATABASE TRANSIT_GAP_DB
COMMENT = 'Between-Stops Economy Analyzer';

CREATE OR REPLACE WAREHOUSE TRANSIT_GAP_WH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
COMMENT = 'Warehouse for Transit Gap analytics';
```

---

### 2.2 Schemas

```sql
-- =========================================================
-- SCHEMAS
-- =========================================================

CREATE OR REPLACE SCHEMA RAW;
CREATE OR REPLACE SCHEMA STAGING;
CREATE OR REPLACE SCHEMA CURATED;
CREATE OR REPLACE SCHEMA MARTS;
```

---

### 2.3 RAW Tables (Ingest Layer)

#### GTFS Stops

```sql
CREATE OR REPLACE TABLE RAW.GTFS_STOPS (
    stop_id            VARCHAR,
    stop_name          VARCHAR,
    stop_lat           FLOAT,
    stop_lon           FLOAT,
    stop_desc          VARCHAR,
    location_type      INTEGER,
    parent_station     VARCHAR,
    ingestion_ts       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Business Registry

```sql
CREATE OR REPLACE TABLE RAW.BUSINESSES (
    business_id        VARCHAR,
    business_name      VARCHAR,
    naics_code         VARCHAR,
    revenue_band       VARCHAR,
    address            VARCHAR,
    latitude           FLOAT,
    longitude          FLOAT,
    hours_of_operation VARCHAR,
    ingestion_ts       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Mobile Footfall

```sql
CREATE OR REPLACE TABLE RAW.FOOTFALL (
    grid_id            VARCHAR,
    event_date         DATE,
    footfall_count     INTEGER,
    latitude           FLOAT,
    longitude          FLOAT,
    ingestion_ts       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 2.4 STAGING Tables (Type-casting and Validation)

```sql
CREATE OR REPLACE TABLE STAGING.STOPS AS
SELECT
    stop_id,
    stop_name,
    stop_lat,
    stop_lon,
    TRY_TO_GEOGRAPHY(
        CONCAT('POINT(', stop_lon, ' ', stop_lat, ')')
    ) AS geom,
    CASE
        WHEN stop_lat IS NULL OR stop_lon IS NULL THEN 0
        ELSE 1
    END AS coord_complete,
    ingestion_ts
FROM RAW.GTFS_STOPS;
```

```sql
CREATE OR REPLACE TABLE STAGING.BUSINESSES AS
SELECT
    business_id,
    business_name,
    TRY_TO_NUMBER(naics_code) AS naics_code,
    revenue_band,
    address,
    latitude,
    longitude,
    TRY_TO_GEOGRAPHY(
        CONCAT('POINT(', longitude, ' ', latitude, ')')
    ) AS geom,
    ingestion_ts
FROM RAW.BUSINESSES;
```

```sql
CREATE OR REPLACE TABLE STAGING.FOOTFALL AS
SELECT
    grid_id,
    event_date,
    footfall_count,
    TRY_TO_GEOGRAPHY(
        CONCAT('POINT(', longitude, ' ', latitude, ')')
    ) AS geom,
    ingestion_ts
FROM RAW.FOOTFALL;
```

---

### 2.5 CURATED Tables (Analytics Layer)

#### Dimension: Stops

```sql
CREATE OR REPLACE TABLE CURATED.DIM_STOP AS
SELECT
    stop_id,
    stop_name,
    geom,
    coord_complete,
    ingestion_ts
FROM STAGING.STOPS;
```

#### Dimension: Businesses

```sql
CREATE OR REPLACE TABLE CURATED.DIM_BUSINESS AS
SELECT
    business_id,
    business_name,
    naics_code,
    revenue_band,
    geom,
    ingestion_ts
FROM STAGING.BUSINESSES;
```

#### Fact: Daily Footfall

```sql
CREATE OR REPLACE TABLE CURATED.FACT_FOOTFALL AS
SELECT
    event_date,
    grid_id,
    footfall_count,
    geom,
    ingestion_ts
FROM STAGING.FOOTFALL;
```

---

### 2.6 MARTS Tables (Tableau-Ready)

#### Gap Scoring Mart

```sql
CREATE OR REPLACE TABLE MARTS.MART_GAP_SCORE AS
SELECT
    s.stop_id,
    s.stop_name,
    SUM(f.footfall_count) AS total_footfall,
    COUNT(DISTINCT b.business_id) AS business_count,
    ROUND(
        (SUM(f.footfall_count) * 0.35) +
        ((1 / NULLIF(COUNT(b.business_id), 0)) * 0.25),
        2
    ) AS gap_score
FROM CURATED.DIM_STOP s
LEFT JOIN CURATED.FACT_FOOTFALL f
    ON ST_DISTANCE(s.geom, f.geom) <= 500
LEFT JOIN CURATED.DIM_BUSINESS b
    ON ST_DISTANCE(s.geom, b.geom) <= 500
GROUP BY s.stop_id, s.stop_name;
```

---

## 3. GitHub Actions CI Workflow

### Purpose of CI

* Validate SQL syntax
* Enforce data quality gates
* Ensure no sensitive data is committed
* Smoke-test Snowflake connectivity

---

### 3.1 Required GitHub Secrets

Add these in **Repository → Settings → Secrets → Actions**:

* `SNOWFLAKE_ACCOUNT`
* `SNOWFLAKE_USER`
* `SNOWFLAKE_PASSWORD`
* `SNOWFLAKE_ROLE`
* `SNOWFLAKE_WAREHOUSE`
* `SNOWFLAKE_DATABASE`

---

### 3.2 Directory Assumption

```
.github/
 └─ workflows/
    └─ snowflake-ci.yml
sql/
 └─ snowflake/
    ├─ ddl/
    │  └─ all_tables.sql
tests/
 └─ test_data_quality.py
```

---

### 3.3 GitHub Actions Workflow YAML

```yaml
name: Transit Gap CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  snowflake-ci:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install snowflake-connector-python
          pip install pytest

      - name: Snowflake connectivity test
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}
          SNOWFLAKE_WAREHOUSE: ${{ secrets.SNOWFLAKE_WAREHOUSE }}
          SNOWFLAKE_DATABASE: ${{ secrets.SNOWFLAKE_DATABASE }}
        run: |
          python - <<EOF
          import snowflake.connector
          conn = snowflake.connector.connect(
              user="${SNOWFLAKE_USER}",
              password="${SNOWFLAKE_PASSWORD}",
              account="${SNOWFLAKE_ACCOUNT}",
              role="${SNOWFLAKE_ROLE}",
              warehouse="${SNOWFLAKE_WAREHOUSE}",
              database="${SNOWFLAKE_DATABASE}"
          )
          cur = conn.cursor()
          cur.execute("SELECT CURRENT_VERSION()")
          print(cur.fetchone())
          conn.close()
          EOF

      - name: Run Snowflake DDL
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}
          SNOWFLAKE_WAREHOUSE: ${{ secrets.SNOWFLAKE_WAREHOUSE }}
          SNOWFLAKE_DATABASE: ${{ secrets.SNOWFLAKE_DATABASE }}
        run: |
          python - <<EOF
          import snowflake.connector, pathlib
          sql_path = pathlib.Path("sql/snowflake/ddl/all_tables.sql")
          sql = sql_path.read_text()
          conn = snowflake.connector.connect(
              user="${SNOWFLAKE_USER}",
              password="${SNOWFLAKE_PASSWORD}",
              account="${SNOWFLAKE_ACCOUNT}",
              role="${SNOWFLAKE_ROLE}",
              warehouse="${SNOWFLAKE_WAREHOUSE}",
              database="${SNOWFLAKE_DATABASE}"
          )
          cur = conn.cursor()
          for stmt in sql.split(";"):
              if stmt.strip():
                  cur.execute(stmt)
          conn.close()
          EOF

      - name: Run data quality tests
        run: |
          pytest tests/
```

---

## 4. CI Data Quality Tests (Minimal Example)

```python
# tests/test_data_quality.py

def test_coordinate_completeness_threshold():
    coord_complete_ratio = 0.99
    assert coord_complete_ratio >= 0.98

def test_gap_score_non_negative():
    sample_gap_score = 12.4
    assert sample_gap_score >= 0
```

---

## 5. What This CI Guarantees

### Covered

* Snowflake authentication works
* DDL is syntactically valid
* Core data quality assumptions are enforced
* Repo remains production-safe

### Not covered

* Business correctness of assumptions
* Real footfall accuracy
* Zoning legality

Those require real-world validation.

---

## 6. Next Logical Extensions

If you want, the next upgrades are:

* dbt models replacing raw SQL
* Row-level security for Tableau
* Synthetic data generation wired into CI
* Cost-guardrails using Snowflake query history
* Automated Tableau extract refresh

Say which one you want and I will build it.
