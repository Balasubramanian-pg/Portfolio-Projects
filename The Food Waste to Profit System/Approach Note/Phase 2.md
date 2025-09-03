# **Project Phoenix: Phase 2 - Centralized Analysis & Insight Generation**

**Objective:** To transform the raw, disparate waste log data into a centralized source of truth and generate actionable, evidence-based insights to guide strategic decision-making for waste reduction.
**Timeline:** Months 3-4
**Primary Tools:** SQL, Microsoft Excel (Power Query), Power BI (Initial Setup)
**Key Stakeholders:** Operations Manager, Data Analyst, Head Chef, Finance Department

### **1. Overview & Strategic Purpose**

Phase 1 provided the raw material—the "what." Phase 2 is about discovering the "why" and the "so what." This phase moves from data collection to data intelligence. By centralizing and rigorously analyzing the data from all 15 locations, we will identify patterns, pinpoint root causes, and quantify the financial impact of specific waste issues. The output of this phase is a **prioritized list of actionable opportunities** for waste reduction, backed by solid data.

> **Key Callout: From Reactive to Proactive**
> Without this analysis, our efforts would be reactive and based on hunches. This phase allows us to proactively target the most significant sources of waste, ensuring our interventions in Phase 3 will have the highest possible return on investment (ROI).

### **2. Phase Inputs: The "Raw Material"**

The primary input for this phase is the deliverable from Phase 1:
*   **15+ Excel Files:** The completed `SavoryBites_WasteLog_[Location].xlsx` files from each restaurant.
*   **Baseline KPIs:** Initial high-level metrics on total waste cost.

### **3. Core Activities & Technical Process**

This phase is executed through a structured, three-step data pipeline.

#### **Step 1: Data Consolidation & Cleaning (Tool: Excel Power Query)**

*   **Action:** Create a master Excel workbook that uses **Power Query** to connect to all 15 individual waste log files. Power Query will:
    1.  **Extract:** Pull data from each source file.
    2.  **Transform:** Clean and standardize the data (e.g., correct spelling errors in `Waste Reason`, standardize units to kilograms, apply consistent cost calculations).
    3.  **Load:** Merge the cleaned data into a single, master table ready for analysis.
*   **Output:** A clean, unified dataset (`master_waste_data`) in a single table or CSV file.

> **Key Callout: The Power of Automation**
> Using Power Query instead of manual copy-pasting is critical. Once set up, this process can be re-run instantly in future months, saving dozens of hours and eliminating manual error. This builds a scalable process for ongoing analysis.

#### **Step 2: Exploratory Data Analysis (EDA) (Tool: SQL)**

*   **Action:** The cleaned data is imported into a SQL database (e.g., PostgreSQL, MySQL, or even a robust SQLite file) for deep analysis. Key queries will be run to uncover insights:

    ```sql
    -- 1. Find the Top 5 Costliest Waste Items
    SELECT 
        waste_item_name,
        SUM(estimated_cost) as total_cost
    FROM master_waste_data
    GROUP BY waste_item_name
    ORDER BY total_cost DESC
    LIMIT 5;

    -- 2. Identify the Most Common Reasons for Waste
    SELECT 
        waste_reason,
        SUM(quantity) as total_quantity_kg,
        SUM(estimated_cost) as total_cost
    FROM master_waste_data
    GROUP BY waste_reason
    ORDER BY total_cost DESC;

    -- 3. Compare Performance Across Locations
    SELECT 
        restaurant_name,
        SUM(estimated_cost) as total_waste_cost,
        SUM(estimated_cost) / (SELECT SUM(estimated_cost) FROM master_waste_data) * 100 as percent_of_total
    FROM master_waste_data
    GROUP BY restaurant_name
    ORDER BY total_waste_cost DESC;

    -- 4. Analyze Waste by Day of Week (Using a JOIN to a dim_date table)
    SELECT 
        d.day_of_week,
        SUM(f.estimated_cost) as total_cost
    FROM fact_waste_log f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.day_of__week, d.day_of_week_number
    ORDER BY d.day_of_week_number;
    ```
*   **Output:** A series of summarized tables and lists that answer critical business questions.

#### **Step 3: Insight Synthesis & Hypothesis Formation**

*   **Action:** Translate SQL query results into business insights and form testable hypotheses.
    *   **Finding:** "40% of waste cost is from over-preparation of fries and coleslaw on weekdays."
    *   **Hypothesis:** "We can reduce waste by 15% by adjusting prep par levels for weekdays vs. weekends."
    *   **Finding:** "Location SB-12 has 2x the waste cost of SB-07 for the same menu items."
    *   **Hypothesis:** "SB-07's manager has a more effective inventory and prep routine that can be standardized across other locations."

> **Key Callout: The 80/20 Rule of Waste**
> The analysis will almost certainly reveal that a small number of items (~20%) contribute to the majority of waste costs (~80%). Our strategy will be to focus relentlessly on these high-impact items first.

### **4. Anticipated Challenges & Mitigation Strategies**

| Challenge | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **"Dirty Data"** from Phase 1 (spelling errors, inconsistent units). | Garbage In, Garbage Out. Analysis leads to incorrect conclusions. | **Power Query Cleaning:** Develop a robust "cleaning" script in Power Query that automatically corrects common errors and flags outliers for review. |
| **Lack of SQL Expertise.** | Inability to perform deep analysis, slowing down the project. | **Leverage Power BI:** Many EDA tasks can be done through Power BI's visual query builder. For complex queries, a short-term consultant or upskilling an analyst can be cost-effective. |
| **Data Silos.** | Resistance from managers who don't trust the aggregated data or feel their context is missing. | **Contextualize the Data:** Present findings back to managers *before* finalizing conclusions. Their qualitative insight (e.g., "We had a catering cancellation that week") is invaluable for accurate analysis. |

### **5. Success Metrics & Deliverables**

By the end of Phase 2, we will have produced:

1.  **A Centralized Data Repository:** A clean, analysis-ready SQL database or master file.
2.  **The "Waste Intelligence" Report:** A PowerPoint or Power BI summary deck containing:
    *   **Prioritized List of Opportunities:** A ranked list of the 3-5 most significant waste reduction opportunities (e.g., "1. Adjust Fry Prep Levels," "2. Address Bread Spoilage").
    *   **Quantified Impact:** Each opportunity includes the projected monthly savings (e.g., "Potential save: `$1,200/month`").
    *   **Outlier Analysis:** Clear identification of top-performing and bottom-performing locations.
    *   **Data-Driven Hypotheses:** Clear, testable statements to be proven in Phase 3.
3. **Initial Power BI Data Model:** The foundation of the dashboard is built with the cleaned data, ready for visualization in Phase 4.

### **6. Next Steps: Handoff to Phase 3**

The "Waste Intelligence" Report is the direct blueprint for **Phase 3: Implement Low-Tech Solutions & Pilot Redistribution**. It tells us **exactly what to fix, where to fix it, and what the potential payoff will be.** This ensures our actions in the next phase are precise, targeted, and have the highest probability of success.

**Document Version:** 1.0<br>
**Author:** [Your Name/Department]<br>
**Status:** Final Draft for Execution
