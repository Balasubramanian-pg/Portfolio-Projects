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

## **3. Architecture and Data Strategy Overview**

Although this project starts with Excel, we must architect for the future to prevent "spreadsheet hell." We will utilize a **Crawl-Walk-Run** technical strategy.

### **3.1 Technical Stack Lifecycle**

| Phase | Collection Layer | Storage Layer | Processing Layer | Consumption Layer |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Paper Logs -> Excel Entry | Local Excel Files (SharePoint) | Manual Aggregation | Monthly Email Reports |
| **Phase 2** | Direct Excel Entry | SharePoint Folder | **SQL Database / Power Query** | Ad-hoc SQL Queries |
| **Phase 3** | Excel / Tablet Entry | Central Data Warehouse (Cloud SQL) | **Stored Procedures** | **Power BI (MVP)** |
| **Phase 4** | IoT Scales (Roadmap) | Cloud Data Warehouse | Auto-ETL Pipelines | **Power BI (Enterprise)** |

### **3.2 The Conceptual Data Model**
Even in the Excel phase, data must follow a strict schema to allow for SQL ingestion later.

**Core Entity: `Waste_Fact`**
*   `Transaction_ID`: Unique Identifier.
*   `Date_Time`: Timestamp of disposal.
*   `Location_ID`: Foreign key to Restaurant master.
*   `Item_ID`: Foreign key to Ingredient master.
*   `Category_Code`: (Prep, Spoilage, Plate, Error).
*   `Reason_Code`: (Over-prep, Burned, Dropped, Refire).
*   `Quantity`: Float value.
*   `UOM` (Unit of Measure): Kg, Lbs, Each.
*   `Estimated_Cost`: Derived field (Quantity * Unit_Cost).

---

## **4. Phase 1: The Manual Audit & Baseline Establishment (Months 1-2)**

### **4.1 Objective**
To establish a "Zero-Day" baseline. We cannot manage what we do not measure. We acknowledge this phase is high-friction for staff; the goal is data acquisition and cultural conditioning.

### **4.2 The "Waste Log" Mechanism**
We will deploy a physical clipboard system first, digitized daily. Kitchens are wet, hot, and fast; tablets break, but paper works.

#### **4.2.1 Data Elements Detailed**
1.  **Date & Time:** Essential for determining *when* waste happens.
    *   *Why?* Waste at 11:00 AM implies Spoilage/Prep error. Waste at 11:00 PM implies Over-production/Buffet waste.
2.  **Item:** Standardized naming is crucial.
    *   *Constraint:* Do not allow free text like "chicken stuff." Use specific codes: `CKN-BRST-RAW` vs `CKN-WNG-CKD`.
3.  **Category:**
    *   *Raw Ingredient:* Spoilage before cooking (Moldy tomatoes).
    *   *Prepared but Unsold:* Production variance (Too much soup made).
    *   *Plate Waste:* Customer refusal/returns (Quality issue).
    *   *Spoiled:* Expiration (Stock rotation failure).
4.  **Quantity & UOM:**
    *   *Standard:* Kitchens must use the prep scales. "A handful" is not data.
5.  **Reason:** The "Why."
    *   *Codes:* `OP` (Over Prep), `EXP` (Expired), `COOK` (Cook error/burnt), `DROP` (Dropped on floor).

### **4.3 Deployment Strategy: Change Management**
**Challenge:** "This is extra work."
**Response:** The "Scales & Incentives" Program.

> **Management Directive:**
> "Team, for the next 30 days, we are measuring waste not to punish, but to stop making you prep food we throw away. If you prep less waste, you close the kitchen faster."

**Incentive:** The kitchen with the most *consistent* logs (not lowest waste, but most accurate logging) gets a fully paid team dinner. This encourages honesty over hiding waste.

### **4.4 Standard Operating Procedure (SOP): Data Entry**
1.  **At the Station:** When a bin is emptied or food is tossed, the Cook places the item on the scale.
2.  **The Record:** Cook writes Time, Item, Wt, and Reason on the clipboard hanging next to the bin.
3.  **Digitization:** The Closing Manager takes the clipboard to the back office PC. They open the "SavoryBites_Master_Waste_Log.xlsx" template located on the shared SharePoint drive.
4.  **Sanitization:** Manager types the rows in. If a cook wrote "Onions," the Manager selects "Onion, Red, Diced" from the drop-down menu in Excel to ensure data quality.

> **Important:** This manual digitization step by the Manager acts as the first layer of Quality Assurance (QA).

---

## **5. Phase 2: Centralized Analysis & Insight Generation (Months 3-4)**

### **5.1 Objective**
Transition from isolated spreadsheets to aggregated intelligence. Identify the "Pareto Principles" of our waste (80% of costs coming from 20% of items).

### **5.2 Data Engineering Process**

#### **5.2.1 Ingestion (ETL)**
We have 15 distinct Excel files (one per restaurant) updated daily.
*   **Tool:** We will use **Power Query (Get Data > From Folder)** or a simple Python/SQL script to merge these files.
*   **Transformation:**
    1.  Union all tables.
    2.  Standardize date formats (ISO 8601).
    3.  Lookup Ingredient Costs: Join the waste log with the "Master Ingredient Price List" (CSV export from Purchasing System) on `Item_Name`.
    4.  Calculation: `Total_Waste_Cost = Quantity * Cost_Per_Unit`.

#### **5.2.2 The SQL Environment**
We set up a lightweight relational database (PostgreSQL or SQL Server Express).

**SQL Table Structure:**
```sql
CREATE TABLE waste_log (
    log_id SERIAL PRIMARY KEY,
    restaurant_id VARCHAR(10),
    log_date DATE,
    item_name VARCHAR(100),
    category VARCHAR(50),
    reason VARCHAR(50),
    quantity_kg DECIMAL(10,2),
    estimated_cost DECIMAL(10,2)
);
```

### **5.3 Analytic Queries & Insights**

#### **5.3.1 Top Waste Drivers by Reason**
*Business Question: Why are we losing money?*

```sql
SELECT 
    Reason, 
    SUM(Estimated_Cost) as Total_Cost 
FROM waste_log 
GROUP BY Reason 
ORDER BY Total_Cost DESC;
```
*   **Result:** The data reveals that "Over-Preparation" is the #1 reason ($40,000 annualized). This is a *behavioral* issue, not a supplier issue.

#### **5.3.2 Top Waste Drivers by Item (The "French Fry" Insight)**
*Business Question: What are we over-prepping?*

```sql
SELECT 
    Item_Name, 
    SUM(Quantity_Kg) as Total_Weight,
    SUM(Estimated_Cost) as Total_Cost
FROM waste_log 
WHERE Category = 'Prepared but Unsold'
GROUP BY Item_Name
ORDER BY Total_Cost DESC;
```
*   **Result:** French Fries and Coleslaw account for 40% of the cost. Staff are batch-cooking huge amounts at 1:30 PM, just before the lunch rush dies down. The food sits under heat lamps and is tossed at 4:00 PM.

#### **5.3.3 Restaurant Benchmarking**
*Business Question: Who is managing this well?*

```sql
SELECT 
    Restaurant_ID, 
    SUM(Estimated_Cost) / (SELECT SUM(Sales) FROM pos_sales WHERE pos_sales.store_id = waste_log.restaurant_id) as Waste_Percent_Of_Sales
FROM waste_log
GROUP BY Restaurant_ID;
```
*   **Result:** Restaurant #4 has 1.2% waste vs Sales. Restaurant #9 has 4.5%. Restaurant #4 becomes the model for Best Practices.

---

## **6. Phase 3: Operational Solutions & Pilot Redistribution (Months 5-8)**

### **6.1 Objective**
Translate SQL queries into kitchen reality. Implement physical changes to the "Process" component of People-Process-Technology.

### **6.2 Intervention 1: Dynamic Prep Levels**
Based on the "Fries/Slaw" insight, we change the Kitchen SOP.

*   **The Change:** Eliminate "Batch Prep" for fry drops after 1:15 PM.
*   **New SOP:** "Cook to Order" mode engages at 1:15 PM.
*   **Tool:** A laminated "Par Level Chart" is placed at the fry station.
    *   *Weekdays:* Par Level = 2kg (1 basket).
    *   *Weekends:* Par Level = 5kg (Full batch).
*   **Impact:** Reduces "Prepared but Unsold" category.

### **6.3 Intervention 2: Supplier Negotiations (The Bread Problem)**
Data showed 25% waste from Bread Spoilage. The loaves are too large for daily consumption.
*   **Action:** Procurement team contacts supplier.
*   **Solution:** Switch to "Split Loaves" (smaller SKUs) OR implement "Freeze-on-Arrival" protocol where 50% of the delivery goes immediately to the walk-in freezer.

### **6.4 Pilot Program: The "Farm Bucket" (Low-Tech Circular Economy)**
We identify a need to divert "inevitable waste" (egg shells, vegetable peels, plate scraps) from the landfill.

#### **6.4.1 Partner Identification**
*   **Target:** Local Piggeries or Composting facilities within 20 miles of 3 pilot locations.
*   **Agreement:** Farmer saves on feed costs; SavoryBites saves on waste removal fees (dumpsters are charged by weight or pull-frequency).

#### **6.4.2 Operational Flow**
1.  **Segregation:** Kitchen gets color-coded buckets. Green = Farm Waste. Black = Landfill.
2.  **Safety Rule (HACCP):** No meat bones (choking hazard/regulations) and no plastic. "Clean Organic Only."
3.  **Logistics:** Farmer picks up Tues/Fri. Exchange clean empty buckets for full ones.

#### **6.4.3 Financials**
*   **Cost Savings:** If we divert 200lbs per week, and tipping fees are $0.08/lb, we save ~$16/week/store. It's small, but scaling to 15 stores = $12,500/year, plus the "Sustainability" marketing value is worth much more.

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
