# Project Bible — Weather FOMO: Lost Revenue Weather Tracker (SunnyDays Resorts)

## Executive summary

SunnyDays Resorts, a 15-property beachfront chain, loses roughly 12 percent of annual revenue due to weather-driven cancellations and missed upsell opportunities. This project transforms weather from a reactive risk into a proactive revenue lever by combining historical analysis, predictive modeling, real-time alerts, and playbooks. The outcome simulated here is a 30 percent reduction in weather-driven revenue loss, equivalent to a $2.4 million annual improvement, plus ancillary revenue gains from targeted promotions.

**ASSUMPTION:** numeric figures below are simulated for planning and decision making. I cannot verify these simulated numbers against SunnyDays internal systems without access to their data.

---

## Goals and key performance indicators

### Business goals

* Predict weather-driven cancellations with at least 85 percent accuracy.
* Reduce weather-related revenue loss by 30 percent within six months of pilot completion.
* Increase ancillary revenue during adverse weather by 25 percent in pilot resorts.

### Measurable KPIs

* Cancellation prediction AUC-ROC, target 0.88 or above.
* Weather-related revenue loss, baseline $8,000,000 per year, target reduction $2,400,000 per year.
* Ancillary revenue uplift, baseline $1,200,000 per month, target $1,600,000 per month in 6 months for chainwide rollout scenarios.
* Manager action rate on alerts, target 70 percent within 24 hours.

---

## Problem framing and assumptions

### Problem statement

Last-minute weather events trigger cancellations and reduce onsite spend. Manual monitoring is too slow and produces inconsistent mitigation. The system must forecast risks and recommend actionable countermeasures 72 hours in advance.

### Core assumptions used in planning

* Baseline weather-related revenue loss is 12 percent of annual revenue, quantified at $8,000,000 per year.
* The resort chain comprises 15 properties with mixed capacity and seasonality.
* Historical data is available for at least five years for bookings, cancellations, and hourly weather for each resort location.
* Managers will accept automated, prescriptive alerts for pilot resorts after an initial A/B test.

**Note:** Where an assumption is material to a decision, it is labeled ASSUMPTION and listed later for verification.

---

## Data inventory and quality issues

### Primary data sources

* Booking and PMS SQL data, core fields: Booking_ID, Resort_ID, Check-in_Date, Check-out_Date, Booked_Rate, Paid_Rate, Cancellation_Flag, Cancellation_Reason, Guest_Type, Channel.
* Historical hourly weather from a weather provider, core fields: timestamp, precipitation_mm, temp_c, wind_kph, forecast_certainty_index.
* Events calendar spreadsheet: local events, festivals, sporting events, public holidays.
* Ancillary sales ledger: spa, F&B, activities, upgrades.

### Known data quality issues and remediation

* 20 percent of cancellations lack structured reasons. Remediation: impute using correlation to weather variables and manual sampling to validate.
* Inconsistent date formats across systems. Remediation: canonicalize to UTC and local resort timezones at ETL ingestion.
* Rate-limit gaps from weather API. Remediation: implement provider caching and a secondary fallback provider.

---

## Data model and ETL design

### Core tables and columns

* `bookings` (booking_id, resort_id, check_in_date, check_out_date, channel, capacity_pct_at_booking, booked_rate, cancellation_flag, cancellation_date, cancellation_reason)
* `weather_hourly` (resort_id, timestamp_local, precipitation_mm, temp_c, wind_kph, forecast_horizon_hours, forecast_certainty)
* `events` (resort_id, event_date, event_type, expected_attendance)
* `ancillary_sales` (sale_id, resort_id, datetime_local, category, amount)

### ETL pipeline (high level)

* Source extraction via scheduled jobs, hourly for weather, daily for bookings and ancillary.
* Standardization step: parse dates, normalize currency, map channels.
* Enrichment: attach 72, 48, and 24 hour forecast slices to bookings keyed by check-in datetime and resort.
* Imputation script for missing cancellation reasons using rule-based and ML techniques with human validation sampling.

---

## Analytical approach and models

### Phase 1: descriptive analysis

* Compute historical correlations between check-in day precipitation > 12.7 mm (0.5 inch) and cancellation rates per resort segmented by day-of-week, guest type, and booking lead time.
* Produce seasonal indices per resort to control for seasonality in modeling.

### Phase 2: cancellation risk model

* Model choice: gradient boosted trees for structured features, logistic output for probability.
* Input features: 3-day rainfall forecast, 24 hour forecast certainty, day-of-week encoded, stay_length, capacity_pct_at_booking, channel, local event indicator, historical cancellation propensity by guest segment.
* Output: cancellation probability per booking 72 hours before arrival.

### Phase 3: demand surge / upsell model

* Model choice: LSTM for short-sequence demand signals combined with tree-based feature inputs for events and weather.
* Output: expected ancillary lift and demand elasticity estimates for offers (discount thresholds, spa bookings, cabana upgrades).

### Model validation plan

* Train/test split by time with rolling backtests, cross validation by resort cluster.
* Performance metrics: AUC-ROC for cancellation model, precision@k for high-risk booking classification, mean absolute percentage error for demand forecasting.
* Target: AUC-ROC >= 0.85 for cancellation risk, precision > 0.7 at top 10 percent flagged bookings.

---

## Real-time alerting and dashboard design

### Alerting logic

* Alert window: 72 to 24 hours before check-in.
* Trigger conditions:

  * Cancellation risk >= 60 percent for high-value bookings (revenue > $X)
  * Predicted chain-level occupancy change > 10 percent versus baseline
  * Opportunity signal: predicted sunny weekend with local high-attendance event and available upsell inventory
* Alert payload: resort, date, flagged bookings, recommended action with expected financial impact and confidence.

### Delivery channels and integrations

* Power BI operational dashboard with flags and drilldowns.
* Automated messages sent to property manager Teams channels via Power Automate.
* Option to push SMS to central ops for urgent actions.

### Dashboard panels

* Risk heatmap by resort and date.
* Booking-level queue for manager triage.
* Recommended playbooks with estimated cost and expected revenue impact.
* Model performance monitoring and concept drift alerts.

---

## Mitigation playbooks (actionable by managers)

### Playbook A: Retain at-risk bookings

* Condition: cancellation probability >= 60 percent and booking value >= $350.
* Action sequence:

  1. Offer a one-time amenity (spa credit $40) for maintaining reservation.
  2. If still unconfirmed in 24 hours, auto-offer free flexible date change within 90 days.
* Cost estimate and expected impact per booking:

  * Cost per offer, $40.
  * Expected retention uplift per offer, 35 percent (ASSUMPTION).
  * Expected net revenue per retained booking, booked_rate minus cost measured in pilot.

### Playbook B: Rainy-day monetization

* Trigger: forecast precipitation on-site on guest day above 12.7 mm.
* Actions:

  * Promote "Rainy Day Spa Package" priced at $60 upcharge with 2 complimentary F&B vouchers.
  * Dynamic F&B bundled promotions for in-house guests.
* Expected uplift: increase ancillary spend by 18 percent among guests who redeem the package in pilot resorts.

### Playbook C: Dynamic capacity pricing for sunny spikes

* Trigger: predicted sunny weekend plus major local event with forecast certainty > 80 percent.
* Action:

  * Increase upgrade availability for poolside cabanas and premium breakfast add-ons with tiered pricing.
* Expected result: 15 percent incremental ancillaries on top of baseline for those weekends.

---

## Pilot design and sampling

### Pilot scope

* Select 4 resorts representing different profiles: high-season, low-season, family-oriented, and urban-adjacent.
* Duration: 12 weeks of live pilot including two major weekend events.

### Experimentation design

* Randomized A/B testing by booking cohort or by time-block for specific playbooks.
* Key metrics: cancellation rate, revenue retained per flagged booking, ancillary revenue per occupied room, guest satisfaction.

---

## Financial model and example calculations

### Baseline figures used (simulated)

* Annual weather-related revenue loss: $8,000,000. (ASSUMPTION)
* Baseline ancillary revenue: $1,200,000 per month.

### Calculate implied annual revenue from baseline loss

We derive chain annual revenue using the statement that 12 percent equals $8,000,000.

Digit-by-digit arithmetic:

* Step 1: Represent percentage as decimal: 12 percent = 0.12
* Step 2: Divide loss by decimal to get total revenue.

  * 8,000,000 divided by 0.12 equals:

    * 8,000,000 / 0.12
    * 8,000,000 / 0.12 = 66,666,666.66666667
* Rounded result: $66,666,667 approximately.

Result: implied annual revenue = $66,666,667 approximately.

### Calculate 30 percent reduction in loss

Digit-by-digit arithmetic:

* Step 1: 30 percent = 0.30
* Step 2: 8,000,000 times 0.30 equals:

  * 8,000,000 × 0.30
  * 8,000,000 × 0.30 = 2,400,000

Result: projected annual savings = $2,400,000.

### Post-implementation loss

Digit-by-digit arithmetic:

* Step 1: Remaining loss fraction = 1.00 - 0.30 = 0.70
* Step 2: 8,000,000 × 0.70 = 5,600,000

Result: expected weather-related loss after program = $5,600,000 per year.

### Ancillary revenue uplift example

* Baseline ancillary revenue per month = $1,200,000.
* Target after program = $1,600,000 per month.
* Monthly uplift = 1,600,000 − 1,200,000 = 400,000.

  * Digit-by-digit: 1,600,000 − 1,200,000 = 400,000.
* Annualized uplift = 400,000 × 12 = 4,800,000.

  * Digit-by-digit: 400,000 × 12 = (400,000 × 10) + (400,000 × 2) = 4,000,000 + 800,000 = 4,800,000.

Result: simulated ancillary revenue increase equals $4,800,000 per year if uplift holds chainwide.

### Example ROI calculations for two strategies

1. Dynamic pricing pilot per resort

   * Cost per resort: $12,000.
   * Revenue impact per resort (simulated): $100,000.
   * ROI = revenue impact / cost = 100,000 / 12,000.

     * Digit-by-digit: 100,000 ÷ 12,000 = 8.333333...
   * ROI = 8.33x.

2. Spa promotion per resort

   * Cost per resort: $5,000.
   * Revenue impact per resort: $19,000.
   * ROI = 19,000 / 5,000 = 3.8x.

     * Digit-by-digit: 19,000 ÷ 5,000 = 3.8

**ASSUMPTION:** the revenue impact values above are simulated pilot outcomes and must be validated.

---

## Risks, mitigations, and governance

### Top risks

* Model drift caused by atypical weather patterns or forecast changes.
* Manager resistance to automatic prescriptive offers.
* Customer dissatisfaction if offers appear coercive.

### Mitigations

* Retrain models monthly and monitor feature importances.
* Implement human-in-the-loop for first 2 months of rollout before fully automating offers.
* A/B test offer language and visible opt-in flows to ensure positive guest perception.

### Governance and compliance

* Data retention and privacy audits for guest PII.
* Clear logging of automated offers and manager overrides for auditability.

---

## Implementation roadmap (12 month view, high level)

### Months 0 to 2 — Discovery and data onboarding

* Complete data inventory, fix date issues, implement ETL templates.
* Deliverable: clean 5-year merged dataset for pilot resorts.

### Months 3 to 5 — Modeling and offline validation

* Build cancellation and demand models, run backtests.
* Deliverable: model artifacts and validation report.

### Months 6 to 8 — Pilot deployment

* Deploy alerting pipeline, Teams integration, and run A/B tests on 4 pilot resorts.
* Deliverable: pilot dashboard, performance summary, refined playbooks.

### Months 9 to 12 — Scale and governance

* Chainwide rollout based on pilot results, scale infrastructure, embed monitoring.
* Deliverable: SOPs, training materials, and executive summary of ROI.

---

## Deliverables and handoffs

* Technical: ETL scripts, model code notebooks, deployment manifests, container images, monitoring runbooks.
* Business: Power BI dashboard templates, manager playbooks with step-by-step actions, training video and FAQ, executive one-page ROI summary.
* Change management: manager training sessions and playbook acceptance sign-offs.

---

## Concise explanation of reasoning steps taken

* I converted the user-supplied narrative into a structured project bible by extracting objectives, mapping data requirements, and defining modeling and operational steps.
* I simulated numbers where the original text used percentages without a base, then derived implied totals to create financial scenarios.
* I applied common hospitality industry logic to design playbooks that are feasible and measurable in a pilot.
* Wherever results are simulated, I labeled them ASSUMPTION and marked them for verification.

---

## Items that require verification or are uncertain

1. Baseline number validation: confirm that weather-related loss equals $8,000,000 and that this represents 12 percent of annual revenue. I cannot verify this.
2. Availability and granularity of historical weather data per resort location and the associated forecast certainty metadata.
3. Completeness of cancellation reason fields and whether manual sampling is possible for validation.
4. Manager willingness and legal constraints for offering incentives and flexible date changes.
5. API rate limits and contract terms with chosen weather providers.
6. Any regional regulatory constraints for dynamic pricing or marketing messages.
7. Pilot budget approvals for per-resort experiments and costs used in ROI calculations.

---

## Next steps (practical, immediate)

* Validate baseline financial figures and data availability for five years across the 15 resorts.
* Approve pilot resort selection and pilot budget for the 4-resort experiment.
* Execute a rapid data readiness sprint to produce the merged bookings-weather dataset for pilot resorts.

---

If you want, I will now:

* produce the SQL schema and example ETL queries for the bookings to weather merge,
* draft the Power BI wireframe with exact visuals and filter interactions, or
* produce the Jupyter notebook outline and model training pipeline with hyperparameter defaults.

Pick one and I will generate the detailed artifacts next.
