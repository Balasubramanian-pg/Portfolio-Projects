# Project Bible — Pet Wellness Tracker

**Project duration**: 12 weeks (internship)
**Primary tools**: Python, SQL, IoT (Arduino / Raspberry Pi / ESP32), Power BI, Figma
**Client**: PawsCare Vet Clinics — 50 clinics (given)
**Primary aim**: Convert fragmented records and passive reminders into a real-time, IoT-enabled pet wellness system that reduces missed appointments, lowers obesity-related visits, and delivers a high-adoption owner app.

---

## Executive summary

This project turns disordered clinic data and unreliable reminders into a production-ready Pet Wellness Tracker: an end-to-end system that ingests wearable collar telemetry and clinic EHR/OCR data, runs predictive models to flag at-risk pets, generates personalized diet and exercise plans, and surfaces action items through a Vet Dashboard and Owner App. Expected near-term business outcomes are reduced no-shows, fewer obesity-related visits, measurable cost savings, and improved owner engagement. Key technical risks include IoT reliability, OCR accuracy for handwritten notes, model false positives, and owner privacy concerns. Where external facts are cited, sources are shown inline. ([Association for Pet Obesity Prevention][1])

---

## Business context, objectives, and success criteria

### Business context

* PawsCare faces a 30% no-show rate and rising obesity-related conditions. These are driving inefficiencies and avoidable treatment costs estimated at $2,000,000/year (client data).
* Owners do not adopt existing manual processes. A modern, data-driven experience aims to increase appointment adherence and preventive care.

### Outcomes and success criteria (SMART)

* Reduce missed wellness appointments from 30% to 18% within 6 months after rollout (40% reduction in relative terms).
* Reduce obesity-related visits by at least 20% within 6 months for pets enrolled in the program.
* Achieve at least 80% adoption among active clients for the Owner App within 9 months of launch.
* Demonstrate a ROI via preventable-cost reduction targeting at least $520,000 in first-year savings (illustrative—see assumptions and calculations below).

---

## High-level timeline (12 weeks)

Week 0 to Week 2 — Discovery and architecture

* Stakeholder interviews, data inventory, security & compliance review, define KPIs, finalize hardware selection.

Week 3 to Week 6 — Ingestion, integration, and prototype dashboards

* OCR pipeline for legacy records, collar data ingestion, unified SQL schema, basic Power BI vet dashboard prototype.

Week 7 to Week 9 — Modeling and app prototype

* Train predictive models, implement diet rule engine, Figma owner app flows, integrate alerts.

Week 10 to Week 12 — Testing, deployment, handover

* Field pilot with 2 clinics, refine models, implement monitoring and SLOs, documentation and transfer to operations.

Deliverables are enumerated later under “Deliverables by phase”.

---

## Scope and boundaries

### In scope

* IoT collar telemetry ingestion using MQTT / HTTPS, local gateway for clinics when required.
* Digitization of legacy records via OCR and human-in-the-loop verification.
* Predictive models (XGBoost / LSTM hybrid or ensemble) for short-term risk flags. ([healthinformaticsjournal.com][2])
* Rule engine for auto-generating diet and exercise plans based on breed, age, weight, activity.
* Power BI dashboards for vets and basic owner app prototype in Figma plus API endpoints for app integration.

### Out of scope (unless explicitly requested)

* Full production-native mobile app (beyond prototype and minimal POC backend).
* Clinical-grade diagnostics or replacing licensed vet judgement.
* Integration with third-party pet insurance claims beyond basic export.

---

## Stakeholders and roles

* Executive sponsor: VP Clinical Operations (business priorities, budget).
* Project owner: Head Vet Operations (clinical acceptance).
* Technical lead: BI / Data Engineer (data platform, pipelines).
* ML lead: Data scientist (models, validation).
* Embedded systems lead: IoT engineer (firmware, mesh networks).
* UX lead: Product designer (Figma flows).
* Intern: implement core PoC pipelines, build dashboards, run pilot.
* Legal / Privacy counsel: review owner data collection rules and consent flows.

---

## Detailed technical architecture

### Logical components

* **Edge devices**: Smart collars (accelerometer, gyro, lick sensor, GPS optional, battery telemetry). Gateways: clinic hub (Raspberry Pi / ESP32) and owner smartphone bridging.
* **Ingestion layer**: MQTT broker + HTTPS ingestion endpoints. Edge-to-cloud secured with TLS and token-based authentication.
* **Staging & persistence**: Raw telemetry stored in time-series store or cloud blob, parsed into an event table and a normalized Pet profile table in SQL.
* **OCR pipeline**: PDF/scan ingestion, image pre-processing, Tesseract-based OCR for printed text, hybrid approach for handwritten notes with human review. Tesseract is strong for printed text but limited for varied handwriting; plan for human-in-the-loop validation. ([Unstract.com →][3])
* **Feature store**: Precomputed time-window aggregates for ML models, weight history, vaccination schedules.
* **Model serving**: Containerized model endpoints (FastAPI / Flask), with batch scoring for historical backfills and streaming inference for real-time alerts. Hybrid ensemble approach recommended: XGBoost for engineered features and LSTM for raw time-series patterns. ([healthinformaticsjournal.com][2])
* **Business logic & rule engine**: SQL-based substitution rules for diet plans plus a lightweight orchestrator for A/B tests.
* **Presentation layer**: Power BI vet dashboards for decision support and a REST API for the Owner App to pull alerts and schedule bookings.
* **Observability & SLOs**: Telemetry on ingestion latency, model drift, collar connectivity rates, and app delivery success.

### Security and privacy

* Use industry IoT guidance and testing (OWASP IoT guidance) for device hardening and API security. Implement device authentication, encrypted transport, and firmware signing. ([OWASP][4])
* Explicit owner consent flows in the Owner App and opt-out or incognito mode for owners uncomfortable with continuous activity tracking.
* Note: HIPAA does not apply to veterinary records, however local privacy laws and best practices require strict data governance. Engage legal counsel for jurisdiction-specific compliance. **ASSUMPTION**: Client desires HIPAA-like protections.

---

## Data model (summary)

Core entities and recommended columns

* `pets`

  * `pet_id`, `owner_id`, `name`, `species`, `breed`, `dob`, `sex`, `neutered`, `microchip_id`

* `owners`

  * `owner_id`, `name`, `contact_phone`, `contact_email`, `consent_flags`

* `clinic_visits`

  * `visit_id`, `pet_id`, `clinic_id`, `visit_date`, `reason`, `diagnosis_codes`, `notes_original_doc`, `notes_text`

* `telemetry_events` (time-series)

  * `event_id`, `pet_id`, `timestamp`, `accel_x, accel_y, accel_z`, `step_count`, `lick_count`, `gps_lat`, `gps_long`, `battery_pct`

* `computed_features`

  * `pet_id`, `feature_name`, `start_ts`, `end_ts`, `value` (e.g., `activity_delta_24h`)

Schema design notes: normalize lookups, partition telemetry by time, and create materialized views for frequent aggregates.

---

## OCR pipeline design and checklist

### Goals

* Digitize 10k legacy records for initial training and matching to profiles. Use OCR to extract vaccination dates, weights, and key diagnoses.

### Steps

1. Pre-process PDFs: deskew, despeckle, contrast normalization, and split multi-page docs into images.
2. Use Tesseract for printed and typewritten text extraction. For handwritten notes, run handwriting detection and route to human validators or an ML handwriting model where feasible. Tesseract is effective for printed text but limited on handwriting. Budget manual validation for ~15 to 30% of records initially. ([Unstract.com →][3])
3. Implement regex parsers and named-entity extractors to capture structured attributes like “Rabies due 11/15/20XX” and “Weight 14.5 kg”.
4. Build an audit table to track confidence score and validation status.

---

## Predictive modeling and evaluation strategy

### Use cases

* Short-term risk flags: UTI, dehydration, acute injury, hyperactivity-related behavioral flags.
* Medium-term risk predictions: weight gain trajectory, obesity risk over 3 to 6 months.

### Model choices and rationale

* Use an ensemble: XGBoost for engineered aggregated features (activity deltas, heuristics like `squat_count`) and LSTM or temporal convolution networks for raw time-series pattern recognition. Hybrid ensembles have shown strong performance in mixed tabular plus time-series tasks. ([healthinformaticsjournal.com][2])

### Training data & features

* Inputs: rolling-window activity deltas (24h, 7d), lick/scratch rates, sleep patterns, historical weight trend, owner-reported symptoms.
* Labeling: use clinic diagnosis codes and vet annotations as ground truth. Add human-verified cases for edge conditions.

### Validation & monitoring

* Use time-based cross-validation and backtesting. Monitor precision at targeted recall thresholds to control false alert rate. Maintain a model drift pipeline and alert on performance decay.

---

## Diet and behavior rule engine

### Approach

* Combine rule-based baseline plans with ML-recommended tweaks. Rules encode vet guidelines by breed and life stage and allow overrides. Example rule shown in the original doc is fine as a template. Provide A/B testing framework for rule vs ML plans.

### Safety guardrails

* All plans must be vetted by a licensed veterinarian before automated prescription changes. The system provides recommendation text and explanations for vets to review.

---

## Vet Dashboard and Owner App — UX & features

### Vet Dashboard (Power BI)

* Pet summary card with latest telemetry, risk score, medication and vaccination due dates, and quick action buttons.
* Clinic-level KPIs: daily no-show forecast, obesity cohort tracking, device connectivity heatmap.
* Drill-through to patient timeline with events and model explanations.

### Owner App (Figma prototype)

* Onboarding: consent, pet profile, brief questionnaire.
* Home: pet status, personalized plan, upcoming appointments, reward points for adherence.
* Alerts: vaccination due, high-risk flags, and local community features.
* Privacy control: toggle for incognito and data-sharing preferences.

---

## Deployment and operations

* Containerize services and use CI/CD for model and API releases.
* Use canary rollout for models and a staging clinic for verification.
* Implement log retention, SLOs for ingestion latency (< 5s for real-time alerts), and daily health checks for device connectivity (% connected collars per clinic).

---

## Testing, pilots, and validation

* Lab testing for edge devices.
* Field pilot with 2 clinics for 4 weeks to measure collar dropout rate, OCR extraction precision, and app adoption behaviors.
* A/B tests for diet plans and reminder strategies.
* Acceptance criteria for pilot: collar uptime > 80%, OCR precision > 85% on printed text, owner opt-in > 50% among contacted clients.

---

## Risks and mitigation

* **Sensor damage**: ~15% chew rate noted in pilot data. Mitigation: tougher straps, replaceable modules, low-cost fallback tags.
* **False positives / alarm fatigue**: tune thresholds, owner-specified sensitivity, include vet confirmation step before clinical outreach.
* **OCR failure on handwriting**: human-in-the-loop validation and gradually build handwriting models. ([Medium][5])
* **Privacy concerns**: offer incognito mode and granular consent.
* **IoT security**: follow OWASP IoT guidance and implement signed firmware, device auth, and regular pen testing. ([OWASP][6])

---

## Metrics and ROI calculation (with digit-by-digit arithmetic)

### Example 1 — No-show reduction

Given:

* Baseline no-show = 30%
* Target reduction = 40% relative

Compute new no-show:

1. Represent numbers as decimals: baseline = 0.30, reduction = 0.40.
2. Remaining fraction = 1 − 0.40 = 0.60.
3. New no-show = 0.30 × 0.60 = 0.18.

Digit-by-digit:

* 0.30 × 0.60

  * 3 0
  * × 6 0
  * Multiply 30 × 60 = 1800 (in hundredths), place decimal => 0.18

So new no-show = 18% (matches the business table sample).

### Example 2 — Obesity visit reduction and illustrative cost savings

Given:

* Baseline obesity visits = 120 per month
* After = 89 per month (example in case study)
* Compute percent change:

1. Absolute change = 120 − 89 = 31.
   Digit-by-digit: 120 − 89 = (120 − 80) − 9 = 40 − 9 = 31.

2. Relative change = 31 / 120 = 0.258333... => 25.8333% ≈ 25.83% ≈ 26% reported.

Digit-by-digit long division (31 divided by 120) abbreviated:

* 120 goes into 31 zero times, append decimal, 310 ÷ 120 = 2 remainder 70, 700 ÷ 120 = 5 remainder 100, etc => 0.25833.

### Cost savings illustration (ASSUMPTION: $2,000,000 preventable costs)

Compute illustrative savings if obesity-related costs fall by 26%:

1. 2,000,000 × 0.26 = ?
   Digit-by-digit:

   * 2,000,000 × 0.26 = 2,000,000 × (26 / 100) = (2,000,000 × 26) / 100.
   * 2,000,000 × 26 = 52,000,000.
   * 52,000,000 / 100 = 520,000.

So estimated saving = $520,000. **ASSUMPTION**: the entire $2M is evenly distributed and proportionally reducible by obesity visit reduction; this is illustrative and requires verification with finance.

---

## Deliverables by phase (concrete)

### Phase 1 — Weeks 0 to 2: Discovery & ingestion

* Inventory report of data sources with connection templates.
* Security and consent checklist.
* Detailed architecture diagram and ERD.

### Phase 2 — Weeks 3 to 6: ETL and OCR

* OCR pipeline code with confidence scoring and human validation UI.
* Unified SQL schema and staging scripts to produce the `pets` and `telemetry_events` tables.
* Prototype Power BI vet dashboard with sample datasets.

### Phase 3 — Weeks 7 to 9: Models and app prototype

* Trained XGBoost + LSTM ensemble notebooks, model card, and serving container. ([healthinformaticsjournal.com][2])
* Diet rule engine SQL procedures and A/B test plan.
* Figma prototype with user flows and annotated handoff notes.

### Phase 4 — Weeks 10 to 12: Pilot and handover

* Pilot report (2 clinics) showing collar connectivity, OCR accuracy, model precision/recall, owner opt-in rates.
* Ops runbook, deployment scripts, and monitoring dashboards.
* Final executive deck and handover documentation.

---

## Implementation checklist (practical tasks)

* [ ] Purchase or procure 150 test collars and 5 gateway kits.
* [ ] Set up dev MQTT broker and staging SQL instance.
* [ ] Implement OCR pre-processing pipeline and human validation backlog.
* [ ] Implement feature engineering ETL and compute baseline features.
* [ ] Train initial models and set up model serving.
* [ ] Create Power BI workspace and vet dashboard templates.
* [ ] Build Figma prototype for the Owner App and a minimal API backend for alerts.
* [ ] Run security scan and boarding checklist for pilot clinics.

---

## Testing matrix (selected)

* **Unit tests**: parser, ingestion, and rule engine logic.
* **Integration tests**: end-to-end telemetry to dashboard path.
* **Pilot QA**: Collar connectivity under real conditions, battery drain tests, OCR end-to-end for 100 scanned records.
* **Clinical safety review**: Vet approval workflow tests and forced vet confirmation for any medication suggestions.

---

## Monitoring and post-deployment maintenance

* Track the following daily metrics: collars connected per clinic, OCR throughput and error rate, number of alerts, false positive rate (owner/vet feedback), appointment booking conversion after alerts.
* Monthly model retraining cadence initially and drift alerts when key features shift beyond predefined thresholds.

---

## Appendix A — Sample SQL snippets

Example: diet rule update (as a template; production implementation should parameterize and avoid direct updates without vet sign-off).

```sql
UPDATE diets
SET plan = CASE
    WHEN age_months < 12 AND activity_level > 0.7 THEN 'Puppy Active: 450g/day'
    WHEN weight_kg > 35 THEN 'Weight Mgmt: 300g/day + 3 walks'
    ELSE plan
END
WHERE breed = 'Golden Retriever'
  AND approved_by_vet = TRUE;
```

---

## Appendix B — Sample ML training note (concise)

* Feature windows: 24h, 72h, 7d for activity deltas.
* Labels: ICD-like vet diagnosis mapping and vet-confirmed events.
* Model evaluation: precision at recall 0.7 for emergency-level alerts to keep false positives low.

---

## Citations for key technical and market claims

* Pet obesity prevalence and owner perception data. ([Association for Pet Obesity Prevention][1])
* Pet wearable market sizing and adoption trends. ([Grand View Research][7])
* OCR capabilities and limitations with Tesseract especially for handwriting. ([Unstract.com →][3])
* Hybrid XGBoost and LSTM approaches for combined tabular/time-series predictions. ([healthinformaticsjournal.com][2])
* OWASP IoT guidance and security testing recommendations. ([OWASP][4])
* Prior clinic no-show studies documenting a wide range of no-show rates in outpatient clinics. ([PMC][8])

---

## Reasoning summary

* I structured the plan into pragmatic phases mapped to a 12-week internship.
* For technical choices I prioritized proven open-source tools and hybrid approaches where they reduce risk: Tesseract for printed text, human verification for handwriting, and ensemble XGBoost + LSTM for mixed data types. ([Unstract.com →][3])
* Business KPIs are tied to measurable changes and sample arithmetic is shown so stakeholders can validate impact estimates. Assumptions are flagged where client data or financial allocation is required.

---

## Assumptions and items that require verification

List of what needs confirmation before work proceeds

1. **$2,000,000 figure** — ASSUMPTION that this is accurate and attributable to preventable obesity-related care costs. Verify with finance.
2. **Baseline 30% no-show** — ASSUMPTION provided by client. Recommend verifying using clinic scheduling logs for past 12 months. ([PMC][8])
3. **Owner contact coverage** — percentage of owners with smartphones and consent to push notifications. Verify via clinic CRM.
4. **Device procurement** — confirm which collar vendors are approved and service model (subscription vs hardware cost). Market data indicates rapid growth of pet wearables; vendor selection needed. ([Grand View Research][7])
5. **Legal constraints** — verify local laws governing animal health data privacy and any industry requirements. Consult legal team.
6. **OCR budget** — accuracy for handwriting is limited; plan budget for human validation and data labeling. ([Medium][5])

If any of the above cannot be verified, label the dependent deliverables as “conditional” and postpone associated assumptions in the schedule.

---

## Next immediate steps (recommended for week 0)

* Validate the six verification items above with named owners.
* Select 2 pilot clinics and get stakeholder signoff on pilot acceptance criteria.
* Procure a small batch of collars and a gateway for lab testing.
* Begin ingestion skeleton: set up MQTT broker and a staging SQL instance.

---

## Closing — what I will deliver if you say “Go”

* A full, versioned project folder containing architecture diagrams, ETL and OCR code, model notebooks, Power BI templates, Figma prototype links, the pilot plan, the testing matrix, and this project bible expanded into a living document for operations and follow-up sprints.

---

### Uncertainties that need verification (re-stated)

* Accuracy of financial numbers and how $2M maps into specific clinical activities.
* Real baseline no-show and owner smartphone penetration numbers.
* Vendor commitments for collars and expected maintenance/replacement rates.
* Jurisdictional privacy requirements and any license needed to deliver clinical recommendations.

---

If you want, I can immediately generate the following items next in this session without delay

* A detailed week-by-week 12-week Gantt with task owners and acceptance criteria.
* The SQL DDL for the unified schema plus sample ETL scripts to populate the first 10,000 records.
* A pilot consent form and in-app consent text for the Owner App.

Pick one and I will produce it now.

[1]: https://www.petobesityprevention.org/2021?utm_source=chatgpt.com "2021 Pet Obesity Survey Results"
[2]: https://healthinformaticsjournal.com/index.php/IJMI/article/download/1188/1095/2061?utm_source=chatgpt.com "LSTM and XGBoost Ensemble Model: An Approach for ..."
[3]: https://unstract.com/blog/guide-to-optical-character-recognition-with-tesseract-ocr/?utm_source=chatgpt.com "Open-Source OCR With Tesseract: A Practical 2026 Guide"
[4]: https://owasp.org/www-project-internet-of-things/?utm_source=chatgpt.com "OWASP Internet of Things"
[5]: https://joseurena.medium.com/tesseract-ocr-evaluating-handwritten-text-recognition-1c6db85b2e7f?utm_source=chatgpt.com "Tesseract-OCR: Evaluating Handwritten Text Recognition"
[6]: https://owasp.org/blog/2024/03/01/iot-security-testing-guide?utm_source=chatgpt.com "Introducing the OWASP IoT Security Testing Guide (ISTG)"
[7]: https://www.grandviewresearch.com/industry-analysis/pet-wearable-market?utm_source=chatgpt.com "Pet Wearable Market Size, Share & Growth Report, 2030"
[8]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11231932/?utm_source=chatgpt.com "Evaluation of no‐show rate in outpatient clinics with open ..."
