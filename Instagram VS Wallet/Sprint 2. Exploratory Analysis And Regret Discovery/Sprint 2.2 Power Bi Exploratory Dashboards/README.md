## Sprint 2.2

**Instagram vs Wallet**
**Power BI Exploratory Dashboards**

---

### 1. Objective

Translate raw exploratory analysis into **decision-grade visual systems**.

Not pretty charts.
Not KPI clutter.

Each dashboard must answer a **specific causal question about regret** and force a conclusion.

---

### 2. Design Principles

* One dashboard = one analytical question
* Every visual must lead to an action or hypothesis
* Interactions over aggregates
* Defaults expose anomalies, not averages

---

### 3. Data Model (Power BI Layer)

**Fact Table**

* `fact_instagram_purchase_outcomes`

**Dimensions**

* `dim_customer`
* `dim_product`
* `dim_creator`
* `dim_time`

**Key Measures**

* Return Rate = returns / purchases
* Regret Rate = regret_returns / purchases
* Avg Time to Return
* Exposure Intensity

---

### 4. Dashboard 1: Trend Velocity vs Regret

**Question:**
Does faster virality create unstable purchases?

**Visuals**

* X-axis: `trend_velocity_percentile`
* Y-axis: `regret_rate`
* Color: category
* Size: purchase volume

**Interaction**

* Filter by creator, category

**Expected Pattern**

* Non-linear spike at high velocity

**Action**

* Identify “toxic virality zones”
* Candidates for intervention

---

### 5. Dashboard 2: Regret Timing Curve

**Question:**
When does regret actually happen?

**Visuals**

* Histogram: `hours_to_return`
* Split by:

  * Instagram vs non-Instagram
  * High vs low velocity

**Expected Pattern**

* Peak within 24–72 hours for Instagram-driven purchases

**Action**

* Define intervention window

---

### 6. Dashboard 3: Discount × Velocity Interaction

**Question:**
Do discounts amplify impulse regret?

**Visuals**

* Heatmap:

  * X: `discount_pct_bucket`
  * Y: `velocity_bucket`
  * Color: regret_rate

**Expected Pattern**

* High discount + high velocity = extreme regret

**Action**

* Apply friction or warnings in this zone

---

### 7. Dashboard 4: Customer Susceptibility Map

**Question:**
Who is most vulnerable to regret?

**Visuals**

* Scatter plot:

  * X: `prior_return_rate`
  * Y: `regret_rate`
* Segmentation:

  * new vs repeat customers

**Expected Pattern**

* High prior return users amplify under trends

**Action**

* Target personalized interventions

---

### 8. Dashboard 5: Creator Risk Matrix

**Question:**
Are some creators systematically causing regret?

**Visuals**

* Table or scatter:

  * X: engagement_rate
  * Y: regret_rate
* Highlight:

  * high engagement + high regret

**Expected Pattern**

* Some creators drive hype without matching product reality

**Action**

* Flag creators
* Adjust promotion strategy

---

### 9. Dashboard 6: Product Risk Baseline

**Question:**
Is regret driven by product or behavior?

**Visuals**

* Bar chart:

  * product category vs baseline return rate
* Overlay:

  * trend-driven regret vs organic

**Expected Pattern**

* Some categories inherently unstable

**Action**

* Adjust merchandising or sizing info

---

### 10. Dashboard 7: Channel Comparison

**Question:**
Is Instagram fundamentally different?

**Visuals**

* Side-by-side:

  * Instagram vs non-Instagram
* Metrics:

  * regret rate
  * time-to-return

**Expected Pattern**

* Faster and higher regret in Instagram channel

**Action**

* Justify intervention investment

---

### 11. Dashboard 8: Negative Space (Stability Zones)

**Question:**
Where does regret NOT happen?

**Visuals**

* Filter:

  * high velocity but low regret
* Compare against:

  * high regret zones

**Expected Pattern**

* Stable creators or categories

**Action**

* Replicate success patterns

---

### 12. Interactivity Design

Required filters across all dashboards:

* Time range
* Category
* Creator
* Customer segment

Drill-through:

* From category → product → transaction

---

### 13. Failure Modes

#### 1. KPI Overload

Too many metrics → no insight

#### 2. Static Views

No slicing → no discovery

#### 3. Averages Only

Hides extreme behaviors

---

### 14. Unorthodox but High-Leverage Feature

#### “Explain This Spike” Button

User selects:

* abnormal point

System shows:

* top contributing factors
* feature breakdown

This turns dashboards into:

* investigation tools

---

### 15. Definition of Done

* All dashboards mapped to analytical questions
* Measures validated
* Interactions functional
* Key patterns observable
* Stakeholders can derive conclusions without guidance

---

### 16. What This Enables

These dashboards:

* Validate hypotheses from Sprint 2.1
* Surface high-signal features
* Guide feature engineering

---

A dashboard should not describe reality.
It should corner you into seeing what you were avoiding.
