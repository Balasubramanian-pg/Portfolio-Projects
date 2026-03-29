## Sprint 2.3

**Instagram vs Wallet**
**Sentiment and Language Signals**

---

### 1. Objective

Convert messy human language into **structured regret signals** that reveal:

* Expectation gaps
* Emotional reversal
* Hidden drivers of returns

This is not NLP for decoration.
It is extracting **why the decision broke after purchase**.

---

### 2. Problem Reframing

Numerical data tells you:

* what happened

Language tells you:

* **why it happened**

Ignoring text means:

* You model behavior without understanding intent

---

### 3. Data Sources for Language

Primary text inputs:

* Return reason descriptions
* Customer support chats
* Product reviews
* Instagram comments (pre-purchase context)

Each plays a different role:

| Source             | Stage         | Value                 |
| ------------------ | ------------- | --------------------- |
| Instagram comments | Pre-purchase  | Expectation formation |
| Reviews            | Mid-cycle     | Product reality       |
| Return reasons     | Post-purchase | Regret expression     |
| Support chats      | Post-purchase | Emotional intensity   |

---

### 4. Signal Types

#### A. Expectation Mismatch Signals

Core regret indicator.

Examples:

* “Not as shown”
* “Looks different in real life”
* “Expected better quality”

Interpretation:

* Gap between **perception vs reality**

---

#### B. Emotional Reversal Signals

Examples:

* “Changed my mind”
* “Impulse buy”
* “Don’t need it anymore”

Interpretation:

* Decision instability, not product failure

---

#### C. Fit and Context Signals

Examples:

* “Didn’t suit me”
* “Fit is off”
* “Doesn’t match my style”

Interpretation:

* Personal mismatch, often regret not defect

---

#### D. Social Influence Signals

Examples:

* “Saw this on Instagram”
* “Looked great on influencer”

Interpretation:

* External influence driving decision

---

### 5. Preprocessing Pipeline

Minimal but critical steps:

1. Lowercasing
2. Stopword removal
3. Lemmatization
4. Noise removal (URLs, emojis, spam)

Do not over-clean:
You may remove signal.

---

### 6. Feature Extraction Approaches

#### A. Keyword-Based (Fast, Interpretable)

Create dictionaries:

* mismatch_terms
* impulse_terms
* fit_terms

Generate features:

* binary flags
* term frequency

Pros:

* Transparent
  Cons:
* Limited coverage

---

#### B. Sentiment Scoring

Compute:

* polarity score
* intensity score

But note:

* Negative sentiment ≠ regret
* Defects also produce negative sentiment

---

#### C. Topic Modeling

Use:

* LDA or clustering

Goal:

* Discover hidden themes

Example output:

* “size issues” cluster
* “quality mismatch” cluster

---

#### D. Embeddings (Advanced)

Use:

* sentence embeddings

Benefits:

* Capture semantic meaning
* Handle unseen phrases

Tradeoff:

* Less interpretable

---

### 7. Derived Features

Examples:

* `mismatch_score`
* `impulse_signal_flag`
* `fit_issue_probability`
* `sentiment_intensity`

Interaction features:

* sentiment × velocity
* mismatch × discount

---

### 8. Pre vs Post Purchase Language

Critical distinction:

#### Pre-Purchase (Instagram Comments)

* Builds expectations

#### Post-Purchase (Returns, Reviews)

* Reveals reality

Gap between them = **regret signal**

---

### 9. Core Insight: Language Gap Metric

Define:

> **Expectation Gap = Pre-Purchase Hype – Post-Purchase Reality**

Operationalization:

* High positive sentiment in comments
* Negative sentiment in returns

This gap is a **direct regret indicator**

---

### 10. Failure Modes

#### 1. Treating All Negative Text as Regret

* Mixes defect with regret

---

#### 2. Ignoring Context

* Same phrase, different meaning

---

#### 3. Overfitting Keywords

* Misses new language patterns

---

### 11. Unorthodox but High-Leverage Feature

#### “Surprise Index”

Measure:

* Frequency of words indicating unexpected outcome

Examples:

* “actually”
* “surprisingly”
* “didn’t expect”

Interpretation:

* Higher surprise → higher regret probability

---

### 12. Validation Strategy

* Compare text signals vs structured features
* Check if language improves prediction
* Validate against known regret cases

---

### 13. Definition of Done

* Text sources identified and ingested
* Preprocessing pipeline built
* Feature extraction implemented
* Key signals validated
* Integrated into feature schema

---

### 14. What This Enables

Language signals unlock:

* Explainable models
* Better interventions
* Deeper behavioral understanding

---

Numbers tell you the decision happened.
Language tells you the decision was a mistake.
