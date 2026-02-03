### **2. PROJECT OBJECTIVES**

- **Quantify:** Establish an empirical baseline for waste volume and financial impact.
- **Reduce:** Achieve a 25% reduction in food waste costs across all units within 12 months.
- **Monetize:** Validate at least one revenue stream or cost-saving partnership derived from waste products.
- **Standardize:** Create a replicable, data-driven operational model for kitchen efficiency and waste management.


### **3. FOUR-PHASE MATURITY MODEL**

#### **PHASE 1: MANUAL AUDIT & BASELINE ESTABLISHMENT (Months 1–2)**
**Objective:** Inject measurement into daily operations to generate initial data and cultural awareness.

- **Key Activities:**
  - Deploy analog scales and standardized paper logs at designated waste stations.
  - Implement a strict taxonomy for items, quantities, and waste reason codes (SP, OP, CK, PW).
  - Digitize logs into centralized Excel templates stored on SharePoint.
  - Launch change management campaigns, including an “Amnesty Declaration” to reduce stigma.

- **Success Criteria:**
  - 100% store participation for 28 consecutive days.
  - Calculated waste rate rises from perceived 0% to a measurable baseline (≥2%).
  - Identification of top 10 loss items by volume and cost.

#### **PHASE 2: CENTRALIZED ANALYSIS & INSIGHT GENERATION (Months 3–4)**
**Objective:** Transform raw data into actionable intelligence through aggregation and financial valuation.

- **Key Activities:**
  - Automate ingestion of Excel logs via Power Query into a SQL database.
  - Enrich waste data with real-time ingredient costs from procurement systems.
  - Execute forensic SQL queries to identify root causes (Pareto analysis of items, reasons, time slots).
  - Normalize performance metrics by sales volume to enable fair store-to-store comparison.

- **Deliverables:**
  - “State of Waste” report detailing cost attribution and variance decomposition.
  - Identification of high-impact intervention points (e.g., over-preparation of fries, bread spoilage).

#### **PHASE 3: OPERATIONAL SOLUTIONS & PILOT REDISTRIBUTION (Months 5–8)**
**Objective:** Implement process changes and launch circular economy pilots based on Phase 2 insights.

- **Key Interventions:**
  - **Dynamic Prep Planning:** Introduce time-gated par levels and visual production matrices to reduce over-preparation.
  - **Supply Chain Rationalization:** Renegotiate minimum order quantities or implement “freeze-on-arrival” protocols for perishables.
  - **Farm Bucket Pilot:** Divert pre-consumer vegetative waste to local livestock farms, reducing disposal fees and building community goodwill.
  - **Imperfect Upcycling:** Explore partnerships with distilleries or bakeries to repurpose bar and kitchen by-products.

- **Success Metrics:**
  - Reduction in dumpster weight and pickup frequency.
  - Decrease in food cost variance from 4.5% to <3.0% for two consecutive months.

#### **PHASE 4: REPORTING, SCALING & CIRCULAR ECONOMY (Months 9–12)**
**Objective:** Institutionalize gains through automated reporting and scale high-value partnerships.

- **Key Activities:**
  - Deploy Power BI dashboards with a star-schema data model for real-time visibility.
  - Implement gamified leaderboards to drive continuous improvement across stores.
  - Expand circular economy initiatives, including non-profit food donation (for tax benefits) and commercial upcycling (e.g., citrus peels for distilleries).
  - Develop consumer-facing sustainability narratives to enhance brand affinity.

- **Long-Term Vision:**
  - IoT integration (smart bins with computer vision) to automate data capture.
  - Dynamic production planning systems that adjust prep levels based on predictive waste analytics.


### **4. KEY STAKEHOLDERS & CHANGE MANAGEMENT**

| **Stakeholder**        | **Role**                | **Primary Concern**                          | **Engagement Strategy**                                                                 |
|-------------------------|-------------------------|----------------------------------------------|------------------------------------------------------------------------------------------|
| **Executive Leadership** | Sarah (COO)             | Margin pressure, ESG compliance              | Regular briefings on financial impact and valuation uplift.                               |
| **Regional Managers**   | Mike (Regional Director)| Lack of real-time visibility across stores   | Provide dashboards for coaching (not policing) and performance normalization.             |
| **General Managers**    | Elena (Store GM)        | Administrative burden, fear of blame         | Streamline inventory processes and frame tools as efficiency enhancers.                   |
| **Kitchen Staff**       | Line Cooks / Prep       | Perceived slowdown, fear of punishment       | Simplify logging workflows, offer amnesty, and incentivize via gamification and recognition. |


### **5. ARCHITECTURE & DATA STRATEGY OVERVIEW**

The technical architecture follows a **crawl-walk-run-fly** maturity model, ensuring each phase builds a scalable foundation for the next.

- **Phase 1 (Crawl):** Iron-clad Excel templates with data validation, stored on SharePoint.
- **Phase 2 (Walk):** Power Query ETL into SQL Server, enabling centralized analysis.
- **Phase 3 (Run):** Migration to Azure SQL Database with star-schema modeling for performance.
- **Phase 4 (Fly):** Power BI dashboards, IoT integration, and predictive analytics.

**Core Data Model:** Centered around `FACT_WASTE_TRANSACTION`, linked to dimensions for Date, Time, Store, Item, and Reason. This ensures historical comparability and robust financial attribution.


### **6. RISK MANAGEMENT**

| **Risk Area**       | **Specific Risk**                          | **Mitigation Strategy**                                                                 |
|----------------------|--------------------------------------------|------------------------------------------------------------------------------------------|
| **Data Quality**     | Fabricated or inaccurate manual logs       | Random audits, CCTV cross-checks, and outlier detection algorithms.                      |
| **Operational**      | Resistance to process changes              | Engage “super-user” champions, demonstrate time-saving benefits, and provide clear SOPs. |
| **Partner Reliance** | Farm pickup failures or supply chain pushback | Establish backup disposal plans and coalition-based negotiation tactics.                 |
| **Financial**        | Savings obscured by ingredient price volatility | Track waste volume (KG) as primary KPI, with cost as a secondary metric.                 |


### **7. FINANCIAL IMPACT & SUCCESS METRICS**

- **Current State:** 4.5% COGS variance ($11,970/store/month) equating to **$2.16M annual loss**.
- **Target:** 25% reduction in waste costs, adding **$540,000 to annual EBITDA**.
- **Valuation Uplift:** At an 8x EBITDA multiple, Project Phoenix adds **$4.3M to enterprise value**.
- **Additional Benefits:** Reduced disposal fees, labor efficiency gains, and enhanced brand equity.


### **8. CONCLUSION**

Project Phoenix represents a fundamental shift in operational philosophy—from viewing waste as an inevitable cost to treating it as a manageable data asset. By systematically implementing measurement, analysis, intervention, and automation, SavoryBites will not only recover significant lost profit but also position itself as a leader in sustainable, efficient dining.

The initiative requires committed leadership, cross-functional collaboration, and a focus on long-term cultural change. Success will be measured not only in dollars saved but in the establishment of a resilient, data-driven operating model capable of sustaining competitive advantage in the evolving casual dining landscape.

**APPROVED FOR EXECUTION**

*Document Version Control: This document is the source of truth for Project Phoenix. Any deviations from defined processes or data standards must be approved by the Project Lead.*