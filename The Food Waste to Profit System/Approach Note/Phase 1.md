# **Project Phoenix: Phase 1 - Manual Audit & Baseline Establishment**

**Objective:** To transition from intuitive understanding to data-driven awareness by establishing a accurate, quantified baseline of food waste across all SavoryBites locations.
**Timeline:** Months 1-2
**Primary Tool:** Microsoft Excel
**Key Stakeholders:** Head Chef, Restaurant Managers, Kitchen Staff, Finance Department

### **1. Overview & Purpose**

Currently, SavoryBites operates with an intuitive understanding that food waste is a problem. This phase is designed to replace that intuition with hard data. The primary output will be a **quantified baseline** of how much waste we generate, what we waste, why we waste it, and what it costs. This baseline is the fundamental cornerstone for all future waste reduction initiatives and for measuring the project's ultimate success.

> **Key Callout: Why Start Manual?**
> While IoT scales automate data collection, a manual audit is superior for initial discovery. It forces staff engagement, provides crucial context for the *reasons* behind waste, and is a low-cost, high-impact starting point that builds a culture of awareness from the ground up.

### **2. The Core Instrument: The Waste Log**

The entire phase revolves around a simple, standardized Excel workbook deployed to each location.

#### **The Waste Log Template (`SavoryBites_WasteLog_Template.xlsx`)**

This template will consist of three key sheets:

1.  **`Data_Entry` Sheet:** A user-friendly form for daily logging.
2.  **`Cost_Reference` Sheet:** A protected list of standard ingredient costs for consistency.
3.  **`Instructions` Sheet:** Clear, simple guidelines for staff.

**Sample Structure of the `Data_Entry` Sheet:**

| Date (dd/mm/yyyy) | Time (hh:mm) | Item Wasted | Category | Quantity | Unit | Reason | Estimated Cost ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 01/10/2023 | 14:30 | Prepped Onions | Raw Ingredient | 2.5 | kg | Over-Preparation | 5.00 |
| 01/10/2023 | 23:15 | Day-Old Bread | Prepared Food | 10 | units | Spoilage | 8.50 |
| 02/10/2023 | 20:45 | Beef Patty | Prepared Food | 4 | units | Customer Return | 12.00 |

**Definition of Log Fields:**
*   **Category:** `Raw Ingredient`, `Prepared Food`, `Plate Waste`, `Spoiled`
*   **Unit:** `kg`, `g`, `units`, `liters` (must be standardized).
*   **Reason:** `Over-Preparation`, `Spoilage`, `Trim Waste`, `Customer Complaint`, `Kitchen Error`, `Expired`

> **Key Callout: Standardized Costs**
> The `Cost_Reference` sheet is vital. It prevents arbitrary guesses and ensures data consistency. For example, it will define that "Prepped Onions" cost `$2.00/kg`. This allows the `Estimated Cost` in the log to be a calculated field (`=[@Quantity] * VLOOKUP([@[Item Wasted]], Cost_Reference, 2, FALSE)`), reducing error and bias.

### **3. Implementation Plan: Rollout & Training**

**Week 1: Preparation & Briefing**
*   Finalize the Waste Log template and cost reference list with the Head Chef.
*   Conduct a mandatory virtual briefing with all Restaurant Managers to explain the **"why"**—connecting waste reduction to cost savings, environmental impact, and potential for staff incentives.

**Week 2: On-Site Training & Launch**
*   Managers train their kitchen teams on the log during pre-shift meetings.
*   **Golden Rule:** **Every single item** destined for the compost/trash must be logged *first*.
*   Print and laminate quick-reference guides and place them near all waste bins.
*   Designate a "Waste Captain" (e.g., a sous-chef) per shift to ensure compliance.

**Weeks 3-6: Active Auditing Period**
*   All 15 locations log every waste item for four full weeks (covering various weekdays and weekends to capture accurate patterns).
*   Managers dedicate 5 minutes at the end of each shift to review the log for completeness.

**Week 7: Data Submission**
*   Managers email their completed Excel file to the central project lead (e.g., Operations Manager).

**Week 8: Data Consolidation & Analysis**
*   The project lead consolidates all 15 Excel files into a single master dataset.
*   Initial analysis begins to establish the baseline metrics.

### **4. Anticipated Challenges & Mitigation Strategies**

| Challenge | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Staff Pushback** ("This is extra work") | Data incompleteness renders the project useless. | **1. Leadership Buy-in:** Managers must participate actively. <br> **2. Create a Contest:** Offer a prize for the most complete and accurate log. <br> **3. Communicate the Vision:** Explain how this data will make their jobs easier in the long run (e.g., less prep, simpler inventory). |
| **Inconsistent Entries** | Data is messy and unreliable. | **1. Simplify the Log:** Use data validation drop-downs for Category, Unit, and Reason. <br> **2. Provide Clear Examples:** The `Instructions` sheet must have photo examples. <br> **3. Standardize Costs:** The `Cost_Reference` sheet automates cost calculation. |
| "Logging Amnesia" | Items are thrown away without being logged. | **1. Physical Reminders:** Place the log on a tablet or clipboard right next to the main waste bin. <br> **2. Peer Accountability:** The "Waste Captain" is responsible for reminding the team. |

> **Key Callout: Culture Over Technology**
> The success of Phase 1 is 10% technology and 90% change management. The goal is not just to collect data, but to foster a mindset of mindfulness and accountability around waste. The simple act of logging forces a moment of reflection that, in itself, begins to reduce waste.

### **5. Success Metrics & Deliverables**

By the end of Phase 1, we will have produced:

1.  **A Master Waste Dataset:** A single, consolidated Excel file containing ~4 weeks of waste data from all locations.
2.  **Baseline Key Performance Indicators (KPIs):**
    *   **Total Weekly Waste Cost:** (e.g., "We waste `$1,200` per week across all locations")
    *   **Average Waste Cost per Location:** (e.g., "`$80`/week")
    *   **Top 5 Wasted Items by Cost:** (e.g., "Beef, Avocado, Bread, Fries, Cream")
    *   **Primary Reasons for Waste:** (e.g., "60% is due to Over-Preparation")
3.  **Identification of Outliers:** Which location has the highest/lowest waste cost? Why?
4.  **Anecdotal Feedback:** Qualitative insights from staff on why waste occurs.

### **6. Next Steps: Handoff to Phase 2**

The validated baseline data and KPIs from Phase 1 will serve as the direct input for **Phase 2: Centralized Analysis & Insight Generation**. This data will be imported into a SQL database and Power BI to uncover the deep, actionable insights that will drive our reduction strategies.

**Document Version:** 1.0<br>
**Author:** [Your Name/Department]<br>
**Status:** Final Draft for Execution
