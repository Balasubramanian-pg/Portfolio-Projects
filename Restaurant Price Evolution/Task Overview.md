## Overview and Scope

You are asking for a **28,000-word project bible** for the **Menu Price Evolution Tracker** internship project, using the full case context you provided.

A document of that size is best delivered **in structured parts**, so that:

* Each section remains readable and reviewable.
* You can validate assumptions, scope, and framing as we go.
* Nothing conceptual, technical, or business-critical is missed.

### Delivery Approach

* I will create a **true project bible**, not a slide outline or summary.
* This will read like a document used by senior analytics teams, product managers, and future interns.
* The final output will be suitable for:

  * Portfolio and interviews
  * Internal knowledge base
  * Conversion into a whitepaper or capstone report

### How This Will Be Delivered

* Total target length: ~28,000 words
* Delivery in **8 major parts**
* Each part will be 3,000–4,000 words
* Every part will be internally complete and logically connected

If this works for you, I will continue sequentially without skipping anything.

---

## Complete Project Bible Structure (Table of Contents)

### Part 1. Strategic Context and Problem Framing

1. Industry Context: Restaurant Pricing in the Post-Inflation Era
2. UrbanEats Diner Chain Overview
3. Margin Compression Mechanics in Multi-Location Restaurants
4. Why Menu Pricing Fails at Scale
5. Limitations of Spreadsheet-Driven Pricing
6. Stakeholder Landscape and Incentive Conflicts
7. Defining the Core Business Questions
8. Success Metrics and North-Star KPIs

### Part 2. Data Landscape and Systems Architecture

9. End-to-End Data Flow Architecture
10. Source Systems and Data Ownership
11. Menu Artifacts as Semi-Structured Data
12. OCR as a Data Engineering Problem
13. Cloud Architecture on AWS
14. Data Storage Strategy and Trade-offs
15. Security, Access Control, and Cost Management

### Part 3. OCR Engineering and Data Quality Framework

16. OCR Failure Modes in Real-World Menus
17. Image Preprocessing and Enhancement Techniques
18. Tesseract vs AWS Textract Decision Analysis
19. Human-in-the-Loop Validation Design
20. Accuracy Measurement and Error Taxonomy
21. Building a Reliable Menu Item Canon
22. Data Versioning and Lineage

### Part 4. Analytical Modeling and Time-Series Design

23. Menu Price History Modeling
24. Ingredient Cost Normalization
25. Wage Inflation as a Cost Driver
26. Time-Series Alignment Challenges
27. Margin Leakage Detection Logic
28. Loss Attribution Methodology
29. Statistical vs Business Interpretability

### Part 5. Competitive Intelligence System

30. Ethical Constraints in Competitive Data Collection
31. Crowdsourcing as a Data Acquisition Strategy
32. Incentive Design for User Submissions
33. Data Validation and Fraud Prevention
34. Price-Quality Positioning Framework
35. Market Segmentation by City and Cuisine
36. Benchmarking Logic and Confidence Scoring

### Part 6. Pricing Engine and Decision Systems

37. Philosophy of Restaurant Pricing Engines
38. Rule-Based vs Model-Driven Pricing
39. Business Rule Design and Safeguards
40. Location-Specific Elasticity Assumptions
41. Simulation and Scenario Testing
42. A/B Testing Framework
43. Risk Controls and Brand Protection

### Part 7. Visualization, Storytelling, and Change Management

44. Designing for Non-Technical Managers
45. Power BI Semantic Model Design
46. KPI Layer vs Insight Layer
47. Alerting and Exception Management
48. Translating Analytics into Action
49. Handling Resistance from Chefs and GMs
50. Training and Adoption Strategy

### Part 8. Business Impact, Governance, and Scaling

51. Measuring Financial Impact Credibly
52. Attribution vs Correlation Challenges
53. Data Governance and Ownership
54. Cost of Change vs Cost of Inaction
55. Scaling to 100+ Locations
56. Future Enhancements and ML Opportunities
57. Risks, Failure Modes, and Mitigations
58. Final Executive Narrative

---

## Part 1: Strategic Context and Problem Framing

### 1. Industry Context: Restaurant Pricing in the Post-Inflation Era

The restaurant industry has historically operated on thin margins, typically ranging between 3 percent and 8 percent net profit. Pricing decisions were often driven by intuition, local manager experience, and periodic competitor checks rather than continuous analytical rigor.

Post-2020 inflation fundamentally altered this equilibrium.

Ingredient costs became volatile rather than seasonal. Labor costs rose unevenly across cities. Customer price sensitivity increased while tolerance for perceived unfair pricing decreased. In this environment, static menus stopped being a neutral operational artifact and became an active source of financial risk.

UrbanEats’ experience reflects a broader industry pattern: pricing systems built for stability failed under volatility.

### 2. UrbanEats Diner Chain Overview

UrbanEats operates 12 mid-volume diner locations across diverse metropolitan markets including New York, Chicago, Austin, Dallas, and several secondary cities.

Key operational characteristics:

* Shared brand identity with localized menu variations
* Decentralized pricing authority at the location level
* Central procurement for some ingredients, local sourcing for others
* Mixed customer base of commuters, families, and tourists

This hybrid structure created hidden complexity. While the brand appeared unified to customers, internally it behaved like 12 semi-independent businesses making pricing decisions with inconsistent data.

### 3. Margin Compression Mechanics in Multi-Location Restaurants

Margin erosion at UrbanEats was not caused by a single factor. It emerged from the interaction of several forces:

* Ingredient inflation outpacing price updates
* Wage increases applied unevenly across cities
* Infrequent menu revisions due to printing and signage costs
* Manager reluctance to raise prices without justification

The 2023 audit exposed the consequence: one in five menu items were being sold at or below cost in certain locations.

This was not visible in aggregate financial reports. It was only detectable at the item-level, location-level, and time-series level simultaneously.

### 4. Why Menu Pricing Fails at Scale

Menu pricing systems fail at scale for structural reasons:

* Menus are treated as documents, not datasets
* Historical prices are overwritten rather than preserved
* Cost changes are tracked separately from menu prices
* Competitive intelligence is anecdotal

Excel exacerbated these issues. Files were duplicated, formulas diverged, and historical context was lost.

Once pricing becomes reactive rather than anticipatory, every price change is late by definition.

### 5. Limitations of Spreadsheet-Driven Pricing

Spreadsheets are optimized for calculation, not governance.

At UrbanEats, Excel pricing workflows suffered from:

* No single source of truth
* No audit trail for price changes
* No automated linkage to costs or competitors
* Manual updates prone to delay and error

The organization was making financial decisions using tools that could not answer basic historical questions, such as when a price last changed or why.

### 6. Stakeholder Landscape and Incentive Conflicts

Pricing touched multiple stakeholders with conflicting incentives:

* Corporate finance wanted margin recovery
* Local managers feared customer backlash
* Chefs prioritized ingredient quality and creativity
* Marketing worried about brand perception
* Customers wanted fairness and transparency

Any analytical system that ignored these tensions would fail, regardless of technical quality.

The project therefore required not only data engineering, but institutional empathy.

### 7. Defining the Core Business Questions

The project reframed pricing from “What should we charge?” to deeper questions:

* Which items are structurally unprofitable and why?
* Where do pricing inconsistencies harm brand trust?
* How do competitor prices constrain feasible price moves?
* Which adjustments improve margins without increasing complaints?

These questions shaped the entire system design.

### 8. Success Metrics and North-Star KPIs

The initiative defined success across three dimensions:

Financial:

* Gross margin improvement
* Reduction in below-cost items

Customer:

* Reduction in price-related complaints
* Improved perceived value scores

Operational:

* Reduction in cross-location price variance
* Faster response time to cost shocks

These metrics prevented local optimization from undermining global outcomes.

## Part 2: Data Landscape and Systems Architecture

### Purpose of This Section

This section establishes the **technical backbone** of the Menu Price Evolution Tracker. It explains how raw, chaotic menu artifacts are transformed into a governed, analytical system capable of supporting pricing decisions at scale.

The intent is not merely to describe tools, but to explain **why specific architectural choices were made**, what alternatives were rejected, and how the system balances accuracy, cost, scalability, and organizational trust.

---

## 9. End-to-End Data Flow Architecture

At a high level, the system follows a layered architecture designed to mirror the lifecycle of menu pricing decisions.

### Architectural Layers

1. **Data Ingestion Layer**

   * Physical and digital menu artifacts
   * Crowdsourced competitor menus
   * External economic datasets

2. **Processing and Validation Layer**

   * OCR pipelines
   * Image preprocessing
   * Human validation workflows

3. **Storage Layer**

   * Structured historical menu database
   * Semi-structured competitor pricing store
   * Reference and dimension tables

4. **Analytics and Modeling Layer**

   * Time-series price tracking
   * Cost correlation models
   * Benchmarking logic

5. **Presentation and Decision Layer**

   * Power BI dashboards
   * Alerting and rules engines
   * Manager-facing insights

Each layer is deliberately decoupled to allow changes without cascading failures across the system.

---

## 10. Source Systems and Data Ownership

A core early decision was to explicitly define **data ownership** at the source level.

### Primary Data Sources

#### Internal Sources

* Legacy menu PDFs
* Photographs of printed menus
* Handwritten chef specials
* Excel pricing sheets maintained by managers

Ownership:

* Corporate operations for official menus
* Local managers for temporary and seasonal items

#### External Sources

* Ingredient prices from USDA
* Wage data from BLS
* Competitor pricing via crowdsourced submissions

Ownership:

* Corporate analytics team

Explicit ownership reduced ambiguity during data disputes and validation escalations.

---

## 11. Menu Artifacts as Semi-Structured Data

Menus appear simple to customers, but from a data perspective they are **semi-structured documents with high variance**.

### Structural Challenges

* Inconsistent layouts across years and locations
* Price placement not tied to item names
* Seasonal inserts and handwritten notes
* Varying fonts, contrast, and image quality

Treating menus as either unstructured text or rigid tables proved insufficient. Instead, the system treats each menu as a **document composed of extractable entities**:

* Item name
* Description
* Price
* Category
* Location
* Effective date

This conceptual model informed OCR preprocessing and downstream schema design.

---

## 12. OCR as a Data Engineering Problem

OCR was not treated as a one-time extraction task, but as an **ongoing data engineering pipeline**.

### Why OCR Was Central

* 5 years of pricing history existed only in visual form
* Manual re-entry would introduce bias and inconsistency
* OCR accuracy directly affected margin calculations

### Failure Modes Identified Early

* Numeric hallucination under poor contrast
* Decimal misplacement
* Item name fragmentation
* Duplicate extraction across overlapping scans

These risks shaped the choice of tools and validation strategies.

---

## 13. Cloud Architecture on AWS

AWS was selected due to its flexibility, managed services, and compatibility with Python-based workflows.

### Core AWS Components

* **Amazon S3**

  * Raw menu images
  * Preprocessed images
  * OCR output logs

* **AWS Textract**

  * Advanced OCR for complex documents
  * Backup for low-confidence Tesseract outputs

* **AWS Lambda**

  * Event-driven OCR processing
  * Lightweight validation triggers

* **Amazon DynamoDB**

  * Real-time competitor pricing submissions
  * High-velocity, schema-flexible data

* **Amazon RDS or PostgreSQL**

  * Canonical historical menu database
  * Strong relational integrity

This hybrid architecture avoided overengineering while preserving extensibility.

---

## 14. Data Storage Strategy and Trade-offs

### Structured vs Semi-Structured Storage

The system deliberately used **multiple storage paradigms**.

#### Relational Database Use Cases

* Historical menu prices
* Item-to-ingredient mappings
* Location and category dimensions

Advantages:

* Strong consistency
* Complex joins
* Time-series analysis support

#### NoSQL Use Cases

* Competitor menu submissions
* Raw OCR outputs
* Validation feedback

Advantages:

* Flexible schema
* Rapid ingestion
* Cost efficiency for sparse data

This separation prevented analytical workloads from being polluted by noisy raw inputs.

---

## 15. Schema Design Principles

The schema was designed around **immutability and traceability**.

### Key Principles

* Prices are never overwritten
* Every price has an effective date range
* Source metadata is preserved
* Confidence scores are stored alongside extracted values

### Core Tables

#### menus

* menu_id
* location_id
* effective_start_date
* effective_end_date
* source_type

#### menu_items

* item_id
* standardized_item_name
* category
* is_core_item

#### menu_prices

* menu_id
* item_id
* price
* extraction_confidence
* source_image_id

This design enabled full historical reconstruction of any menu at any point in time.

---

## 16. Security, Access Control, and Cost Management

Although this was an internship project, security considerations were treated seriously.

### Access Controls

* Read-only access for most managers
* Write access restricted to ingestion pipelines
* Audit logging for price changes and overrides

### Cost Management Decisions

* OCR batch processing scheduled during off-peak hours
* Textract used selectively for low-confidence cases
* Archival policies for raw images after validation

These measures ensured the system remained financially justifiable.

---

## 17. Data Quality as a First-Class Concern

Data quality was not handled downstream. It was embedded at every layer.

### Quality Dimensions Tracked

* Accuracy
* Completeness
* Timeliness
* Consistency
* Traceability

Each extracted price carried metadata describing:

* Extraction method
* Confidence score
* Validation status
* Human reviewer if applicable

This transparency increased stakeholder trust.

---

## 18. Lineage and Auditability

Every analytical insight needed to be defensible.

### Lineage Capabilities

* From dashboard metric back to SQL query
* From SQL record back to OCR output
* From OCR output back to source image

This was critical when managers questioned recommendations or when finance audited margin claims.

---

## 19. Integration with Analytics and BI Tools

The storage layer was optimized for consumption by Power BI.

### Semantic Layer Design

* Pre-aggregated views for common KPIs
* Clear separation between raw facts and derived metrics
* Naming conventions aligned with business language

This reduced dashboard complexity and improved adoption.

---

## 20. Architectural Constraints and Known Limitations

No system is perfect, and documenting limitations was part of the project discipline.

### Known Constraints

* OCR accuracy still lower for handwritten cursive
* Competitor data subject to sampling bias
* Near-real-time pricing updates limited by menu board update cycles

Explicitly acknowledging these constraints prevented overconfidence in outputs.

---

## Reasoning Summary

This section was constructed by mapping business needs to technical capabilities, then justifying each architectural choice based on reliability, scalability, and stakeholder trust rather than novelty.

---

## Points Requiring Verification or Monitoring

* OCR accuracy rates over time as menu designs change
* AWS service costs as data volume grows
* Data latency between ingestion and dashboard availability
