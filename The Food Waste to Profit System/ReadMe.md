# Project Phoenix Bible: Operational Optimization and Waste Reduction

**Client:** SavoryBites Restaurant Chain
**Project Lead:** Data Architecture & Transformation Office
**Version:** 1.0 (FINAL)
**Status:** Approved for Execution

---

## **1. Executive Summary**

### **1.1 Overview**
Project Phoenix is a strategic transformation initiative designed for SavoryBites, a chain of 15 casual dining restaurants. The project addresses a critical inefficiency in current operations: **Food Waste**. Historically treated as an "unavoidable cost of doing business," food waste actually represents a significant leakage of net profit, impacting Cost of Goods Sold (COGS), labor efficiency, and corporate sustainability goals.

Currently, SavoryBites relies on managerial intuition and isolated Point-of-Sale (POS) data, which tracks *sales* but fails to track *loss*. There is no standardized measurement framework.

### **1.2 Objectives**
The primary objectives of Project Phoenix are:
1.  **Quantify:** Transition from intuition to empirical evidence regarding waste volume and value.
2.  **Reduce:** Achieve a **25% reduction** in food waste costs within 12 months.
3.  **Monetize:** Identify and validate at least one revenue stream or direct cost-saving partnership (circular economy) derived from waste products.
4.  **Standardize:** Create a replicable, data-driven operational model for kitchen efficiency.

### **1.3 Strategy Summary**
The project will follow a four-phase maturity model:
*   **Phase 1 (Manual Audit):** Establishing the baseline using low-barrier tools (Excel) to generate culture shock and initial data.
*   **Phase 2 (Insight):** Centralizing data via SQL to identify root causes (Variance Analysis).
*   **Phase 3 (Action):** Operationalizing changes in the kitchen and piloting waste diversion (Animal Feed).
*   **Phase 4 (Scale & Value):** Implementing Power BI for automated reporting, gamification, and high-value circular economy partnerships.

---

## **2. Business Context and Problem Statement**

### **2.1 The Economics of Restaurant Waste**
In the casual dining sector, net profit margins often hover between 3% and 9%. Food Cost (COGS) typically accounts for 28-32% of total revenue.
*   **The Problem:** Every dollar of food waste is a dollar of **pure loss**. It includes the cost of the raw ingredient, the labor cost to prep it, the energy cost to store/cook it, and the disposal cost to haul it away.
*   **The Multiplier:** Saving $1 in waste is financially equivalent to generating $10-$15 in new sales (assuming a profit margin of 6-10%).

### **2.2 Current Operational Gaps**
SavoryBites currently suffers from:
1.  **Inventory Blindness:** We know what we bought (invoices) and what we sold (POS), but the gap between the two (Shrinkage/Waste) is opaque.
2.  **Cultural Acceptance:** Staff view throwing away food as "closing duties" rather than "burning cash."
3.  **Siloed Operations:** Restaurant A might have solved a spoilage issue that Restaurant B is still suffering from, with no mechanism to share that knowledge.

### **2.3 Stakeholders and Personas**

| Stakeholder Group | Persona | Pain Points | Success Metric |
| :--- | :--- | :--- | :--- |
| **Executive Leadership** | *Sarah (COO)* | Shrinking margins, investor pressure on ESG. | Margin improvement by 0.5-1%. |
| **Regional Managers** | *Mike (Regional Dir.)* | Cannot monitor 5 kitchens at once; relies on excuses from GMs. | Real-time visibility into outlier locations. |
| **General Managers** | *Elena (Store GM)* | Overwhelmed by admin work; feels attacked by "cost cutting." | Tools that make inventory ordering easier. |
| **Kitchen Staff** | *Line Cooks/Preps* | "Logging waste slows me down." Fear of punishment. | Simplified workflow; less prep work required. |


## 2.1 The Macro-Economic Landscape: Why This Matters Now

To understand the necessity of Project Phoenix, we must first contextualize SavoryBites within the broader harsh reality of the mid-2020s casual dining industry. The era of cheap ingredients, abundant labor, and forgiveness for operational inefficiency is over.

### 2.1.1 The Inflationary Vise
The restaurant industry is currently caught in an "Inflationary Vise."
*   **Input Cost Surge:** Wholesale food prices have risen 22% over the last 24 months. The price of fryer oil alone has fluctuated by 80% due to supply chain disruptions.
*   **Price Elasticity Limit:** We have raised menu prices by 12% over two years. Customer sentiment analysis shows we are reaching a "resistance point." Further price hikes will drive customers to fast-casual competitors (e.g., Chipotle) or grocery stores.
*   **Result:** We cannot raise prices fast enough to cover costs. The only lever remaining to preserve margin is **Operational Efficiency**, specifically Yield Management (Cost of Goods Sold optimization).

### 2.1.2 The Environmental Mandate
The cultural tolerance for waste has vanished.
*   **Legislative Pressure:** Municipalities in three of our operating regions (California, Massachusetts, New York) have introduced or are introducing strict organic waste bans from landfills. "Tipping fees" (the cost to dump trash) have tripled in 5 years, with surcharges for heavy organic matter.
*   **Consumer Demand:** Our demographic (Families, Millennials, Gen Z) lists "Sustainability" as a Top 3 factor in brand affinity. A viral social media post showing a SavoryBites dumpster full of edible food could be a reputation-killing event.

---

## 2.2 Company Profile: SavoryBites Inc.

**Overview:**
SavoryBites is a 15-unit chain positioning itself in the "Polished Casual" segment. We are not fine dining, but we are a step above a generic diner. We emphasize "Fresh ingredients, Scratch-made sides, Family Atmosphere."

*   **Locations:** 15 units (Mixed Suburban/Urban).
*   **Average Annual Revenue (AAR):** $3.2 Million per unit ($48M Total System Revenue).
*   **Menu Profile:** American Comfort (Burgers, Rotisserie Chicken, Ribs, Elaborate Salads).
*   **Operational Style:** High-prep. We cut our own fries, we bread our own onion rings, and we simmer our own stocks.
*   **Current Margin Profile:**
    *   **Ideal Food Cost:** 29.0% (Theoretical cost based on recipes).
    *   **Actual Food Cost:** 33.5% (What we actually spend).
    *   **The Gap:** **4.5%**.

**The Multi-Million Dollar Leak:**
A 4.5% gap on $48M revenue equals **$2.16 Million** annually evaporating from the supply chain. This is not "cost of business"; this is the equivalent of running one restaurant specifically to burn cash.

---

## 2.3 The Pathology of Waste: Detailed Scenarios

To solve the problem, we must see the problem. Waste at SavoryBites is not a single event; it is a pervasive, silent accumulation of small errors. Below are the three primary "infection vectors" identified during preliminary site visits.

### Scenario A: The "Just-in-Case" Paranoia (Pre-Consumer Waste)
**Location:** Store #04 (Suburban Mall Anchor)
**Time:** Tuesday, 10:30 AM (Prep Shift)
**Actor:** Marcus, Kitchen Manager (KM)

**The Context:**
Marcus was yelled at three weeks ago because the kitchen ran out of Mashed Potatoes during a surprise Saturday rush. He swore "never again."

**The Incident:**
1.  **Prediction Failure:** Marcus looks at the forecast. It predicts a slow Tuesday lunch ($800 sales forecast). However, deeply traumatized by the outage, he intuitively "buffers" the prep list.
2.  **The Action:** The recipe calls for 10lbs of potatoes. Marcus preps 25lbs.
3.  **The Reality:** Tuesday lunch is slow, as predicted. They sell 8lbs of mashed potatoes.
4.  **The Shelf Life:** Fresh mashed potatoes have a quality shelf life of 4 hours under heat lamps or 24 hours refrigerated.
5.  **The Outcome:** The crew saves 5lbs for dinner. They reheat it at 5 PM. It forms a crust. The texture is off. The Dinner Manager, adhering to quality standards, throws the 5lbs away. The remaining 12lbs in the fridge turns gray by Wednesday morning.
6.  **The Loss:**
    *   **Ingredient:** 17lbs of Potatoes ($15 cost).
    *   **Labor:** 20 mins of peeling/boiling labor ($6).
    *   **Energy:** Gas used to boil water ($2).
    *   **Disposal:** Weight added to dumpster ($1).
    *   **Total Loss:** $24 for one item, on one shift, in one store.
    *   **Scale:** Multiply by 15 stores x 365 days x 10 items. This behavior is systemic.

### Scenario B: The "Visual Variance" (Production Waste)
**Location:** Store #12 (Downtown District)
**Time:** Friday, 7:00 PM (Peak Rush)
**Actor:** Sarah, Fry Cook (New Hire)

**The Context:**
The "Savory Stack" Onion Rings are a signature item. They are supposed to be a pyramid of 8 rings.

**The Incident:**
1.  **Training Gap:** Sarah was rushed through onboarding. She relies on "visual" measurement rather than scales.
2.  **The Action:** Sarah grabs a "handful" of breaded rings for every order. Because she wants the customer to be happy (and doesn't want the server to complain the portion looks small), she errs on the side of generosity. She serves 10-11 rings per order instead of 8.
3.  **The Math:** This is a **25% over-portioning variance**.
4.  **The Invisibility:** This is the most dangerous type of waste because it does *not* go in the trash can. It goes out the front door. It is invisible to a "Garbage Log." It only shows up when the P&L comes out at the end of the month and the manager asks, "Why did we buy 100 bags of onions but only sell 80 bags worth of rings?"
5.  **The Financial Hit:** We just gave away 25% of our inventory for free.

### Scenario C: The "Logistics Mismatch" (Spoilage Waste)
**Location:** Store #07 (University Town)
**Time:** Monday, 8:00 AM (Delivery Day)
**Actor:** Elena, General Manager

**The Context:**
Our primary bread supplier, *Grains & Co*, has a Minimum Order Quantity (MOQ). They sell Brioche buns in cases of 144.

**The Incident:**
1.  **The Need:** Store #07 needs roughly 80 buns for the Mon-Wed period based on historical sales.
2.  **The Constraint:** Elena cannot order 80. She must order 144.
3.  **The Storage:** The freezer is packed with frozen chicken (due to a separate bulk buy deal). Elena leaves the bread on the dry rack.
4.  **The Mold:** By Thursday morning, humidity in the kitchen causes mold spots on the remaining 40 buns.
5.  **The Disposal:** The entire bag goes into the dumpster.
6.  **The Interpretation:** Corporate sees this as "Poor inventory management by Elena." In reality, it is a **Procurement Contract Failure**. We are buying bulk to save pennies per unit, but losing dollars per case in spoilage.

---

## 2.4 Financial Forensic Audit: The Cost of Doing Nothing

The Board of Directors often focuses on Top-Line Growth (Sales). Project Phoenix argues that Bottom-Line Hygiene (Cost) is where the enterprise value lies.

### 2.4.1 The Profit & Loss Statement (Monthly Average per Store)

| Line Item | Value ($) | % of Sales | Note |
| :--- | :--- | :--- | :--- |
| **Gross Sales** | **$266,000** | **100%** | |
| Cost of Goods Sold (Actual) | $(89,110) | 33.5% | |
| *Target COGS (Theoretical)* | *$(77,140)* | *29.0%* | *Based on Recipes* |
| **COGS Variance (WASTE)** | **$(11,970)** | **4.5%** | **The Opportunity** |
| Labor | $(85,120) | 32.0% | |
| Rent & Utilities | $(26,600) | 10.0% | |
| Marketing & Admin | $(13,300) | 5.0% | |
| **EBITDA (Current)** | **$51,870** | **19.5%** | |
| **EBITDA (Potential)** | **$63,840** | **24.0%** | **If Waste = 0** |

**Interpretation:**
*   We are losing nearly **$12,000 per month per store** to inefficiency.
*   Across 15 stores, that is **$180,000 per month** ($2.16M Annual).
*   **The Project Goal:** We are targeting a 25% reduction in that variance ($3,000/month/store savings).
*   **Net Impact:** This would add **$540,000** of pure profit to the bottom line annually.
*   **Valuation Impact:** At a standard 8x EBITDA multiple, Project Phoenix adds **$4.3 Million** to the company's enterprise valuation.

### 2.4.2 The "Hidden Costs" of Waste
The $11,970 monthly figure above is *only* the food cost. It does not calculate the collateral damage.

1.  **The Labor Multiplier:** We pay a prep cook $18/hour to slice vegetables. If 20% of those vegetables end up in the trash, we effectively paid the cook $18/hour to manufacture garbage.
2.  **The Utility Load:** Cooking food that nobody eats wears down fryers, uses gas, uses water for dishwashing, and burns electricity for HVAC to cool the kitchen.
3.  **Disposal Fees:** Waste management contracts are rising. We pay per "pull" (dumpster empty). Heavier bins (wet food waste) lead to overage charges.
    *   *Current Spend:* $1,200/month/store on Trash Removal.
    *   *Est. Reduction:* $200/month/store if volume decreases by 30%.

---

## 2.5 Operational Diagnostics: Why the Current System Fails

Why haven't we fixed this yet? Because our current operational infrastructure is built to *facilitate* waste, not prevent it.

### 2.5.1 The Blind Point-of-Sale (POS) System
*   **Tool:** Legacy Micros/Aloha System.
*   **The Flaw:** The POS tracks **Sales**. It does not track **Consumption**.
*   **Example:** A customer orders a Burger (No Tomato). The POS tells the kitchen "Burger - No Tom." The server presses the button.
    *   *But:* Did the inventory system deduce 1 tomato? Or 0?
    *   *Reality:* The inventory module is hard-coded to deduct 1 tomato for every burger sold, regardless of modification. Our theoretical inventory is permanently out of sync with physical reality.
    *   **Result:** Managers stop trusting the system ("The computer says we have 50 tomatoes, I see 0, so the system is broken"). They revert to gut-feeling ordering.

### 2.5.2 The "Sheet to Shelf" Disconnect
*   **Tool:** Weekly Inventory Excel Sheets.
*   **Process:** Every Sunday night, managers physically count every item in the store.
*   **The Flaw:** This tells us the **End State** (What we have left) but not the **Flow** (How we lost it).
    *   We started with 100. We bought 100. We have 50 left. We sold 100.
    *   Math: 100 (Start) + 100 (Buy) - 100 (Sold) = Should have 100.
    *   Reality: Have 50. Missing 50.
    *   *The Black Box:* Did those 50 rot? Were they stolen? Did the cook drop them? Did the supplier short-change the delivery?
    *   **Analysis:** Without a *daily waste log*, the Sunday Night Inventory count is just an autopsy. It tells us the patient died, but not what killed him.

### 2.5.3 The Human Factor: Psychology of the Kitchen
*   **Fear of "86":** The greatest sin in a restaurant is "86-ing" (running out of) a menu item on a Friday night. It upsets guests and stresses servers.
*   **The Consequence:** Managers are incentivized to **Over-Order**.
    *   Manager Logic: *"If I throw away $50 of lettuce, Corporate might yell at me next month. If I run out of lettuce tonight, the General Manager will yell at me immediately."*
    *   **Strategic Shift Needed:** Project Phoenix must make Waste as visible and painful as "86-ing."

---

## 2.6 Stakeholder Personas & Resistance Mapping

Successful implementation requires navigating the political and emotional landscape of SavoryBites.

### Persona 1: Sarah, The Regional Director
*   **Motivation:** Her quarterly bonus is tied to "Controllable Profit."
*   **Pain Point:** She manages 5 stores. She cannot physically be in every kitchen watching the garbage cans.
*   **Attitude towards Project Phoenix:** **Champion.** She wants data to hold her General Managers (GMs) accountable.
*   **Risk:** She may use the data as a "blunt object" to punish GMs, causing a mutiny. We must train her to use data for coaching, not just policing.

### Persona 2: Chef Marco, The "Old Guard" Kitchen Manager
*   **Motivation:** Pride in food quality. Loves cooking, hates paperwork.
*   **Pain Point:** Finds Excel spreadsheets insulting to his craft.
*   **Attitude towards Project Phoenix:** **Detractor.** *"You want me to weigh potato peels? Do you want good food or do you want me to be an accountant?"*
*   **Mitigation Strategy:** The process must be low-friction. The "Why" must be explained in culinary terms (respecting the ingredient), not just financial terms.

### Persona 3: Elena, The Overwhelmed GM
*   **Motivation:** Getting home before midnight.
*   **Pain Point:** She already spends 2 hours a day on admin.
*   **Attitude:** **Skeptic.** Sees this as "More work from Corporate."
*   **Success Criterion:** If Project Phoenix can streamline her Sunday inventory counts (by making stock levels more predictable), she will adopt it.

---

## 2.7 The Problem Summary: The "Data Desert"

We are currently operating a multi-million dollar supply chain based on **intuition** and **lagging indicators**.

1.  **No Granularity:** We know *Cost* is high, but we don't know if it's Meat, Produce, or Dairy.
2.  **No Timeliness:** We find out about waste 30 days after it happens (Monthly P&L).
3.  **No Root Cause:** We cannot distinguish between "Bad Training" (Cook cuts peppers wrong) and "Bad Purchasing" (Manager buys too many peppers).
4.  **No Accountability:** Because there is no record of *who* threw the food away, there is no ownership.

## 2.8 The Interpretation: Formulating the Battle Plan

Project Phoenix is not just an IT project; it is an Operational Transformation. We interpret these challenges into a phased plan of attack.

### Challenge 1: "We don't know what we don't know."
*   **Plan (Phase 1):** The Manual Audit. We must forcefully inject measurement into the workflow. We accept that manual logging is annoying, but it serves to shock the system and create the initial dataset. It moves the conversation from "I think we waste food" to "We wasted 42kg of Fries yesterday."

### Challenge 2: "Data requires Analysis."
*   **Plan (Phase 2):** Centralization. Isolated spreadsheets are useless. We need to aggregate the data to find the "Red Flags." This requires SQL and comparative analytics to spot that Store A wastes Fries while Store B wastes Bread.

### Challenge 3: "Knowledge isn't Action."
*   **Plan (Phase 3):** Operational Pivot. Data must change physical behavior.
    *   *Insight:* "Fries are wasted at 3 PM."
    *   *Action:* Change the Prep Chart.
    *   *Circular Economy:* We must solve the "Inevitable Waste" (Peels/Shells). This requires external partnerships (Farm Pilot).

### Challenge 4: "Sustainability must Scale."
*   **Plan (Phase 4):** Automation & Culture. We cannot rely on manual logs forever. We must verify the ROI to fund IoT scales and use Dashboards (Power BI) to make waste reduction a competitive game between stores.

---

### **Conclusion of Business Context**
The survival of SavoryBites' profit margin depends on closing the gap between *what we buy* and *what we sell*. We are currently bleeding $2M+ annually into landfills. This is a fixable operational failure. Project Phoenix provides the methodology to cauterize this wound, recover lost capital, and position the brand for the sustainable future.

**We proceed immediately to Phase 1.**

---

>[!warning]
>**Assumption Check for Project Team**
>The financial modeling above assumes a standard ingredient mix. If the price of Protein (Beef/Chicken) spikes disproportionately in Q3, the savings target ($100k) may be obscured by inflation. We must track "Volume of Waste" (Kg) as the primary metric of success, with "Cost of Waste" ($) as the secondary financial outcome, to control for market price volatility.

---
# Project Phoenix Bible
## Section 3: Architecture and Data Strategy Overview

**Document Owner:** Chief Data Architect
**Date:** October 15, 2024
**Scope:** Technical Architecture, Data Modeling, Integration Strategy, and Roadmap
**Status:** Approved for Design
**Version:** 1.0

---

## 3.0 Architectural Philosophy: The "Anti-Fragile" Approach

### 3.0.1 The Trap of Over-Engineering
In typical enterprise data projects, there is a temptation to purchase the "Ferrari" immediately—implementing Snowflake, Databricks, or a Kafka streaming layer on Day 1. For Project Phoenix at SavoryBites, this would be a catastrophic failure.

Why? **Because the data source (Human Behavior) is currently unstable.**

We are asking line cooks, who are under immense physical pressure, to manually log waste. If we build a rigid, high-tech API-driven architecture before we have established the *discipline* of data collection, the system will ingest garbage data at the speed of light.

### 3.0.2 The Crawl-Walk-Run Imperative
Our architectural strategy is defined by the **Maturity Model**. We will match the complexity of our technology to the maturity of our operational processes.

1.  **Crawl (Manual Audit):** Low tech, high touch. We validate the *existence* of data.
2.  **Walk (Centralization):** Moderate tech. We validate the *consistency* of data.
3.  **Run (Cloud Integration):** High tech. We automate the *flow* of data.
4.  **Fly (IoT & ML):** Cutting edge. We automate the *decision-making*.

---

## 3.1 Detailed Technical Stack Lifecycle

We will progressively migrate the technical estate. The architecture is designed so that each phase provides the foundation for the next; nothing is "throw-away" work; it is "prototype" work that informs the final schema.

| Component | **Phase 1: The Paper & Excel Era** | **Phase 2: The Aggregation Era** | **Phase 3: The Cloud Foundation** | **Phase 4: The Enterprise State** |
| :--- | :--- | :--- | :--- | :--- |
| **Duration** | Months 1-2 | Months 3-4 | Months 5-8 | Months 9+ |
| **Data Generation** | Analog Scales + Paper Clipboards. Manual entry into Store PC. | Direct entry into constrained Excel Templates on Managers' tablets. | Digital Web Form / PowerApps or continued Excel (Standardized). | IoT Smart Bins (Winnow/Leanpath) + API Feeds. |
| **Ingestion** | Manager types paper log into local Excel file. | Power Query scans SharePoint folders nightly. | Azure Data Factory (ADF) Ingestion pipelines. | Real-time JSON Event Streams (Event Hubs). |
| **Storage** | Local Files (CSV/XLSX) stored on SharePoint (Silos). | Local SQL Express or consolidated CSVs. | Azure SQL Database (Central Warehouse). | Cloud Data Warehouse (Snowflake or Azure Synapse). |
| **Transformation** | Manual Excel formulas (`SUMIF`, `VLOOKUP`). | Power Query M Scripts / Simple SQL Views. | Stored Procedures / DBT (Data Build Tool). | Automated ETL pipelines with anomaly detection. |
| **Reporting** | Static Monthly Email (PDF) sent by Analyst. | Ad-Hoc SQL Queries / Excel Pivot Tables. | Power BI Pro (connected to SQL DB). | Embedded Analytics & Predictive Models. |
| **Key Risk** | Data Entry Errors (Typos). | File Version Conflicts. | Latency / Connectivity. | Hardware Maintenance & Calibration. |

---

## 3.2 Phase 1 Architecture: "Iron-Clad Excel" (The Crawl)

**Objective:** Standardize input data to minimize "Cleaning" time later.

In Phase 1, the "Architecture" is essentially a rigorous File System governance policy. If 15 managers name their files differently, the project fails.

### 3.2.1 The Distributed File System (SharePoint)
We will leverage the existing Microsoft 365 license.

**Directory Structure:**
```text
/SavoryBites_Corp/
  /Operations/
    /Project_Phoenix/
      /Incoming_Data/
        /Region_East/
          /Store_01_Boston/
            - 2024-11_Waste_Log_Store01.xlsx
            - 2024-12_Waste_Log_Store01.xlsx
        /Region_West/
          ...
```

### 3.2.2 The Collection Instrument (The Spreadsheet)
We cannot rely on a blank spreadsheet. It must be an **Application** built within Excel.

**Feature Specification: `Master_Waste_Log_Template_v1.xlsx`**
1.  **Worksheet 1: `Entry_Log`**:
    *   **Data Validation:** Columns C, D, and E (Item, Category, Reason) will *not* allow free text. They will reference named ranges in the `Reference_Data` sheet.
    *   **Error Trapping:** The `Quantity` column is set to "Decimal" type. If a user types "5 lbs" (text), Excel rejects the input. It must be `5`.
    *   **Conditional Formatting:** If a user enters a quantity > 50kg (unlikely), the cell turns bright red to prompt a double-check (sanity check).

2.  **Worksheet 2: `Reference_Data` (Locked/Hidden)**:
    *   This sheet contains the "Golden Records" exported from our master systems.
    *   **Master Item List:** Copied from our Sysco/US Foods Order Guide. Contains `SKU`, `Item_Name`, `Purchase_UOM`, `Unit_Cost`.
    *   **Store List:** List of Store IDs.

**VBA Automation (Optional but Recommended):**
*   A simple "Submit" button macro that saves a timestamped CSV backup to a separate "Archive" folder, ensuring that if the Manager corrupts the main file, we have a history.

---

## 3.3 Phase 2 Architecture: The Integration Logic (The Walk)

**Objective:** Remove the human effort of opening 15 files to make a report.

### 3.3.1 The Aggregation Engine: Power Query (M Language)
We will create a **Master Analysis Workbook**. It does not contain data; it contains *connections*.

**The Pipeline Logic:**
1.  **Source:** `Folder.Files("https://savorybites.sharepoint.com/.../Incoming_Data/")`
2.  **Filter:** Select only `.xlsx` files. Exclude files beginning with `~` (temp files).
3.  **Transform:**
    *   `Table.Combine`: Stacks 15 files into one massive table.
    *   `Table.AddColumn`: Extracts "Store ID" from the folder path or filename.
    *   `Type.Conversion`: Forces strict data typing (Date as Date, Cost as Currency).
4.  **Lookup Enrichment:**
    *   Merge queries with the `Master_Ingredient_Price_List.csv` based on Item Name.
    *   *Note:* In Phase 1, cost was manual. In Phase 2, we centrally control cost to ensure consistency.

### 3.3.2 The Intermediate Database (SQL Express)
Towards the end of Phase 2, as row counts exceed 50,000, Excel performance will degrade. We will deploy a lightweight PostgreSQL or SQL Server Express instance on a secure corporate VM.

*   **Ingestion Script:** A simple Python script (pandas) or PowerShell script runs nightly.
    *   *Action:* Truncate the daily staging table -> Bulk Insert new data -> Append to History table.

---

## 3.4 Phase 3 Architecture: The Cloud Warehouse (The Run)

**Objective:** Scalability, Security, and Single Source of Truth (SSOT).

We migrate from "Files on SharePoint" to a true **Modern Data Stack (MDS)**.

### 3.4.1 The Data Warehouse: Azure SQL Database
We choose a relational database (OLTP/OLAP hybrid) over a data lake for now because the data is highly structured.

**Schema Design Pattern:** Star Schema (Kimball Methodology).
This optimizes the database for *read* performance (Power BI reports) rather than *write* performance.

### 3.4.2 The Semantic Layer (Power BI Datasets)
We do not let users query the database directly. We build a governed dataset.
*   **DAX Measures:** Pre-calculated business logic.
    *   `Waste Cost` = `SUM(Waste_Fact[Estimated_Cost])`
    *   `Waste % of Sales` = `DIVIDE([Waste Cost], [Total Sales], 0)`
*   **Row-Level Security (RLS):**
    *   A General Manager logging in from "Boston #1" can *only* see data where `Location_ID = 'BOS-001'`.
    *   The Regional Manager sees all stores in `Region = 'East'`.

---

## 3.5 Conceptual Data Model: The "Phoenix Schema"

This is the most critical component. Bad code can be rewritten; bad data modeling rots the foundation forever.

We will use a **Star Schema** centered around `FACT_WASTE_TRANSACTION`.

### 3.5.1 The Fact Table (`FACT_WASTE_TRANSACTION`)
This table records the event. It is "narrow and deep."

| Field Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `Waste_ID` | BIGINT | PK, Auto-Inc | System generated unique key. |
| `Date_Key` | INT | FK | Link to Date Dimension (e.g., `20241015`). |
| `Time_Key` | INT | FK | Link to Time Dimension (Hour buckets). |
| `Store_Key` | INT | FK | Link to Store Dimension. |
| `Item_Key` | INT | FK | Link to Master Ingredient Dimension. |
| `Reason_Key` | TINYINT | FK | Link to Reason Code Dimension. |
| `Quantity_Raw` | DECIMAL(10,3) | NOT NULL | The number typed by the human. |
| `UOM_Input` | VARCHAR(10) | NOT NULL | The Unit chosen (Kg, Lbs, Case). |
| `Quantity_Standardized_Kg` | DECIMAL(10,3) | Derived | **Critical ETL Logic:** Converts Lbs/Cases to Kg. |
| `Unit_Cost_At_Disposal` | DECIMAL(10,4) | Derived | The cost of the item *on that specific day*. |
| `Total_Cost_Loss` | DECIMAL(10,2) | Derived | `Qty_Standard * Unit_Cost`. |
| `Input_Source` | VARCHAR(20) | Metadata | 'Excel', 'App', 'IoT'. Helps track data confidence. |

### 3.5.2 Dimension: Items (`DIM_ITEM`)
Handling ingredients is difficult because they change (new suppliers, seasonal items).

| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `Item_Key` | INT | Surrogate Key (Internal). |
| `SKU_Code` | VARCHAR(50) | Supplier SKU (External). |
| `Item_Name` | VARCHAR(100) | "Tomatoes, Roma". |
| `Reporting_Category` | VARCHAR(50) | "Produce", "Protein", "Dairy". |
| `Standard_Unit_Weight_Kg` | DECIMAL | *Crucial Reference:* Weight of 1 "Each" or 1 "Case". |
| `Yield_Percent` | DECIMAL | e.g., 0.85 (We lose 15% when peeling). Used for advanced cost calcs. |

::: warning
**Architectural Risk: The "Unit of Measure" Nightmare**
Kitchen staff think in "Pinches," "Bunches," and "Cases." The database thinks in Kilograms.
**The Solution:** The `DIM_ITEM` table must contain a "Conversion Factor" for every Item/UOM combination.
*   If Item = "Avocado" and Input = "Case", Logic: `Quantity * Case_Weight (10kg)`.
*   If Item = "Avocado" and Input = "Each", Logic: `Quantity * Single_Weight (0.2kg)`.
**Strict Rule:** Phase 1 Excel template will *limit* UOM choices per item. Users cannot select "Liters" for "Steaks."
:::

### 3.5.3 Dimension: Reason (`DIM_REASON`)
A small reference table, but vital for analytics.

| Field Name | Description |
| :--- | :--- |
| `Reason_Code` | Short Code (`OP`, `EXP`, `DROP`). |
| `Reason_Description` | Friendly Name ("Over Preparation", "Expired"). |
| `Controllability_Flag` | Boolean (0/1). Was this preventable? |
| `Disposition_Type` | "Landfill", "Compost", "Donation". Important for Sustainability Reporting. |

### 3.5.4 Dimension: Store (`DIM_STORE`)

| Field Name | Description |
| :--- | :--- |
| `Store_Key` | Internal ID. |
| `Store_Code` | "BOS-01". |
| `Region_Name` | "Northeast". |
| `POS_Integration_ID` | The ID used in the POS system (to join with Sales data). |
| `Square_Footage` | Useful for normalizing efficiency metrics. |

---

## 3.6 Integration Strategy (Master Data Management)

### 3.6.1 The "Sales" Context Integration (Phase 2+)
To answer "Are we wasting more when it's busy?", we need Sales Data.
*   **Source:** Micros POS daily export (CSV).
*   **Join Logic:** `FACT_SALES` linked to `DIM_DATE` and `DIM_STORE`.
*   **Metric:** `Waste_Efficiency_Ratio` = `Total_Waste_Cost` / `Total_Food_Sales`.

### 3.6.2 The Cost Ingestion
We will not manually type costs after Phase 1.
*   **Source:** ERP / Supply Chain System (e.g., Sysco/Compeat).
*   **Frequency:** Monthly average cost updates.
*   **Logic:** `FACT_WASTE` looks up the cost from `DIM_ITEM_HISTORY` based on the date of the waste.
    *   *Why?* If we wasted Chicken in January ($5/lb), we must not re-calculate that loss in June using June prices ($7/lb). History must be immutable.

---

## 3.7 Data Quality & Governance Framework

We are building a "Digital Trust" system.

### 3.7.1 Validation Rules (The "Bouncers" at the door)
1.  **Completeness:** A record with NULL `Item_ID` is rejected.
2.  **Range Checking:**
    *   Warning: Quantity > 20kg.
    *   Hard Stop: Quantity < 0.
3.  **Logical Consistency:** "Spoiled" waste cannot be "Plate Waste" (Customer side).

### 3.7.2 Outlier Detection (The "Smoke Alarm")
*   **Logic:** During ETL, calculate `Mean` and `Standard_Deviation` for daily waste weight per store.
*   **Trigger:** If `Daily_Waste` > (`Mean` + 3 * `StdDev`), flag row as `Audit_Required`.
*   **Action:** Email alerts the Regional Manager. "Store #4 just logged 500kg of waste. Typo or Disaster?"

---

## 3.8 Phase 4: Future State IoT & Automation

Though currently a Roadmap item, the architecture supports the transition.

### 3.8.1 The Smart Scale Integration
Smart bins (like Winnow) emit JSON payloads via REST API.

**Payload Example:**
```json
{
  "device_id": "SCALE_BOS_01_A",
  "timestamp": "2024-11-05T14:30:00Z",
  "item_recognition_label": "French Fries",
  "confidence_score": 0.98,
  "weight_g": 450,
  "staff_id": "EMP_992"
}
```

**Architecture Shift:**
*   Excel manual entry is replaced by an **Azure Event Hub**.
*   The logic map updates: `item_recognition_label` maps to `DIM_ITEM.SKU`.
*   Data becomes real-time. Dashboard refreshes every 15 minutes.

---

### **Conclusion of Architecture**

This strategy prioritizes **structure over speed**. By forcing data through the `Fact_Waste` model—even when that data comes from a clipboard—we ensure that when we eventually upgrade to automated tools, the history is compatible. We are building a cathedral, not a shack; the foundation (Schema) must be poured before the stained glass (Dashboards) is installed.

---

# Project Phoenix Bible
## Section 4: Phase 1 – The Manual Audit & Baseline Establishment (Months 1-2)

**Document Owner:** Head of Field Operations & Data Governance
**Date:** October 15, 2024
**Scope:** In-Unit Implementation, Analog Data Capture, and Cultural Alignment
**Status:** Approved for Pilot
**Target Audience:** General Managers, Kitchen Managers, Executive Chefs

---

## 4.0 Introduction: The "Culture of Concealment"
Before we write a single line of SQL or build a dashboard, we must acknowledge the current reality of the SavoryBites kitchen: **Waste is hidden.**

In the restaurant industry, "waste" is often synonymous with "mistake." If a line cook burns a burger, they bury it in the trash to avoid judgment. If a prep cook orders too much basil, they throw it out before the Chef sees it rotting. This "Culture of Concealment" is the primary barrier to data integrity.

**Phase 1 is not just about counting; it is about granting Amnesty.** We are removing the stigma of waste to see the monster in plain sight.

---

## 4.1 Phase Objective: The "Zero-Day" Baseline

We are attempting to measure the unmeasured. Our goals for the first 60 days are specific and binary (Pass/Fail).

1.  **Metric:** Establish the **"True Waste Rate"**. We suspect it is 4.5%, but the P&L says 4.0% (inventory manipulation accounts for the rest). We need the real number.
2.  **Behavior:** Establishing "The Walk." The physical habit of walking a failed item to the scale *before* walking it to the bin.
3.  **Data Integrity:** Generate 60 days of contiguous data from 15 locations with <5% "Unknown" category entries.
4.  **Identification:** Identify the "Top 10" loss items. (We cannot fix 1,000 SKUs at once; we need to find the heavy hitters).

---

## 4.2 The "Waste Log" Mechanism: Physical Architecture

We purposefully reject the use of tablets/iPads in the kitchen during Phase 1.
*   **The Problem:** Touchscreens don't work with latex gloves covered in fryer oil. Tablets break when dropped. Batteries die. WiFi disconnects in walk-in freezers.
*   **The Solution:** The "Red Clipboard." High-visibility, tactile, indestructible.

### 4.2.1 Station Setup
Every kitchen will be equipped with **3 Waste Stations**, strategically placed to minimize travel time for staff.

**Station A: The Prep Zone (Vegetables/Butchery)**
*   **Scale Type:** 20lb Analog Bench Scale (Tare function).
*   **Focus:** Trimmings, Spoilage, Over-Prep.
*   **Log Sheet Color:** White.

**Station B: The Cook Line (Hot Side)**
*   **Scale Type:** 5lb Digital Precision Scale.
*   **Focus:** Burnt food, Dropped items, Wrong orders.
*   **Log Sheet Color:** Yellow (High visibility for "Heat of Battle").

**Station C: The Dish Pit (Plate Waste)**
*   **Scale Type:** Industrial Floor Scale (for full trash bags).
*   **Focus:** Post-consumer waste (what customers leave).
*   **Log Sheet Color:** Blue.

### 4.2.2 The "Red Clipboard" Data Fields
The layout of the paper log is critical. If it is confusing, the data will be blank. The header contains: *Store ID*, *Date*, *Shift*.

**The 5 Columns:**

| Column | Data Type | Requirement | Field Example | Explanation for Staff |
| :--- | :--- | :--- | :--- | :--- |
| **1. Time** | HH:MM | Approx. | `11:45 AM` | Just look at the clock. Helps us know *when* we are messing up. |
| **2. Item Name** | Code | **Strict** | `FRIES`, `RIB-EYE` | No slang. Use the "Cheat Sheet" names attached to the clipboard. |
| **3. Wt / Qty** | Number | Numeric | `2.5` | How heavy is it? |
| **4. UOM** | Circle One | **Fixed** | `LB` / `KG` / `EA` | Circle "LB" for weight, "EA" if it's a whole chicken breast. |
| **5. Reason** | Code | **Strict** | `OP` / `CK` / `SP` | Use the 2-letter codes. Don't write an essay. |

---

## 4.3 Detailed Data Elements & Taxonomy

To ensure the "Messy Excel" data in Phase 2 is actually usable, we enforce strict taxonomy on the paper logs.

### 4.3.1 The Time Dimension
*   **Why it matters:** Waste signatures are time-dependent.
    *   *08:00 - 11:00 (Prep):* Spoilage logs here mean "Bad Inventory Management" (Rotten produce found during setup).
    *   *11:00 - 14:00 (Service):* Waste here implies "Execution Errors" (Burning food, wrong tables).
    *   *22:00 (Close):* Waste here implies "Over-Production" (Throwing away 20 gallons of unused Soup).

### 4.3.2 The Item Dimension (The "Top 50" List)
We cannot expect cooks to memorize 800 SKU codes.
*   **Action:** Each station has a laminated "Top 50 Waste Items" list attached to the wall.
*   **Rule:** If the item is *not* on the Top 50 list, write the clear English name (e.g., "Saffron").
*   **Grouping:** We group variant items for Phase 1 simplification.
    *   *Acceptable:* "Mashed Potato"
    *   *Too Detailed:* "Mashed Potato (No Garlic)" vs "Mashed Potato (Extra Butter)".
    *   *Reasoning:* The waste cost difference is negligible. We need speed.

### 4.3.3 The Reason Code Dictionary
We strip the nuance to 4 primary root causes.

| Code | Full Name | Definition | Scenario | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **SP** | **SPOILAGE** | Ingredient expired or degraded before cooking. | Moldy strawberries; Chicken smelling "off"; Stale bread. | KM / GM |
| **OP** | **OVER-PREP** | Perfectly good food cooked, but never sold. | End of night: 4 pans of rice in the trash. | KM |
| **CK** | **COOK ERROR** | Human error during production. | Burnt steak; Salty soup; Dropped on floor. | Line Cook |
| **PW** | **PLATE WASTE** | Food returned by guest. | "Cold soup"; "Didn't like taste"; "Portion too big." | Server/Menu |

::: info
**Scenario: The "Drop" vs. The "Bad Order"**
Cook A drops a raw steak on the floor. -> Code: **CK (Cook Error)**.
Server B rings in a "Medium" steak but the guest ordered "Rare." Cook A cooked it correctly (Medium), but it's waste. -> Code: **CK (Cook Error)** (Phase 1 simplification—we don't want cooks fighting servers over whose fault it is).
:::

---

## 4.4 Standard Operating Procedures (SOPs)

We introduce a new ritual to the kitchen: **"The Weigh-In."**

### 4.4.1 Workflow: The Line Cook (Hot Side)
**Scenario:** A basket of fries sits under the heat lamp for 15 minutes. They are limp. We cannot serve them.
1.  **Stop:** Do not dump the basket into the main bin.
2.  **Move:** Walk the basket to the "Station B" scale.
3.  **Tare:** Ensure scale reads `0.0`. Dump fries onto the scale tray.
4.  **Read:** Scale reads `1.2 lbs`.
5.  **Log:** Grab the pen on the string.
    *   *Time:* 1:45 PM
    *   *Item:* FRIES
    *   *Qty:* 1.2
    *   *UOM:* Circle `LB`
    *   *Reason:* Write `OP` (Over Prep/Batching).
6.  **Disposal:** Dump tray into the bin.
    *   *Total Time Cost:* 15 seconds.

### 4.4.2 Workflow: The Prep Cook (Vegetables)
**Scenario:** Trimming 50lbs of Asparagus. The woody ends are waste.
*   *Conflict:* We do not want to weigh every single stalk end.
*   **Protocol (Batching):**
    1.  Place a dedicated "Green Bucket" on the scale. Hit Tare.
    2.  Work for 1 hour, tossing ends into the Green Bucket.
    3.  When full, read the scale (`12.5 lbs`).
    4.  Log *one single entry* for the session.
    5.  *Log:* 9:30 AM | ASPARAGUS TRIM | 12.5 | LB | PREP (Natural Yield).

### 4.4.3 Workflow: The Manager (Digitization)
**Time:** 10:30 PM (Closing Duty)
1.  **Retrieve:** Manager collects clipboards from Stations A, B, and C.
2.  **Sanity Check:** Scan the sheets.
    *   *Error Check:* "Someone wrote '100 lbs' for a steak drop. They meant 1.00 lbs." Manager fixes it with red pen.
    *   *Translation:* Someone wrote "Bad Chix." Manager translates to "CKN-BREAST - SP".
3.  **Data Entry:** Open `Master_Waste_Log.xlsx` on the office PC.
    *   Manager transcribes the 20-30 lines of data.
    *   **Auto-Calculations:** The Excel sheet has a hidden VLOOKUP. As the Manager types "CKN-BREAST", Excel flashes "$4.50/lb" in the corner, confirming the SKU is matched.
4.  **Save:** File saved to SharePoint.

---

## 4.5 Change Management Strategy

This is the hardest part of Phase 1. "Culture eats Strategy for breakfast."

### 4.5.1 The "Amnesty" Declaration
**Risk:** Cooks will think, "If I log this burnt steak, I will get fired."
**Action:** The CEO and COO issue a video message to all stores.
> **The Script:** *"We know waste happens. For the next 60 days, nobody gets in trouble for the number on the scale. The only way you get in trouble is if the trash can is full, but the log sheet is empty. We are testing the system, not you."*

### 4.5.2 The Incentive: "The Precision Dinner"
We need to gamify the boring task of writing on a clipboard.

*   **The Metric:** Data Completeness, not Volume.
    *   Bad: Store A reports 0 lbs of waste (Obvious lie).
    *   Good: Store B reports 200 lbs of waste, with 98% of Reason Codes filled in correctly.
*   **The Reward:** The Kitchen Team with the most consistent logs (evaluated weekly by the Regional Manager) wins a $500 team dinner/bar tab at a competitor restaurant (or cash equivalent).
    *   *Why:* Cooks are competitive. They want to beat the other locations.

### 4.5.3 Handling "Rush Hour" Resistance
**Complaint:** "It's Friday at 7 PM. I don't have time to weigh a burger."
**The Compromise:** The "Sin Bin."
*   During extreme volume (Friday/Saturday 6-9 PM), staff can throw food into a specific clear "Sin Bin" *without* weighing immediately.
*   **The catch:** At 9:30 PM, the closing manager must weigh and categorize the entire Sin Bin contents (the "Autopsy").
*   *Psychology:* Cooks realize it's nicer to weigh as they go than to dig through cold, soggy food at the end of the shift.

---

## 4.6 Quality Assurance & Verification

How do we know the data isn't fake?

1.  **The Dumpster Diver Audit:**
    *   Once a week, the GM must randomly inspect the dumpster bags.
    *   *Check:* If there are 5 whole chickens in the bag, but the log says "0 Waste," we have a compliance failure.
    *   *Action:* GM holds a "Coach, Don't Punish" stand-up meeting the next day.

2.  **The Variance Triangulation:**
    *   Analyst at HQ compares `POS Sales` vs. `Purchases`.
    *   Theoretical usage says we should have used 500 burgers. We bought 550.
    *   Waste Log says we wasted 10.
    *   Gap: 40 missing burgers.
    *   *Conclusion:* Theft or failure to log. This prompts a site audit.

---

## 4.7 Risks and Mitigations (Phase 1 Specific)

| Risk Scenario | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **"Pencil Whipping"** (Making up numbers at end of shift) | High | Severe | Random Video Audit (checking CCTV timestamps against log timestamps). |
| **Equipment Failure** (Dead scale batteries) | Medium | Medium | "Scale Emergency Kit" (Spare AA batteries and analog backup scale) required in every office. |
| **Language Barrier** (Staff uncomfortable writing English) | Medium | Low | Use Icon-based charts for "Reasons" (e.g., picture of a trash can, picture of a clock). |
| **Data Silos** (Manager saves file to Desktop, not SharePoint) | High | Medium | Automated script scans SharePoint for missing store files at 9:00 AM daily and emails the GM automatically. |

---

## 4.8 Phase 1 Exit Criteria: The "Go/No-Go" for Phase 2

We conclude Phase 1 and unlock the funding for Phase 2 (SQL Server) only when:
1.  **Participation:** 15 out of 15 stores have submitted daily logs for 28 consecutive days.
2.  **Coverage:** The calculated "Waste %" rises from 0% (current perception) to at least 2% (approaching reality).
    *   *Note:* If the logs show 0.5% waste, the logs are fake. We expect to see "Ugly Data." **Ugly data is a success.**
3.  **Process:** All GMs can demonstrate the digitization process without assistance.

---

### **Conclusion of Phase 1**
Phase 1 is not efficient. It is messy, manual, and relies on paper. This is by design. By forcing the physical interaction with the waste, we interrupt the subconscious habit of throwing money away. We are building the muscle memory required for the sophisticated analysis to come.

>[!tip]
>**Field Note:** The most valuable data points in Phase 1 often come from the *notes* section of the Excel file. Managers often write comments like *"Fryer 2 is running too hot, burning stuff."* This qualitative feedback is just as valuable as the quantitative data.

---

# Project Phoenix Bible
## Section 5: Phase 2 – Centralized Analysis & Insight Generation (Months 3-4)

**Document Owner:** Head of Data Analytics
**Date:** October 15, 2024
**Scope:** Data Engineering, SQL Implementation, and Business Intelligence Extraction
**Status:** Approved for Implementation
**Dependencies:** Phase 1 Data Collection Completion

---

## 5.0 Introduction: The Shift from Observation to Intelligence
Phase 1 was about *participation*—getting 150 kitchen staff to physically acknowledge waste. Phase 2 is about *truth*. We are moving from 15 disparate clipboards to a single, unified source of truth.

At the start of Month 3, we possess a messy but valuable asset: approximately 45,000 rows of waste data (15 stores x 30 days x 100 entries/day). Stored in isolated Excel spreadsheets, this data is noise. Aggregated into a relational database, it becomes a signal.

This phase transforms the role of the Operations Team from "Loggers" to "Analysts." We are not just reporting *what* happened; we are determining *why* it happened and *how much* it cost us.

---

## 5.1 Objectives
The goal of Phase 2 is **Variance Decomposition**. We know we have a problem. Now we must dissect it.

1.  **Ingestion Automation:** Eliminate the need for a human analyst to manually copy-paste 15 Excel files together.
2.  **Valuation:** Append accurate financial values (Unit Costs) to volume data. Waste is physically measured in KGs but managed in Dollars.
3.  **Pattern Recognition:** Identify the "Vital Few" (Pareto Principle).
    *   Which *items* account for 80% of value loss?
    *   Which *reasons* account for 80% of preventable volume?
    *   Which *time slots* are the most dangerous?
4.  **Performance Normalization:** Rank restaurants fairly. Store A losing $500 is not necessarily worse than Store B losing $200, if Store A does 10x the sales volume.

---

## 5.2 The Data Engineering Architecture
We are bridging the gap between "file storage" (SharePoint) and "analytical processing" (SQL).

### 5.2.1 The Data Source Landscape
*   **Source:** SharePoint Folder `.../Incoming_Data/`.
*   **Format:** Standardized `.xlsx` template (enforced in Phase 1).
*   **Frequency:** Files are saved/overwritten daily by 11:00 PM local time.
*   **File Naming Convention:** `Waste_Log_[STORE_ID]_[YYYYMM].xlsx`.

### 5.2.2 The ETL Pipeline (Extract, Transform, Load)

We will use **Excel Power Query (Get Data)** as the "Poor Man's ETL" initially, graduating to a **Python Script** if file sizes exceed 100MB.

**Step 1: The Folder Scan (Extraction)**
We configure a Power Query connection to the root SharePoint folder.
*   *Filter:* Extension = `.xlsx` AND Name does not start with `~` (temp files).
*   *Action:* `Table.ExpandTableColumn` to merge all files into a singular dataset.

**Step 2: The Cleansing Layer (Transformation)**
Raw data from kitchen managers will be imperfect. The transformation logic handles the "Human Error."
*   **Date Standardization:** Convert text strings ("Nov 1st", "11/01") into ISO 8601 (`YYYY-MM-DD`).
*   **Unit Conversion (The UOM Standardizer):**
    *   *Problem:* Store A logs "5 Lbs" of Beef. Store B logs "2.2 Kg" of Beef.
    *   *Logic:* Create a conditional column.
        *   `IF UOM = 'LB' THEN Quantity * 0.453592 ELSE Quantity` -> `Quantity_KG`.
    *   *Output:* A unified volume metric (`Quantity_KG`) for every single row.
*   **Sanitization:** Trim whitespace (`TRIM()`), Proper Case text, remove NULL rows where managers dragged formulas too far down.

**Step 3: The Cost Injection (Enrichment)**
This is the most critical financial step. The waste logs contain *Volume*, not *Value*.
*   **Reference Data:** We export the `Master_Ingredient_Price_List.csv` from the Purchasing System.
    *   Columns: `Item_Code`, `Item_Name`, `Standard_Cost_Per_KG`, `Effective_Date`.
*   **The Join:** Perform a **Left Outer Join** between `Waste_Log` and `Price_List` on `Item_Name`.
    *   *Fallibility:* If a match is not found (e.g., Log says "Avocados", Price List says "Avocado, Haas"), the cost returns NULL.
    *   *Governance:* All NULL cost rows are flagged for review. A "Mapping Table" is maintained to alias "Avocados" to "Avocado, Haas".
*   **The Calculation:** `Estimated_Cost = Quantity_KG * Standard_Cost_Per_KG`.

### 5.2.3 The SQL Database Schema
Once transformed, the clean data is loaded into a local SQL Server Express or PostgreSQL instance. This provides query speed and allows for complex aggregations.

```sql
-- The Central Truth Table
CREATE TABLE waste_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY, -- Auto-increment unique ID
    transaction_uuid UNIQUEIDENTIFIER DEFAULT NEWID(), -- Traceability
    
    -- Dimensions
    restaurant_id VARCHAR(10) NOT NULL, -- e.g., 'STORE-05'
    log_date DATE NOT NULL,             -- e.g., '2024-11-01'
    time_bucket_hour INT,               -- Derived from HH:MM (e.g., 14 for 2PM)
    
    -- Item Details
    item_code VARCHAR(50),              -- SKU
    item_name VARCHAR(100),             -- Clean Name
    category VARCHAR(50) CHECK (category IN ('Raw', 'Prepared', 'Plate', 'Spoiled')),
    reason VARCHAR(50) CHECK (reason IN ('OP', 'EXP', 'COOK', 'DROP')),
    
    -- Metrics
    quantity_input DECIMAL(10,2),       -- What they typed
    uom_input VARCHAR(10),              -- What they selected
    quantity_kg DECIMAL(10,3),          -- Normalized Weight
    unit_cost_at_time DECIMAL(10,4),    -- Frozen cost at time of waste
    estimated_cost DECIMAL(10,2),       -- The Final $ Value
    
    -- Audit Metadata
    ingest_timestamp DATETIME DEFAULT GETDATE(),
    source_filename VARCHAR(255)
);

-- Indexing for Performance
CREATE INDEX idx_waste_store_date ON waste_log(restaurant_id, log_date);
CREATE INDEX idx_waste_category ON waste_log(category);
```

---

## 5.3 Analytic Queries & Insights: "The Forensic Accounting"

With the database populated, we move from data engineering to business intelligence. We ask three specific questions to unlock the savings.

### 5.3.1 Analysis A: The "Why" (Root Cause Attribution)
*Business Question:* "Are we losing money because the food is bad (Spoilage) or because our process is bad (Over-Prep)?"

**The SQL Query:**
```sql
SELECT 
    Reason, 
    -- Financial Impact
    SUM(estimated_cost) AS Total_Cost,
    CAST(SUM(estimated_cost) * 100.0 / (SELECT SUM(estimated_cost) FROM waste_log) AS DECIMAL(5,1)) AS Cost_Pct,
    -- Frequency
    COUNT(*) AS Incident_Count,
    -- Magnitude
    AVG(estimated_cost) AS Avg_Cost_Per_Incident
FROM waste_log
GROUP BY Reason
ORDER BY Total_Cost DESC;
```

**The Scenario & Insight:**
*   **Data Return:**
    *   Over-Preparation (OP): $42,000 (45%)
    *   Spoilage (EXP): $23,000 (25%)
    *   Cook Error (CK): $15,000 (16%)
    *   Plate Waste (PW): $13,000 (14%)
*   **Interpretation:** Almost half our waste is **Self-Inflicted**.
    *   *Insight:* "Over-Prep" is the low-hanging fruit. It means we cooked food hoping to sell it, but didn't. This suggests our "Par Levels" (prep quantity guides) are too optimistic.
    *   *Action:* We do not need new suppliers (Spoilage); we need new production schedules.

### 5.3.2 Analysis B: The "What" (Item-Level Pareto)
*Business Question:* "We have 800 items on the menu. Which 5 items are killing the P&L?"

**The SQL Query:**
```sql
SELECT TOP 10
    Item_Name,
    Category,
    SUM(quantity_kg) AS Total_Weight_Kg,
    SUM(estimated_cost) AS Total_Cost
FROM waste_log
WHERE Category = 'Prepared but Unsold' -- Focused only on Production Waste
GROUP BY Item_Name, Category
ORDER BY Total_Cost DESC;
```

**The Scenario & Insight:**
*   **Data Return:**
    1.  **French Fries:** $8,500 loss (High volume, low cost, huge aggregate).
    2.  **Coleslaw:** $4,200 loss.
    3.  **Mashed Potatoes:** $3,800 loss.
*   **Deep Dive Investigation (The Time Dimension):**
    *   We run a secondary query on French Fries specifically:
        ```sql
        SELECT time_bucket_hour, SUM(quantity_kg) 
        FROM waste_log 
        WHERE Item_Name = 'French Fries' 
        GROUP BY time_bucket_hour 
        ORDER BY time_bucket_hour;
        ```
    *   *Result:* Massive spike at 15:00 (3 PM) and 22:00 (10 PM).
*   **The Narrative:**
    *   *The 3 PM Spike:* The "Lunch Hangover." Cooks fill the fry baskets at 1:30 PM for the rush. The rush stops at 2:00 PM. The fries sit. At 3:00 PM shift change, the incoming manager tosses the cold fries.
    *   *Action:* Implementation of "Cook-to-Order" blackout periods (Phase 3).

### 5.3.3 Analysis C: The "Who" (Normalized Performance)
*Business Question:* "Which manager needs a bonus, and which needs training?"

*Warning:* We cannot compare raw totals. Store #1 (Times Square) will always have more waste than Store #15 (Suburbs) simply due to volume. We must normalize by Sales.

**The SQL Query:**
```sql
WITH Store_Sales AS (
    -- Aggregated from POS System Import
    SELECT store_id, SUM(gross_sales) as Total_Sales 
    FROM pos_data 
    GROUP BY store_id
),
Store_Waste AS (
    SELECT restaurant_id, SUM(estimated_cost) as Total_Waste
    FROM waste_log
    GROUP BY restaurant_id
)
SELECT 
    w.restaurant_id,
    w.Total_Waste,
    s.Total_Sales,
    -- The Magic Metric: Waste %
    (w.Total_Waste / s.Total_Sales) * 100 AS Waste_Percentage_Of_Sales,
    RANK() OVER (ORDER BY (w.Total_Waste / s.Total_Sales) ASC) as Performance_Rank
FROM Store_Waste w
JOIN Store_Sales s ON w.restaurant_id = s.store_id
ORDER BY Waste_Percentage_Of_Sales DESC;
```

**The Scenario & Insight:**
*   **Data Return:**
    *   *Store #09:* 4.8% Waste (Worst).
    *   *Store #04:* 1.2% Waste (Best).
    *   *Average:* 3.1%.
*   **The Deep Dive on Store #09:**
    *   We filter the waste log for just Store #09.
    *   We find that 60% of their waste is "Spoilage" of "Seafood".
    *   *Root Cause:* Store #09 is in a business district that is dead on weekends, yet they are ordering fish delivery on Fridays.
    *   *Action:* Change Store #09's delivery schedule to Monday/Wednesday only.

---

## 5.4 Cross-Analysis: Validating the Data (Quality Assurance)

Before we present these findings to the COO, we must audit the data for "Cheating."

**The "Laziness" Query:**
```sql
-- Finding rounded numbers suggesting estimation
SELECT 
    restaurant_id,
    COUNT(*) as Suspicious_Entries
FROM waste_log
WHERE quantity_input IN (1.00, 2.00, 5.00, 10.00) -- Clean integers usually mean guessing
GROUP BY restaurant_id;
```
*   *Interpretation:* If Store #02 has 95% of their entries as exactly "1.00" or "5.00", they aren't using the scale. They are "pencil whipping" the log. The data from Store #02 is excluded from the regional average to avoid skewing the results.

---

## 5.5 Deliverable: The "State of Waste" Report
At the end of Month 4, the Central Analysis team produces a comprehensive deck.

**Visual 1: The Waterfall Chart**
*   Start: Ideal Food Cost (29%)
*   Add: Spoilage (+1.1%)
*   Add: Over-Prep (+2.0%)
*   Add: Theft/Unexplained (+0.9%)
*   End: Actual Food Cost (33%)

**Visual 2: The "Menu Matrix" (Boston Consulting Group Style)**
*   X-Axis: Waste Frequency (How often we toss it).
*   Y-Axis: Cost per Incident (How expensive is it).
*   *Quadrant I (High Cost/High Freq):* **Steaks & Seafood**. (Priority 1: Immediate procedural change).
*   *Quadrant II (Low Cost/High Freq):* **Fries, Rice, Mash**. (Priority 2: Batch size adjustment).

**The Final Recommendation:**
> "The data proves that 65% of our waste variance is internal operational behavior (Over-Prep/cooking habits), not supplier quality. We propose immediate adoption of 'Dynamic Par Levels' (Phase 3) focusing on the Top 5 Items: Fries, Slaw, Mash, Burgers, and Bread. This targets an annualized savings of $280,000."

::: tip
**Technical Note on Phase 2 Tools**
While SQL is powerful, Phase 2 relies heavily on **Power Query in Excel** as the user interface for the Analysts. We use Excel to *render* the data from the SQL backend because the Business Stakeholders are comfortable with PivotTables. We are building a "Hybrid" model: SQL for storage/logic, Excel for presentation. This bridges the gap before the Phase 4 Power BI rollout.
:::

# Project Phoenix Bible
## Section 6: Phase 3 – Operational Solutions & Pilot Redistribution (Months 5-8)

**Document Owner:** VP of Operations / Chief Sustainability Officer
**Date:** October 15, 2024
**Scope:** Process Re-Engineering, Supply Chain Optimization, and Waste Diversion Pilots
**Status:** Execution Phase
**Prerequisites:** Phase 2 Root Cause Analysis Complete

---

## 6.0 Introduction: The Bridge from "What" to "How"

In Phase 2, the SQL queries acted as a diagnostic MRI, revealing the internal fractures of our operation (Over-Prep and Spoilage). Phase 3 is the Surgery.

We are now pivoting the organization from **Observation** mode to **Intervention** mode. This phase is dangerous because it requires interfering with the "sacred geometry" of the line cook’s workflow. We are moving from an "Intuition-Based" kitchen (where chefs guess how much to prep) to a "Precision-Based" kitchen (where data dictates the prep).

Simultaneously, we launch the "Redistribution" stream. We acknowledge that zero waste is impossible—there will always be eggshells. The goal shifts from "Prevention" to "Value Retention" via the Circular Economy.

---

## 6.1 Intervention 1: Dynamic Prep Planning (The "Fry/Slaw" Correction)

**The Insight:** Phase 2 data revealed that 40% of our cost variance comes from "Prepared but Unsold" items, specifically rapid-turnover items like French Fries, Coleslaw, and Mashed Potatoes.
**The Root Cause:** Static Par Levels. The kitchen acts as if 2:00 PM Tuesday is the same volume as 7:00 PM Friday.
**The Objective:** Implementing "Temporal Production Gates."

### 6.1.1 The "Time-Gate" SOP Change
We are altering the Standard Operating Procedure (SOP) to introduce a hard operational break at **1:15 PM** and **8:00 PM**.

**SOP Reference: KIT-OPS-044 (Fry Station Management)**

| Time Window | Operational Mode | Trigger Behavior | Batch Size Constraint |
| :--- | :--- | :--- | :--- |
| **11:00 AM – 1:15 PM** | **Batch Mode** | Anticipatory Cooking. | **Full Basket (5 lbs).** Cook continuously to keep holding bin full. |
| **1:15 PM – 4:30 PM** | **Cook-to-Order** | Reactive Cooking. | **Single Order.** Drop fries *only* when ticket prints. |
| **4:30 PM – 8:00 PM** | **Batch Mode** | Anticipatory Cooking. | **Full Basket (5 lbs).** |
| **8:00 PM – Close** | **Cook-to-Order** | Reactive Cooking. | **Half Basket / Single Order.** Strict ban on full drops. |

### 6.1.2 The "Visual Anchor": The Par Level Matrix
Kitchens do not read memos. They look at walls. We will install **Laminated Par Charts** at the Fry Station and Cold Station (Garde Manger).

**The Physical Tool:**
*   **Dimensions:** 11x17 inch, heavy lamination, magnetic backing.
*   **Content:** A matrix correlating Day/Time to Bin Size.
*   **Color Coding:**
    *   **RED ZONE (High Vol):** Use 1/3 Pans (Deep).
    *   **YELLOW ZONE (Med Vol):** Use 1/6 Pans.
    *   **GREEN ZONE (Low Vol):** Use 1/9 Pans or Cook-to-Order.

> **Field Execution Detail:**
> On Weekdays at 1:15 PM, the "Expo" (Expediter/Head Chef) calls out: *"Switch to CT-O (Cook to Order) on Fries."*
> The Fry Cook physically removes the large "holding scoop" and replaces it with tongs. This physical tool change enforces the behavioral change.

### 6.1.3 Impact Projection
*   **Historical Behavior:** Dropping a 5lb basket at 1:45 PM. Result: 3lbs wasted at 2:15 PM (Quality Timer expiry).
*   **New Behavior:** Dropping 4 separate orders between 1:45 PM and 2:15 PM.
*   **Net Savings:** 3lbs of potatoes + 4 oz of Fryer Oil + Energy + Disposal Cost.
*   **Scaling:** 3lbs/day * 15 stores * 365 days = **16,425 lbs of potatoes saved annually**.

---

## 6.2 Intervention 2: Supply Chain Rationalization (The "Bread" Fix)

**The Insight:** Bread Spoilage accounts for 25% of waste cost.
**The Root Cause:** **The "Minimum Order Quantity" (MOQ) Trap**. We are contractually forced to buy 144 Brioche Buns (12 packs of 12) even if we forecast selling only 60.

### 6.2.1 Strategy A: The "Broken Case" Negotiation
**Action Owner:** Procurement Director.
**Target:** Regional Distributor (e.g., Sysco, US Foods) and the Local Bakery.

**The Pitch:**
*   Currently, we buy a "Master Case" (144 count).
*   We propose a new SKU: "Split Case" (72 count).
*   *Distributor Resistance:* "It costs us labor to break the case."
*   *SavoryBites Leverage:* "We are currently throwing away 20% of your product. If we cannot resolve this, we will switch to a 'Frozen Bun' product which allows unit-level pulling. This will result in a 100% loss of business for the fresh bakery."
*   **Target Outcome:** Supplier agrees to list a 72-count SKU with a 5% price premium (which is cheaper than 20% waste).

### 6.2.2 Strategy B: The "Freeze-on-Arrival" Protocol (SOP)
If negotiation fails, we implement rigorous inventory management.

**The "Day Dot" Workflow:**
1.  **Delivery Arrival (Mon 8:00 AM):** 144 Buns arrive.
2.  **Segregation:** Manager checks the sales forecast.
    *   Projected Usage (Mon-Wed): 70 Buns.
    *   Buffer: 10 Buns.
    *   Total Shelf Needed: 80.
    *   Surplus: 64.
3.  **Action:** The 64 surplus buns are **immediately** placed in freezer bags.
4.  **Tagging:** A specific "frozen date" label is applied.
5.  **Re-Activation:** On Thursday, if sales spike, buns are pulled 4 hours prior to service to slack-out (thaw).

**The Rule:** *"If it hits the Bread Rack, the clock starts. If it hits the Freezer, the clock stops."* We stop treating the Bread Rack as storage and start treating it as "Ready Inventory."

---

## 6.3 Pilot Program: The "Farm Bucket" (Organics Redistribution)

**The Objective:** Close the loop on *inevitable* organic waste (e.g., Pineapple skins, onion peels, eggshells).
**The Challenge:** Food waste is heavy. Dumpsters are expensive.

### 6.3.1 Regulatory Framework & Compliance (The "Swill" Law)
**Critical Critical Constraint:** The "Swill Feeding" laws (e.g., USA Swine Health Protection Act).
*   Feeding meat or food contaminated with meat/grease to pigs is illegal in many jurisdictions to prevent Foot and Mouth Disease (FMD).
*   **Strict Scope:** The pilot will cover **Pre-Consumer Vegetative Waste Only**.
    *   *Allowed:* Fruit rinds, vegetable peels, eggshells, coffee grounds, stale bread.
    *   *Banned:* Meat scraps, dairy, oily table scraps (Plate Waste).

### 6.3.2 Partner Identification Strategy
We need local agility, not national contracts.
**Pilot Locations:** 3 Stores situated in semi-rural/suburban zones (closer to agriculture).

**Vetting Checklist for Farmers:**
1.  **Proximity:** < 20 miles (Otherwise fuel costs negate the benefit).
2.  **Scale:** Must handle ~150-200lbs per week.
3.  **Reliability:** Commitment to twice-weekly pickup.
4.  **Liability Waiver:** Signed agreement that SavoryBites is donating "as-is" and is not liable for livestock health (standard "Good Samaritan" law protection).

### 6.3.3 Operational Workflow: "The Green Bucket"

**Equipment:**
*   Five 5-Gallon Home Depot-style buckets per store.
*   Color Code: **Bright Green** (Spray painted or labeled).
*   Location: Prep Table only (Vegetable Station).

**Step-by-Step SOP:**
1.  **Prep:** Cook peels carrots. Peels go into Green Bucket (NOT the trash can).
2.  **Audit:** Before sealing, Manager visual check. "Any plastic? Any bacon?" -> *If yes, dump in trash. We cannot risk the relationship.*
3.  **Staging:** Sealed buckets are moved to the Walk-in Cooler (Back shelf). *They must be refrigerated to prevent pest infestation/odors.*
4.  **Hand-Off:** Tuesday/Friday morning. Farmer arrives at back door.
    *   Farmer drops off 5 Clean Empty Buckets.
    *   Farmer takes 5 Full Buckets.
    *   *Zero Dumpster Interaction.*

### 6.3.4 The Economic & Environmental Model

**The Economics of Trash (Tipping Fees):**
*   **Current State:** 3 Yards Dumpster, picked up 3x/week.
    *   Cost: $400/month.
    *   Overweight Fees: $50/month (Wet organics are heavy).
*   **Future State:**
    *   Divert 250 lbs/week to Farm.
    *   Reduce Dumpster weight. Eliminate Overage Fees ($50 saved).
    *   Reduce Pickup Frequency to 2x/week (negotiated with Hauler).
    *   New Cost: $300/month.
    *   **Net Savings:** $150/month per store.
    *   *Farmer Cost:* Free (We give feed, he gives labor/transport).

**The Environmental "Marketing" Asset:**
*   Diverting 250lbs/week = 13,000 lbs/year per store.
*   **The Story:** We place a chalkboard in the waiting area:
    > *"This week, SavoryBites Store #4 diverted 250lbs of food scraps to feed local livestock at [Farm Name]. Nothing wasted, everything connected."*
*   This builds immense community goodwill and differentiates us from generic chains.

---

## 6.4 Intervention 4: The "Imperfect" Upcycling (Citrus Rescue)

**The Insight:** Bar operations produce distinct, high-quality waste. We peel hundreds of lemons/oranges for "twists," discarding the juicy fruit; or we juice them and discard the rinds.

**The Micro-Pilot:**
*   **Partner:** Local Craft Distillery or Bakery.
*   **Scenario:**
    1.  Bartenders peel lemons. The "waste" is the peeled fruit itself.
    2.  Kitchen collects peeled lemons.
    3.  **Use Case A (Internal):** Culinary team creates "House-Made Lemonade" or "Citrus Vinaigrette." Cost of Goods: $0.
    4.  **Use Case B (External):** Local Distillery collects the lemon peels (if we juice the fruit) to use as botanicals for Gin.
*   **Result:** Turning a disposal cost into a product (Lemonade has 95% profit margin).

---

## 6.5 Measuring Phase 3 Success (KPIs)

How do we know the "Process" changes worked before we scale?

1.  **The "Dumpster Dive" Metric:** The physical weight of the trash dumpster should decrease by 20%.
2.  **The "Hold Time" Metric:** Random audits of the Fry Station.
    *   *Success:* Auditor finds only 1 basket of fries at 3:00 PM.
    *   *Fail:* Auditor finds 3 baskets of cold fries.
3.  **The "Variance Report":** Phase 3 ends when the **Usage Variance** (Actual vs Ideal) drops from 4.5% to <3.0% for two consecutive months.

---

## 6.6 Risk Management Strategy (Phase 3)

| Risk Area | Specific Threat | Mitigation Protocol |
| :--- | :--- | :--- |
| **Operational Friction** | "The Par Charts slow me down." | Chefs are stubborn. We identify one "Super-User" Chef to vouch for the system: *"I leave earlier at night because I have less to clean up."* Appeal to their laziness/efficiency. |
| **Health/Safety** | Farmer Bucket contamination (Salmonella/Pests). | Buckets MUST be refrigerated. We implement a "HACCP Log" for the waste buckets just like food (Temp check). |
| **Partner Reliance** | Farmer stops showing up. Buckets pile up. | **Backup Plan:** If Farmer misses 2 pickups, the program pauses, and waste reverts to landfill. Do not let rotting food accumulate. |
| **Supply Chain** | Distributor refuses to break cases. | We form a "Buying Group" coalition with other local restaurants to pressure the distributor, or we implement the Freezer Protocol. |

---

### **Conclusion of Phase 3**
Phase 3 is the hardest operational phase. It asks staff to change habits formed over years. Success depends on "Visible Leadership"—the Regional Managers must physically inspect the Par Charts and the Green Buckets.

If successful, we achieve the "Triple Bottom Line":
1.  **Profit:** Lower Food Cost (Less prep) and Lower Waste Removal Cost.
2.  **People:** Less busy work for cooks (Don't prep what you don't sell).
3.  **Planet:** Circular economy diversion.

We are now ready to automate the reporting and scale the victories in **Phase 4**.

---

## **7. Phase 4: Reporting, Scaling, and Circular Economy (Months 9-12)**

### **7.1 Objective**
Institutionalize the gains. Replace manual SQL queries with automated BI Dashboards. Scale the circular economy concept to high-revenue opportunities.

### **7.2 Power BI Architecture**

#### **7.2.1 Data Modeling (Star Schema)**
We transform the data into a star schema for performance in Power BI.

*   **Fact Table:** `Fact_Waste_Transactions`
*   **Dimension Tables:**
    *   `Dim_Restaurant` (ID, Region, Manager Name, Opening Date)
    *   `Dim_Item` (Item_ID, Name, Category, Unit_Cost, Supplier)
    *   `Dim_Date` (Date, Day_of_Week, Is_Holiday, Fiscal_Month)
    *   `Dim_Reason` (Reason_Code, Reason_Description, Corrective_Action_Text)

#### **7.2.2 The "Circular Economy Dashboard"**
**Tab 1: Executive Overview**
*   **KPIs:** Total Waste Cost (YTD), Variance vs Goal (25%), Waste % of Sales.
*   **Visual:** Line chart overlaying Waste Cost vs. Sales (Check for correlation).

**Tab 2: Operations Leaderboard (Gamification)**
*   **Visual:** Horizontal Bar Chart ranking restaurants by "Waste Reduction %".
*   **Psychology:** No manager wants to be at the bottom. This drives compliance without top-down shouting.

**Tab 3: Sustainability Impact**
*   **Metrics:** Lbs Diverted from Landfill.
*   **Equivalencies:** "We saved enough food to feed X families" or "Carbon footprint reduced by Y tons." (Used for marketing/PR).

### **7.3 Expanding Partnerships**

#### **7.3.1 Non-Profit Partnership (Tax Strategy)**
*   **Scenario:** Perfectly safe cooked food (e.g., muffins baked that morning, soups) cannot be sold tomorrow.
*   **Action:** Partner with "City Harvest" or local shelter.
*   **Process:** Food is blast-chilled, packaged, and labeled.
*   **Financial Impact:** In many jurisdictions, businesses receive a tax deduction for the Fair Market Value (or cost) of donated food. This turns a total loss into a tax shield.
*   **Tracking:** The Power BI dashboard adds a `Donation_Value` column to track potential tax credits.

#### **7.3.2 Revenue Stream: The "Citrus Peel" Upcycling**
*   **Insight:** Bar waste (Lemons, Limes, Oranges peeled for garnishes) is high volume and high quality.
*   **Partner:** Local craft distillery or marmalade startup.
*   **Deal:** SavoryBites provides "pre-peeled, washed citrus skins" (a raw material) for a nominal fee or trade (branded spirits).
*   **Outcome:** We turn a waste disposal cost into a small revenue line or marketing collaboration ("SavoryBites Gin").

---

## **8. Risk Management**

| Risk Area | Specific Risk | Mitigation Strategy |
| :--- | :--- | :--- |
| **Data Quality** | "Pencil Whipping" (Staff fabricating logs). | Spot checks (Audit bins vs Logs). Digital scales with Bluetooth connectivity (Year 2 roadmap). |
| **Operational** | Cross-contamination in Farm Buckets. | rigorous training on "Green Bucket" protocols. One strike rule for plastics in compost. |
| **Health/Safety** | Storing waste leading to pests. | Farm pickups must be twice weekly. Sealed, air-tight buckets stored in refrigerated areas if necessary. |
| **Financial** | Savings do not justify the labor cost of logging. | Switch to "Key Item Audit" only (Track top 20 items only) after baseline is established to reduce labor time. |

---

## **9. Year 2 Roadmap & Beyond**

### **9.1 IoT Integration**
**Smart Bins:** Implement technology like *Leanpath* or *Winnow*.
*   *How it works:* A camera above the bin uses Computer Vision to identify the food. A scale below weighs it. The staff member just confirms the item on a touchscreen.
*   *Benefit:* Eliminates manual data entry, increases accuracy to 99%.

### **9.2 Dynamic Production Planning**
Integrate the Waste Database with the Prep Database.
*   *Logic:* If Waste Logs show "Monday Potato Soup" is thrown away 80% of the time, the Digital Prep List automatically reduces the par level for Monday Soup by 50%.

### **9.3 Consumer-Facing Story**
Add a "Sustainability Score" to the menu.
*   *Marketing:* "At SavoryBites, 0% of our Fry Oil goes to landfill—it all becomes Biodiesel." Use the data to drive brand preference among eco-conscious diners.

---

## **10. Conclusion**

Project Phoenix is not merely a cost-cutting exercise; it is a fundamental shift in operational philosophy. By moving from intuition to instrumentation, SavoryBites transforms food waste from a "garbage problem" into a "data asset."

Within 12 months, we project:
1.  **Financials:** Saving $100,000+ annually across the chain (based on industry standards of 25% waste reduction).
2.  **Operational:** Leaner, more disciplined kitchen workflows.
3.  **Reputation:** Positioning SavoryBites as a leader in sustainable dining.

The journey begins not with a server, but with a scale and a spreadsheet.

>[!information]
>**Final Note on Document Usage**
>This document serves as the Source of Truth. Any deviations from the data definitions or SOPs listed in Phases 1-3 must be approved by the Project Lead to ensure data integrity for the Phase 4 rollout.
