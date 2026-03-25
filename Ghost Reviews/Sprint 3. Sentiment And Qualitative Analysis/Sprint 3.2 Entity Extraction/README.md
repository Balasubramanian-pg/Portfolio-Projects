## Overview of Sprint 3.2: Entity Extraction

If Sprint 3.1 taught your system to **feel the tone**, Sprint 3.2 teaches it to **recognize the actors, objects, and specifics inside the story**.

A review is not just “positive” or “negative.” It contains:

* People (“staff”, “manager”)
* Items (“pizza”, “haircut”)
* Places (“downtown branch”)
* Attributes (“service”, “pricing”, “cleanliness”)

Entity extraction transforms unstructured text into **structured, queryable components**. Instead of a blob of opinion, you now have a **map of what exactly is being talked about**.

---

## Why Entity Extraction Matters for Ghost Review Detection

Ghost reviews often fail at **specificity and consistency**.

They tend to:

* Avoid concrete details
* Repeat generic entities (“service”, “experience”)
* Mention irrelevant or incorrect entities
* Show unnatural uniformity across reviews

Entity extraction enables you to:

* Detect **generic vs specific narratives**
* Identify **incorrect or fabricated details**
* Track **coordinated mention patterns**
* Build **fine-grained behavioral signals**

---

## Phase 1: Problem Framing & Objectives

### 1. Define What “Entity” Means in This Context

In review analytics, entities include:

* **Business components**: food, staff, ambience
* **Products/services**: dishes, treatments, offerings
* **People roles**: waiter, manager, technician
* **Locations**: branches, neighborhoods
* **Attributes**: pricing, cleanliness, speed

You are not limited to traditional Named Entity Recognition (NER). You extend it into **domain-specific entities**.

---

### 2. Define Use Cases

Entity extraction will support:

* Ghost review detection
* Sentiment attribution (which entity is praised or criticized)
* Business insights (what customers talk about)
* Explainability (“flagged due to repeated mention of X”)

---

### 3. Align with Previous Sprints

Entity signals combine with:

* Sentiment (Sprint 3.1)
* Probabilistic model (Sprint 2.2)
* Rule engine (Sprint 2.1)

Example:

* Generic entities + extreme sentiment → suspicious
* Incorrect entity mention + geo mismatch → high risk

---

## Phase 2: Data Preparation

### 4. Collect Text Data

Sources:

* Review body
* Titles
* Comments

Ensure:

* No truncation
* Proper encoding

---

### 5. Text Cleaning

Steps:

* Normalize casing
* Remove noise (HTML, special characters)
* Handle emojis

---

### 6. Language Handling

If multilingual:

* Detect language
* Route to language-specific pipelines

---

### 7. Annotation for Training (If Custom Model)

Label entities manually:

Example:

* “The pasta was amazing but service was slow”

  * pasta → PRODUCT
  * service → ATTRIBUTE

Reasoning:

* High-quality annotations = high-quality extraction

---

## Phase 3: Entity Types & Taxonomy Design

---

### 8. Define Entity Categories

Core categories:

* PRODUCT (food, service items)
* SERVICE (experience elements)
* PERSON_ROLE (staff, manager)
* LOCATION (branch, area)
* ATTRIBUTE (price, quality, speed)

Optional:

* BRAND
* EVENT
* TIME

---

### 9. Domain-Specific Extensions

For local businesses:

Restaurant:

* Dish names
* Cuisine types

Salon:

* Haircut types
* Treatments

Healthcare:

* Procedures
* Symptoms

---

### 10. Hierarchical Taxonomy

Example:

* SERVICE

  * Speed
  * Friendliness
* PRODUCT

  * Food
  * Beverage

Reasoning:

* Enables deeper analysis and aggregation

---

## Phase 4: Entity Extraction Techniques

---

### 11. Rule-Based Extraction

Use:

* Keyword dictionaries
* Pattern matching

Example:

* “pizza”, “burger” → PRODUCT

Advantages:

* Simple
* Fast

Limitations:

* Limited coverage
* Hard to scale

---

### 12. Classical NER Models

Use:

* Conditional Random Fields (CRF)
* Hidden Markov Models (HMM)

Features:

* Word position
* Capitalization
* Context words

---

### 13. Deep Learning NER Models

Use:

* BiLSTM-CRF
* Transformer models (BERT, RoBERTa)

Advantages:

* Context-aware
* High accuracy

---

### 14. Pretrained Models

Use:

* spaCy NER
* Hugging Face models

Fine-tune for domain:

* Add custom entity labels

---

### 15. Hybrid Approach

Combine:

* Rule-based (for known entities)
* ML-based (for unknown patterns)

---

## Phase 5: Entity Feature Engineering

---

### 16. Entity Count

Number of entities in a review:

* Low count → generic
* High count → detailed

---

### 17. Entity Diversity

Measure:

* Unique entity types

Example:

* Only “service” repeated → low diversity

---

### 18. Entity Specificity Score

Compare:

* Generic: “food”
* Specific: “margherita pizza”

Assign higher score to:

* Specific mentions

---

### 19. Entity Consistency Across Reviews

Check:

* Are multiple reviews mentioning the same entities?

Ghost signal:

* Repeated identical entities across many reviews

---

### 20. Entity-Context Alignment

Check:

* Does entity match business type?

Example:

* Mentioning “sushi” in a bakery review → suspicious

---

### 21. Entity-Sentiment Pairing

Combine:

* Entity + sentiment

Example:

* “service” → negative
* “food” → positive

---

### 22. Entity Frequency Patterns

Track:

* How often each entity appears across reviews

Ghost signal:

* Sudden spike in mentions of a specific entity

---

## Phase 6: Advanced Qualitative Signals

---

### 23. Generic vs Specific Language Detection

Ghost reviews:

* “Great service, nice place”

Genuine reviews:

* “The butter chicken was slightly spicy and well-cooked”

---

### 24. Entity Co-Occurrence Patterns

Check:

* Which entities appear together

Example:

* “service + staff + rude” cluster

---

### 25. Missing Expected Entities

If a review lacks:

* Expected entities for that business

Example:

* Restaurant review without food mention

---

### 26. Contradictory Entity Mentions

Example:

* “Quick service” + “waited 40 minutes”

---

### 27. Entity Novelty Detection

Detect:

* Rare or first-time entity mentions

Could indicate:

* Genuine experience
* Or fabricated detail

---

## Phase 7: Scoring Framework

---

### 28. Entity-Based Risk Scoring

Example:

* Low entity count → +2
* Low diversity → +2
* Repeated entities → +3
* Incorrect entity → +4

---

### 29. Normalize Scores

Adjust for:

* Review length
* Business type

---

### 30. Combine with Other Signals

Final risk score includes:

* Deterministic rules
* Probabilistic model
* Sentiment score
* Entity score

---

## Phase 8: Evaluation & Validation

---

### 31. Evaluate Extraction Accuracy

Metrics:

* Precision
* Recall
* F1 score

---

### 32. Human Validation

Check:

* Are extracted entities meaningful?
* Do they match context?

---

### 33. Error Analysis

Common errors:

* Missing entities
* Incorrect classification
* Overgeneralization

---

## Phase 9: Deployment & Monitoring

---

### 34. Real-Time Extraction

Process:

* Extract entities during review submission

---

### 35. Monitor Drift

Track:

* New entity types
* Changing language patterns

---

### 36. Continuous Improvement

Update:

* Dictionaries
* Models
* Taxonomy

---

## How Entity Extraction Enhances Ghost Detection

Without entities:

* You know tone

With entities:

* You know **what exactly is being talked about**

This enables:

* Detection of generic spam
* Identification of coordinated narratives
* Fine-grained anomaly detection

---

## End-to-End Flow Summary

1. Collect review text
2. Clean and preprocess
3. Extract entities
4. Generate entity features
5. Score entity-based risk
6. Integrate with overall system

---

## Key Strengths

* Adds structural understanding
* Improves explainability
* Detects narrative patterns
* Enables deeper analytics

---

## Key Limitations

* Requires domain tuning
* Struggles with ambiguous language
* Dependent on training data quality
* May miss implicit entities

---

## What Requires Verification or Is Uncertain

* Optimal entity taxonomy for all business types
* Accuracy across different languages
* Effectiveness of entity-based scoring thresholds
* Generalization across regions

“I cannot verify this” for:

* Universal effectiveness of a single entity extraction approach across all datasets

Suggested next steps:

* Build domain-specific taxonomy
* Annotate sample data
* Test multiple NER models
* Continuously refine

---

## Final Perspective

This sprint gives your system **eyes for detail**.

It stops seeing reviews as emotional blobs and starts seeing:

* Objects
* Actors
* Attributes
* Context

Where sentiment tells you *how someone feels*,
entity extraction tells you *what they are talking about*.

Together, they turn raw text into **structured intelligence**.

---

If you want next, I can:

* Design a full entity schema for your dataset
* Provide Python code using spaCy or BERT NER
* Or integrate entity signals into your fraud detection model end-to-end
