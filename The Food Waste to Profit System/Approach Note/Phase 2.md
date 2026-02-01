# **Phase 2: Centralized Analysis & Insight Generation**
## **"Operation Deep Dive"**

**Document Type:** Technical & Analytical Specification
**Phase Status:** **Planned (Months 3-4)**
**Primary Tool:** Power Query (ETL) $\rightarrow$ SQL Express (Storage) $\rightarrow$ Excel/Power BI (Visualization)
**Objective:** Variance Decomposition and Root Cause Identification

---

### **1.0 Strategic Intent: The Move to Intelligence**
In Phase 1, we successfully compelled 150 kitchen staff to generate data. However, 15 isolated spreadsheets on a SharePoint drive do not constitute an "Enterprise Asset"—they constitute **Administrative Noise**.

**The Phase 2 Mandate:**
1.  **Consolidate:** Create a Single Source of Truth (SSOT) by merging disparate files.
2.  **Enrich:** Attach financial values ($) to physical volumes (lbs/kg).
3.  **Diagnose:** Deconstruct the "Variance." We must mathematically distinguish between **Process Failure** (Kitchen behavior) and **Procurement Failure** (Supply chain/Contracting).

> **The output of Phase 2 is not a "Dashboard." It is a "Verdict." We are determining exactly which processes will be culled or modified in Phase 3.**

---

### **2.0 The Data Engineering Architecture (Crawl/Walk Stage)**

We resist the urge to buy enterprise cloud warehouses immediately. We will utilize a "Hybrid Architecture" leveraging existing Microsoft tooling to minimize cost while maximizing structural rigour.

#### **2.1 Step 1: Ingestion & Harmonization (Power Query)**
**The Engine:** Excel Power Query (M Language).
**The Source:** `SharePoint/.../Incoming_Data/`
**The Logic:**
1.  **Directory Scan:** Point Power Query to the root folder. Filter for `*.xlsx` excluding `~$*` (temp files).
2.  **Schema Enforcement:**
    *   Use `Table.Combine` to stack the files.
    *   **Strict Typing:** Force `Date` column to Date format (ISO 8601). Force `Quantity` to Decimal. *Any row failing type-conversion is dumped to an "Error Table" for review.*
3.  **The UOM Standardization Layer:**
    *   *Problem:* Store A logs "5.0 lbs". Store B logs "2.25 kgs".
    *   *Solution:* Conditional Logic implemented in M:
        ```powerquery
        if [UOM] = "LB" then [Quantity] * 0.453592 else [Quantity] 
        --> Output Column: [Quantity_KG_Normalized]
        ```

#### **2.2 Step 2: Financial Enrichment (The Cost Injection)**
Raw waste logs contain volume, not value.
*   **External Data Source:** `Master_Ingredient_Price_List.csv` (Exported monthly from ERP/Purchasing).
*   **Join Logic:** Left Outer Join on `Item_Name`.
*   **The Calculation:** `Estimated_Cost` = `[Quantity_KG_Normalized]` * `[Standard_Cost_Per_KG]`.
*   **Gap Analysis:** If `Estimated_Cost` returns NULL (due to spelling errors, e.g., "Avocados" vs "Avocado Haas"), the row is flagged `Unknown Cost` but preserved for volume analysis.

#### **2.3 Step 3: Storage (The SQL Foundation)**
We will load the cleaned dataset into a **Local SQL Server Express** or **PostgreSQL** instance to enable complex queries that Excel cannot handle efficiently.

**Target Schema (`FACT_WASTE`):**
```sql
CREATE TABLE waste_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    transaction_uuid UNIQUEIDENTIFIER, -- Lineage back to source file
    restaurant_id VARCHAR(10) NOT NULL, -- e.g. 'SB-05'
    log_date DATE NOT NULL,
    day_part VARCHAR(20), -- 'Lunch', 'Dinner', 'Prep' (Derived from Time)
    item_code VARCHAR(50), 
    category_code VARCHAR(10), -- 'PREP', 'COOK', 'SPOIL'
    reason_code VARCHAR(10), -- 'OP', 'EXP', 'HE'
    quantity_kg DECIMAL(10,3), -- The Source of Truth for VOLUME
    cost_usd DECIMAL(10,2),    -- The Source of Truth for VALUE
    ingest_timestamp DATETIME DEFAULT GETDATE()
);
```

---

### **3.0 Analytical Framework: The Three Pillars**

We will run three specific forensic analyses to identify the "Pareto Principles" of our waste (80% of costs coming from 20% of sources).

#### **3.1 Pillar A: Attribution Analysis (The "Why")**
*Business Question:* Is this a supplier problem (Spoilage) or a kitchen problem (Over-Prep)?

*   **Query Focus:** Group by `Reason_Code` and `Category`.
*   **Expected Insight:**
    *   If **Spoilage > 50%**, we trigger Phase 3 "Procurement Negotiations."
    *   If **Over-Prep/Cook Error > 50%**, we trigger Phase 3 "Operational SOP Changes."
*   *Preliminary Hypothesis:* Based on casual observation, we expect "Over-Preparation" (Behavioral) to be the dominant cost driver.

#### **3.2 Pillar B: Item Pareto Analysis (The "What")**
*Business Question:* We waste 100 different items. Which 5 matter?

*   **Query Focus:** `SELECT TOP 5 item_name FROM waste_log ORDER BY sum(cost_usd) DESC`.
*   **The Matrix:** We plot items on a 2x2 matrix:
    *   **High Freq / Low Cost:** (e.g., Rice, Fries). *Fix:* Batch Prep Rules.
    *   **Low Freq / High Cost:** (e.g., Steaks, Seafood). *Fix:* Inventory par-level reduction.
*   *The "Fry Insight":* We will run time-series analysis on "Fries." If waste spikes at 14:00 (end of lunch), it confirms "Batching Abuse" (Cooks dropping full baskets right before the rush ends).

#### **3.3 Pillar C: Performance Normalization (The "Who")**
*Business Question:* Which Manager is actually failing?

*   **The Trap:** Comparing absolute dollars. (Store #1 in Times Square will always waste more dollars than Store #15 in the suburbs).
*   **The Solution:** Relative Performance Metrics.
    *   **Metric 1:** `Waste %` = `Total_Waste_USD` / `Total_Sales_USD` (Joined from POS Data).
    *   **Metric 2:** `Waste per Cover` = `Total_Waste_KG` / `Guest_Count`.
*   **Output:** A "League Table" ranking the 15 stores from Best to Worst Efficiency. This creates the psychological leverage for Phase 3 gamification.

---

### **4.0 Data Quality Assurance (The "Sniff Test")**

Before presenting to the C-Suite, we check for "Malicious Compliance."

**The Integer Test:**
```sql
SELECT count(*) FROM waste_log 
WHERE quantity_input IN (1.00, 2.00, 5.00, 10.00);
```
*   *Logic:* Real measurements are messy (e.g., `1.24 lbs`, `4.85 lbs`). If a store's data is 90% perfect integers (`5.00 lbs`), they are not weighing food—they are guessing. We mark this store's data as **Low Confidence** and exclude it from the regional baseline.

---

### **5.0 Success Metrics & Deliverables**

By the end of Phase 2, we will deliver:

1.  **The "Verdict" Deck:** A concise report for the COO outlining:
    *   The "Big Three" wasted items (Volume & Value).
    *   The "Primary Bleed" (Is it Spoilage or Process?).
    *   The "Efficiency Ranking" of all 15 General Managers.
2.  **The Target Savings Number:** A revised financial goal.
    *   *Example:* "We have identified $22,000/month in actionable over-prep waste. We target capturing 60% of this ($13.2k/month) in Phase 3."
3.  **The Phase 3 Blueprint:** Specific recommendations (e.g., "Implement Cook-to-Order SOPs for French Fries between 2 PM and 5 PM").

---

> [!Tip]
> **Technical Note for Analysts**
> Do not obsess over the 1% "Long Tail" of waste (e.g., parsley garnish, spices). We are hunting Elephants, not Flies. If an item constitutes less than 1% of total waste cost, group it into "Other" and move on. Speed of insight is more valuable here than 100% granular perfection.
