## Overview of Sprint 2.1: Deterministic Rule Development

Think of this sprint as building a **watchtower system** for local businesses. Instead of guessing with machine learning, you are writing **explicit, inspectable rules** that say:

* “If this pattern appears → something is suspicious.”
* “If enough suspicious signals stack up → flag as ghost review.”

This approach is **transparent, fast, and controllable**, which is critical when protecting real local customers from being wrongly penalized.

---

## Phase 1: Requirements & Data Preparation

### 1. Define "Ghost Review" Criteria

You are setting the **legal definition of the crime before catching criminals**.

A ghost review, in a local economy context, typically includes:

* Reviews from users who **never physically visited** the location
* Coordinated attacks or **review bombing**
* Paid or automated **rating farms**
* Reviews posted via **VPN clusters or bot networks**

Why this matters:

* Every rule you write later depends on this definition
* Poor definition leads to **high false positives**, which damages trust

---

### 2. Map Available Data Attributes

You inventory your raw materials. Typical attributes:

* **User-level**: account age, number of reviews, activity patterns
* **Technical**: IP address, device ID, VPN/proxy detection
* **Temporal**: timestamp, frequency of reviews
* **Geospatial**: distance between reviewer and business
* **Content**: text similarity, sentiment, duplication
* **Behavioral history**: past reviews, patterns across businesses

Reasoning:

* Deterministic systems are only as strong as the **signals they can access**

---

### 3. Establish Success Metrics

Here, you define what “good” looks like.

Primary focus:

* **Precision (very important)**
  → Avoid falsely flagging real customers

Secondary:

* Recall (catching as many ghost reviews as possible)
* Latency (speed of detection)

Reasoning:

* In local economies, **false accusations hurt businesses and users immediately**

---

### 4. Extract Localized Sample Dataset

You collect:

* Reviews from **local businesses** (restaurants, salons, etc.)
* A mix of:

  * Normal organic reviews
  * Suspicious or known fake patterns

Reasoning:

* Your rules must reflect **local behavior**, not global averages

---

### 5. Establish Ground Truth

You manually label:

* “Ghost”
* “Genuine”

This becomes your **benchmark dataset**.

Reasoning:

* Without ground truth, you are tuning rules blindly

---

### 6. Conduct Exploratory Data Analysis (EDA)

You look for patterns such as:

* Sudden bursts of reviews
* Accounts created and used immediately
* Same wording across multiple reviews

Example insight:

* A bakery normally gets 5 reviews/day but suddenly gets 60 in 1 hour

Reasoning:

* EDA helps convert intuition into **quantifiable thresholds**

---

## Phase 2: Deterministic Rule Ideation

This phase is where you **convert patterns into rules**.

---

### 7. Account-Level Rules

Focus: user credibility

Examples:

* New accounts posting many reviews quickly
* Accounts reviewing only one business

Purpose:

* Detect **throwaway or bot accounts**

---

### 8. Temporal & Velocity Rules

Focus: timing anomalies

Examples:

* Sudden spike in review volume
* Multiple reviews within seconds

Purpose:

* Detect **coordinated campaigns**

---

### 9. Geolocation Rules

Focus: physical plausibility

Examples:

* Reviewer located far away with no travel history

Purpose:

* Critical for local businesses where **physical presence matters**

---

### 10. Network & Device Rules

Focus: technical fingerprints

Examples:

* Same IP used for multiple accounts
* Known VPN exit nodes

Purpose:

* Detect **infrastructure behind fake reviews**

---

### 11. Content-Based Rules

Focus: text patterns

Examples:

* Identical reviews across multiple businesses
* Generic templated praise or criticism

Purpose:

* Detect **copy-paste or automated content**

---

## Phase 3: Rule Engine Design & Implementation

Now you move from ideas to **structured logic**.

---

### 12. Establish Hard Thresholds

Convert vague ideas into numbers.

Example:

* “Spike” becomes:
  → > 3× average daily reviews within 2 hours

Reasoning:

* Deterministic systems require **clear boundaries**

---

### 13. Design Boolean Logic Matrices

Define how rules combine:

* **AND logic** → stricter (reduces false positives)
* **OR logic** → broader detection (increases recall)

Example:

* IF (Geo mismatch AND new account) → Ghost

Reasoning:

* This is where **precision vs recall tradeoff** is controlled

---

### 14. Implement Scoring / Weighting

Instead of binary rules, assign points:

Example:

* Geo mismatch = +3
* New account = +1
* Duplicate text = +2

Final rule:

* IF score ≥ 4 → Ghost

Reasoning:

* Allows **flexibility without full ML complexity**

---

### 15. Code the Rule Engine

Implementation layer:

* Python (batch or streaming)
* SQL (for data warehouse execution)

Typical flow:

1. Ingest review
2. Apply each rule
3. Aggregate score
4. Output classification

Reasoning:

* This becomes your **production detection system**

---

## Phase 4: Testing & Calibration

Now you pressure-test the system.

---

### 16. Execute Rules on Ground Truth

Run your engine against labeled data.

Output:

* Predicted vs actual classification

---

### 17. Analyze Errors

Two key error types:

* **False Positives**
  → Real users flagged as fake
* **False Negatives**
  → Fake reviews missed

Reasoning:

* Each type has different business impact

---

### 18. Calibrate & Document

You refine:

* Thresholds
* Rule combinations
* Scoring weights

Then document:

* Each rule
* Its threshold
* Why it exists

Reasoning:

* Ensures **transparency, auditability, and future scalability**

---

## How Everything Connects

This entire pipeline forms a loop:

1. Define → what is fake
2. Observe → find patterns
3. Encode → create rules
4. Test → measure accuracy
5. Refine → improve precision

It is less like training a black-box model and more like building a **custom rulebook for spotting suspicious behavior in a neighborhood**.

---

## Key Strengths of This Approach

* Fully explainable decisions
* Fast execution
* Easy to debug and adjust
* Works well with limited data

---

## Key Limitations

* Can miss sophisticated attackers
* Requires constant manual tuning
* Rules may become outdated over time

---

## What Requires Verification or Is Uncertain

* Exact thresholds such as “500 miles” or “300% spike”
  → These must be derived from your dataset via EDA
* Effectiveness of VPN detection
  → Depends on external IP intelligence services
* Ground truth labeling accuracy
  → Human bias can affect results

---

## Final Thought

This sprint builds the **first defensive wall**. It is not meant to be perfect. It is meant to be **reliable, interpretable, and fast**, forming the foundation before introducing more advanced techniques like machine learning in later stages.

If you want, I can next:

* Convert this into an actual Python rule engine
* Or design a scoring schema tailored to your dataset structure
