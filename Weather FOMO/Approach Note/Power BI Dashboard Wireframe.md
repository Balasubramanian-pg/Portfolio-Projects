# Power BI Dashboard Wireframe

**Weather FOMO – Cancellation Risk & Revenue Opportunity Command Center**

This is a **real-world, executive-to-operator grade Power BI wireframe**, mapped one-to-one with the notebook outputs you approved. It is designed so a BI developer can build it without guesswork and a hiring manager can immediately recognize production thinking.


## 1. Dashboard purpose and audience

### Primary purpose

* Enable **72-hour proactive decisions** that reduce cancellations and increase ancillary revenue.
* Convert model outputs into **clear, defensible actions** for resort managers and central ops.

### Target users

* Resort General Managers
* Revenue Management Team
* Central Operations
* Executive leadership (read-only, summarized)


## 2. Data model feeding Power BI

### Fact tables consumed

* `booking_risk_scores`
* `revenue_opportunity_scores`
* `ancillary_daily_summary`
* `booking_outcomes_post_action`

### Core relationships

* `resort_id` → shared across all facts
* `date` → linked to `dim_date`
* `booking_id` → booking-level drillthrough only

**Design principle:**
Executives see aggregates. Managers see bookings. Nobody sees raw model internals.


## 3. Dashboard layout (single-page command view)

### Page name

**Weather Revenue Control Tower**


## 4. Top banner: Executive snapshot (above the fold)

### Visual: KPI tiles (4 tiles, left to right)

1. **Weather Cancellation Risk**

   * Metric: % of upcoming bookings flagged Amber + Red
   * Example display: `18.4% (↓ from 22.1% last week)`
   * Data: `booking_risk_scores`
   * Conditional formatting:

     * Green < 15%
     * Amber 15–22%
     * Red > 22%

2. **Revenue at Risk (Next 7 Days)**

   * Metric: Sum of booking value × cancellation probability
   * Example: `$1.42M`
   * Tooltip:

     * “Expected loss without mitigation”

3. **Recoverable Revenue**

   * Metric: Expected retained revenue if playbooks executed
   * Example: `$480K`
   * Logic:

     * Risked revenue × historical retention lift

4. **Upsell Opportunity Forecast**

   * Metric: Predicted incremental ancillary revenue
   * Example: `$210K`
   * Confidence band shown in tooltip


## 5. Central visual: Risk heatmap (decision driver)

### Visual type

* Matrix heatmap

### Rows

* Resort name

### Columns

* Check-in date (Next 7 days)

### Values

* Average cancellation probability

### Conditional color scale

* Green: 0.00–0.30
* Amber: 0.30–0.60
* Red: 0.60–1.00

### Interaction

* Clicking any cell:

  * Cross-filters all visuals
  * Enables booking-level drillthrough

**This is the visual managers live on.**


## 6. Right panel: Action recommendation engine

### Visual: Table with icons

| Resort      | Date | Risk Band | Recommended Action   | Expected Impact |
| ----------- | ---- | --------- | -------------------- | --------------- |
| Miami Beach | Sat  | Red       | Offer $40 Spa Credit | +$62K           |
| San Diego   | Sun  | Green     | Premium Cabana Push  | +$28K           |

### Logic

* Populated directly from model rules
* Sorted by **Expected Impact descending**

### UX rule

* One action per row
* No model jargon
* Business verbs only


## 7. Bottom left: Cancellation drivers explainer

### Visual: Horizontal bar chart

**Title:**
“What is driving cancellation risk?”

### Dimensions

* Rainfall intensity
* Forecast uncertainty
* Lead time
* Day of week
* Capacity pressure

### Values

* SHAP-style contribution score (normalized)

**Purpose:**
This visual defuses stakeholder pushback by explaining *why* the model flagged risk.


## 8. Bottom center: Upsell opportunity analyzer

### Visual: Scatter plot

* X-axis: Temperature (°F)
* Y-axis: Ancillary revenue per occupied room
* Size: Resort occupancy
* Color: Event vs non-event days

### Tooltip

* Expected uplift
* Confidence score
* Suggested promotion type

**Insight surfaced visually:**
“Sunny + event weekends create nonlinear revenue spikes.”


## 9. Bottom right: Intervention effectiveness tracker

### Visual: Before vs after bar chart

**Title:**
“Did actions work?”

### Metrics

* Cancellation rate (control vs action)
* Ancillary revenue per guest
* Guest satisfaction (if available)

### Filters

* Resort
* Date range
* Action type

**This closes the loop and builds trust.**


## 10. Drillthrough page: Booking-level triage

### Trigger

* Right-click from heatmap or action table

### Page contents

* Booking ID
* Guest segment
* Booking value
* Cancellation probability
* Weather forecast summary
* Recommended incentive
* Historical success rate for similar bookings

### Decision buttons (conceptual)

* “Approve Offer”
* “Override”
* “Ignore”

**ASSUMPTION:**
Actual approval actions may live outside Power BI depending on tooling.


## 11. Filters and slicers (global)

### Mandatory slicers

* Resort
* Date range
* Risk band
* Guest type
* Channel

### Hidden slicers (analyst only)

* Model version
* Forecast horizon
* Confidence threshold


## 12. Security and row-level access

### Row-level security rules

* Resort managers:

  * See only their resort(s)
* Central ops:

  * See all
* Executives:

  * Aggregated views only, no booking IDs


## 13. Refresh and performance strategy

### Refresh cadence

* Weather + risk scores: every 3 hours
* Ancillary actuals: daily
* Historical metrics: static

### Performance optimizations

* Import mode for aggregated tables
* DirectQuery avoided for booking-level pages
* Pre-aggregated measures for KPI tiles


## 14. What this dashboard demonstrates in interviews

* You design **decision systems**, not just visuals
* You understand **operational analytics**
* You bridge **ML → BI → action**
* You anticipate **trust, governance, and adoption**


## 15. Items that require confirmation or verification

1. Final definitions of “recoverable revenue” used by finance.
2. Whether booking approval actions occur inside or outside Power BI.
3. Availability of guest satisfaction data at booking or stay level.
4. Final RLS rules based on org structure.
5. Acceptable refresh frequency given weather API costs.


## 16. What I can generate next immediately

Choose one and I will build it end-to-end:

* A **Power BI DAX measure pack** for all KPIs and risk calculations
* A **manager-facing SOP / playbook document** tied to each risk band
* A **portfolio README + architecture diagram** suitable for GitHub or case study submission

Say the next one.