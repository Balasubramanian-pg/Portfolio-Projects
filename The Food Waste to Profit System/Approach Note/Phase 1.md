# **Phase 1: Manual Audit & Baseline Establishment**
## **"Operation Glass Kitchen"**

**Document Type:** Strategic Operating Procedure (SOP)
**Phase Status:** **CRITICAL / MANDATORY**
**Primary Tool:** Physical Logging (Clipboard) $\rightarrow$ Digital Aggregation (Excel)
**Duration:** Weeks 1-8 (Month 1-2)


### **1.0 Strategic Intent & Psychology**
We are initiating Phase 1 not to reduce waste immediately, but to **expose** it. Currently, SavoryBites suffers from "Waste Blindness." Staff sweep trim into the bin without thought, and burnt food is hidden to avoid reprimand.

**The Objective:**
To construct a statistically significant "Zero-Day" Baseline of waste volume, value, and root cause across all 15 locations.

**The Operational Philosophy:**
> "You cannot punish what you have just started to measure."

During Phase 1, we declare **Total Amnesty**. No staff member will be written up, reprimanded, or coached on *volume* of waste. The only disciplinary offense in Phase 1 is **failure to log**. This psychological safety is the only way to get accurate data rather than fabricated "safe" numbers.


### **2.0 The Operational Toolset**

To mitigate the "Wet Kitchen" environment (grease, water, heat), we employ a hybrid Analog/Digital approach.

#### **2.1 The Physical Capture Layer (The "Red Clipboard")**
We do not use tablets on the line in Phase 1. Tablets die, get dirty, and have input lag.
*   **Hardware:** Heavy-duty Red Aluminum Clipboards (Visual cue: Red = Critical).
*   **Location:** Installed at 3 key waste vectors:
    1.  **Prep Station:** (Vegetable/Meat trimmings).
    2.  **The Line/Expo:** (Burnt food, wrong orders, cold food).
    3.  **The Dish Pit:** (Plate waste/Customer returns).
*   **Instrumentation:** A waterproof "Cheat Sheet" of common Item Codes is attached to the wall above the clipboard (e.g., `FRY` = French Fries, `CHK-W` = Chicken Wings).

#### **2.2 The Digital Twin (The Excel Workbook)**
The digital record lives on the Store Manager's PC.
*   **File Name Protocol:** `SB_WasteLog_[StoreID]_[YYYY-MM].xlsx`
*   **Structure:**
    *   **Tab 1: `Input_Log`:** The data entry interface.
    *   **Tab 2: `Master_Price_List` (Hidden/Locked):** A protected sheet containing current SYSCO/Vendor pricing per unit.
    *   **Tab 3: `Dash_View`:** A simple PivotTable showing the manager their current week's total (Immediate feedback).


### **3.0 Data Elements & Taxonomy**

We standardize data entry to prevent "garbage in." Staff are trained on the following four elements.

#### **3.1 Category (The "State" of Food)**
| Category Code | Name | Definition | Example |
| :--- | :--- | :--- | :--- |
| **RAW** | Raw Ingredient | Food expired or spoiled *before* cooking. | Moldy tomatoes, grey ground beef. |
| **PREP** | Prepared (WIP) | Food cooked/chopped but *never served*. | End-of-night batch soup, over-prepped rice. |
| **COOK** | Production Error | Food ruined *during* the cooking process. | Burnt steak, dropped tray, oversalted sauce. |
| **PLATE** | Customer Waste | Food served and returned/rejected. | "Steak undercooked", "Hair in food", "Cold". |

#### **3.2 Reason Codes (The Root Cause)**
*   **OP (Over-Prep):** "We made too much."
*   **EXP (Expired):** "We didn't use it in time."
*   **QI (Quality Issue):** "It arrived bad / looks bad."
*   **HE (Human Error):** "I burnt/dropped it."
*   **CR (Customer Refusal):** "Guest didn't like it."

#### **3.3 The "Unit of Measure" (UOM) Control**
To avoid mathematical chaos, Excel validation restricts UOM selection:
*   **LB (Pounds):** *Standard.* Used for bulk items (Fries, Mash, Trim).
*   **EA (Each):** Used for distinct unit items (Burger Patty, Bun, Chicken Breast).
*   **PORT (Portion):** Used for completed dishes (e.g., A full "Cobb Salad" returned).


### **4.0 The "Life of a Waste Event" (Workflow)**

#### **Step 1: The Event (Kitchen Floor)**
*   *Scenario:* A line cook, Dave, accidentally drops a Rack of Ribs.
*   *Action:* Dave picks it up. instead of throwing it in the black bin, he walks to the **Scale**.
*   *Measurement:* Dave places ribs on scale. Reading: **1.5 lbs**.
*   *Logging:* Dave writes on the Red Clipboard:
    *   Time: `19:30`
    *   Item: `RIBS`
    *   Qty: `1.5`
    *   Reason: `HE` (Human Error)

#### **Step 2: The Audit (Manager's Office)**
*   *Time:* 10:30 PM (Closing).
*   *Action:* Manager retrieves clipboards from the 3 stations.
*   *Review:* Manager scans for legibility. "What is this? Chicken or Chickpeas?" Clarifies with Closing Chef.

#### **Step 3: Digitization (Data Entry)**
*   *Action:* Manager opens `SB_WasteLog_Store05.xlsx`.
*   *Typing:* Manager transcribes the ~25 lines from the clipboard.
*   *Automation:* Manager types "RIBS". The Sheet VLOOKUPs the `Master_Price_List` and auto-populates "Cost: $6.50".
*   *Completion:* File is saved to the **Cloud OneDrive/SharePoint Folder** (Automated sync).


### **5.0 Implementation Roadmap**

#### **Week 1: The "Soft Launch" (Culture)**
*   **Objective:** Deployment and Fear Reduction.
*   **Action 1:** Distribute Kits (3 Clipboards, 1 Analog Scale, 1 Digital Scale) to all 15 stores.
*   **Action 2: The Town Hall.** Every GM holds a meeting.
    *   *Script:* "We are bleeding money, but we don't know where. We need your help to find the leak. I promise: **No one gets fired for filling out this log.** Only for ignoring it."
*   **Action 3:** "Practice Days." Thurs-Sat of Week 1, staff practice using the scales. Data is discarded.

#### **Week 2-5: The "Hard Audit" (Execution)**
*   **Objective:** 30 Days of Contiguous Data.
*   **Routine:** Daily logging is mandatory.
*   **The Check:** Regional Directors (RDs) randomly spot-check Sharepoint folders at 9:00 AM. If a store hasn't uploaded yesterday's log, the GM gets a call.

#### **Week 6-8: Validation & Transition**
*   **Objective:** Cleanup.
*   **Action:** Central Data Analyst consolidates the 15 files.
*   **Sanity Check:**
    *   *Store A* logs 40lbs of waste/day.
    *   *Store B* logs 2lbs of waste/day.
    *   *Conclusion:* Store B is lying. RD visits Store B for a "Trash Can Audit" (Physically comparing the trash bag weight to the log).


### **6.0 Managing Resistance (Troubleshooting)**

| Complaint | Interpretation | Response / Mitigation |
| :--- | :--- | :--- |
| **"I don't have time to weigh during a Friday Rush."** | Valid concern regarding speed of service. | **Implement "The Sin Bin".** A clear plastic tub. During Peak Rush (6pm-8pm), waste is dumped into the Sin Bin. At 8:30pm, the "Lull", the Sin Bin is weighed and logged as "Aggregate Rush Waste." |
| **"The scale is broken / Battery dead."** | Operational friction. | Supply a backup Mechanical Analog Scale (Spring loaded). It never runs out of batteries. |
| **"This makes us look bad."** | Fear of management retribution. | **The Accuracy Incentive.** The store with the *most detailed* logs (regardless of waste amount) wins a Pizza Party. Rewarding *truth* creates psychological safety. |


### **7.0 Deliverables & Exit Criteria**

Phase 1 is complete when:
1.  **The Dataset:** We possess 15 Store Files x 30 Days of clean, categorized data.
2.  **The Baseline:** We can explicitly state: *"SavoryBites wastes **X%** of Purchased Food, valued at **$Y** annually."*
3.  **The Discovery:** We have identified the **"Big Five"** items that constitute >50% of the value loss (Pareto Principle).

>[!warning]
>**Data Quality Warning**
>If the Phase 1 audit reveals that waste is less than **2.5%** of sales, the data is invalid. Industry average is 4% - 10%. A result of 2% implies hidden waste (theft or unlogged throwing). We must re-audit "too good to be true" locations.