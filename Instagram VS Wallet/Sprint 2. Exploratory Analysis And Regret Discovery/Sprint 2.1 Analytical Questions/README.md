## Sprint 2.1

**Instagram vs Wallet**
**Analytical Questions**

---

### 1. Objective

Define the **minimum set of questions that expose causal structure**, not just correlations.

Most teams ask:

* “What correlates with returns?”

Wrong level.

This sprint asks:

> “What forces convert Instagram exposure into regret?”

---

### 2. Framework

All questions must map to the decision chain:

> Exposure → Activation → Purchase → Reflection → Regret → Return

Each stage has different failure modes.
Your questions must isolate them.

---

### 3. Exposure Layer Questions (What drives desire?)

These test whether **Instagram creates unstable demand**.

* Do high-velocity trends produce higher regret rates than stable trends?
* Is **rate of change** (velocity spike) more predictive than total engagement?
* Does sentiment polarity correlate with regret, or is hype independent of quality?
* Do certain creators systematically generate higher regret outcomes?

Hidden angle:
You are testing whether influence quality varies across creators.

---

### 4. Activation Layer Questions (What triggers purchase?)

These identify **decision acceleration mechanisms**.

* How does discount depth interact with trend velocity?
* Are impulse purchases clustered in specific time windows (late night, weekends)?
* Does shorter session duration correlate with higher regret?
* Does device type (mobile vs desktop) change regret likelihood?

Core hypothesis:
Faster decisions → weaker evaluation → higher regret.

---

### 5. Purchase Context Questions (Who is vulnerable?)

These segment **customer susceptibility**.

* Do customers with high prior return rates exhibit stronger trend sensitivity?
* Is there a threshold effect in impulse_score beyond which regret spikes?
* Are new customers more vulnerable than repeat buyers?
* Does category familiarity reduce regret?

Uncomfortable truth:
Some customers are structurally prone to regret.

---

### 6. Product Layer Questions (What is inherently risky?)

Separate **bad decisions from bad products**.

* Which categories have high regret independent of trends?
* Do products with high size/fit variability amplify regret?
* Is baseline product return rate a dominant predictor?
* Are certain price bands more prone to regret?

Goal:
Prevent blaming behavior when the product is the problem.

---

### 7. Temporal Questions (When does regret emerge?)

Understand **regret dynamics over time**.

* What is the distribution of time-to-return?
* Does Instagram-driven regret peak earlier than organic purchases?
* Do high-velocity purchases return faster than low-velocity ones?
* Is there a decay curve for regret probability?

Key insight:
Timing reveals mechanism.

---

### 8. Interaction Questions (Where does signal actually live?)

Single variables rarely matter. Interactions do.

* Velocity × Discount → does this create super-linear regret?
* Velocity × Prior Return Rate → does amplification occur?
* Time of Day × Device → does mobile-night behavior spike regret?
* Creator × Category → are some creators mismatched with product types?

This is where most signal hides.

---

### 9. Counterfactual Questions (What would have happened otherwise?)

Without this, you cannot claim causality.

* Do similar products without Instagram exposure have lower regret?
* For the same customer, is regret higher when purchase is trend-driven?
* Do non-trending purchases behave differently under same discount?

You are testing:
Is Instagram causing regret, or just exposing it?

---

### 10. Negative Space Questions (What does NOT cause regret?)

Critical and often ignored.

* Are there high-velocity trends with low regret?
* Are there heavy discounts that do NOT increase regret?
* Are some customers immune to trend effects?

These define:

* Safe zones
* Stable strategies

---

### 11. Anomaly Questions (Where does the model break?)

Look for patterns that violate expectations.

* Low-velocity trends with high regret
* High-quality products with unexpected returns
* Customers with zero history suddenly returning

These often reveal:

* Missing variables
* Hidden mechanisms

---

### 12. Output of This Sprint

You are not producing charts.
You are producing:

* A ranked list of regret drivers
* A set of validated hypotheses
* A shortlist of high-signal interactions

---

### 13. Failure Modes

#### 1. Correlation Hunting

* Finding patterns with no causal grounding

#### 2. Aggregation Blindness

* Monthly averages hiding daily spikes

#### 3. Feature Isolation

* Ignoring interactions

---

### 14. Unorthodox but High-Leverage Move

#### Invert the Question

Instead of:

* “What causes regret?”

Ask:

* “What predicts **no regret under high-risk conditions**?”

This identifies:

* Protective factors
* Intervention opportunities

---

### 15. Definition of Done

* Questions mapped to decision chain
* Hypotheses defined for each layer
* Interaction effects identified
* Counterfactual framing included

---

### 16. What This Enables

This sprint determines:

* What features to engineer
* What models can learn
* What interventions can work

---

Bad questions produce elegant but useless analysis.
Good questions make the model almost inevitable.
