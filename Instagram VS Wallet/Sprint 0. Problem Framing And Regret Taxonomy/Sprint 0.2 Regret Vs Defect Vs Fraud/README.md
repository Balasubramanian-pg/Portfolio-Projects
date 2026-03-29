## Sprint 0.2

**Instagram vs Wallet**
**Regret vs Defect vs Fraud**

---

### 1. Objective

Create a **hard boundary system** that cleanly separates three fundamentally different return drivers:

* Regret
* Defect
* Fraud

If these bleed into each other:

* Models become unusable
* Interventions become harmful
* ROI attribution becomes fake

This sprint is about **classification integrity**, not analysis.

---

### 2. First Principles Separation

At root, these three are not variations of the same thing. They are **different causal systems**:

| Dimension                | Regret                    | Defect               | Fraud                 |
| ------------------------ | ------------------------- | -------------------- | --------------------- |
| Origin                   | Mind (decision error)     | Product (failure)    | Intent (manipulation) |
| Timing                   | Post-purchase realization | On use or inspection | Strategic timing      |
| Predictable              | Yes                       | Partially            | Rarely                |
| Preventable pre-purchase | Yes                       | No                   | No                    |
| Business Response        | Influence behavior        | Fix supply chain     | Enforce controls      |

Most teams fail because they mix **psychology, engineering, and abuse** into one label.

---

### 3. Operational Definitions

#### A. Regret

A **reversal of purchase intent** after emotional or impulsive decision-making.

**Signals**

* Fast return cycles
* Trend-driven purchases
* Expectation mismatch language

**Example**

* “Looked better on Instagram”

---

#### B. Defect

A **failure of the product to meet functional or quality expectations**.

**Signals**

* Damage, missing parts
* Manufacturing inconsistency
* Repeat complaints for same SKU

**Example**

* “Zipper broke on first use”

---

#### C. Fraud

A **deliberate exploitation of the return system**.

**Signals**

* High-frequency returns with usage patterns
* Wardrobing behavior
* Inconsistent claims

**Example**

* Wearing once, then returning

---

### 4. Why This Separation Matters

Each category implies a completely different system:

| Category | Solution System                      |
| -------- | ------------------------------------ |
| Regret   | Behavioral nudges, decision friction |
| Defect   | Quality control, vendor management   |
| Fraud    | Policy enforcement, detection models |

Mixing them leads to absurd outcomes:

* Showing “fit advice” for defective products
* Blocking genuine customers due to fraud logic
* Ignoring real product issues

---

### 5. Decision Framework (Labeling Logic)

A return must pass through a **decision tree**, not a flat rule.

#### Step 1: Product Integrity Check

* Any evidence of damage, defect, or wrong item?
  → YES → **Defect**
  → NO → move forward

#### Step 2: Fraud Screening

* Suspicious behavior pattern?

  * High return frequency
  * Usage indicators
    → YES → **Fraud**
    → NO → move forward

#### Step 3: Behavioral Classification

* Remaining returns default to **Regret**, with subtyping

---

### 6. Feature-Level Separation

To enforce this at data level:

#### Regret Features

* Trend velocity exposure
* Discount depth
* Purchase timing (late-night, impulse)
* Customer prior behavior

#### Defect Features

* SKU-level defect rate
* Batch/lot issues
* Supplier quality metrics

#### Fraud Features

* Return frequency anomalies
* Time-to-return inconsistencies
* Cross-account patterns

Important:
Do not mix these feature spaces during modeling.

---

### 7. Edge Case Handling

#### Case 1: “Size Didn’t Fit”

* Could be regret or product issue

Resolution:

* High SKU-level fit issue → Defect
* Otherwise → Regret

---

#### Case 2: “Not as Expected”

* Could hide both regret and defect

Resolution:

* Combine with:

  * sentiment
  * timing
  * SKU history

---

#### Case 3: Repeat Returns

* Could be regret or fraud

Resolution:

* Pattern-based thresholding:

  * Consistent across products → Fraud
  * Trend-driven → Regret

---

### 8. Misclassification Costs

This is where most systems silently fail.

| Misclassification | Consequence                           |
| ----------------- | ------------------------------------- |
| Regret → Defect   | Lose chance to prevent future returns |
| Defect → Regret   | Blame customer, ignore product issue  |
| Fraud → Regret    | System gets exploited                 |
| Regret → Fraud    | Lose customers                        |

The worst error is:
**Calling regret fraud**

That destroys trust permanently.

---

### 9. Unorthodox but Necessary Rule

**Default Bias: Favor Regret over Fraud unless confidence is high**

Reason:

* False fraud accusations are costly
* Regret interventions are low-risk

Tradeoff:

* Slight fraud leakage
* But preserves customer trust

---

### 10. Final Taxonomy Output

Each return must be labeled as:

* `return_type = regret`
* `return_type = defect`
* `return_type = fraud`

Optional extension:

* `regret_subtype = impulse | mismatch | fit | rationalization`

---

### 11. Definition of Done

* Clear, non-overlapping definitions
* Decision tree implemented in logic
* Feature separation enforced
* Edge cases documented
* Stakeholder alignment achieved

---

### 12. What This Unlocks

This sprint enables:

* Clean training datasets
* Separate modeling pipelines
* Targeted interventions
* Accurate ROI attribution

---

This is not taxonomy work.
This is **damage control before scale**.

If you get this wrong, every downstream metric becomes a lie.
