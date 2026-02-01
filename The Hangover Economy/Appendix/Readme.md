# Full Finance Model — ROI by Promotion Type

**Project:** The Hangover Economy — Post-Party Purchase Analyzer
**Deliverable:** Conceptual end-to-end finance model with line-by-line sample calculations for three promo types (Early Bird Bundle, Night Owl Deal, Wellness Kit). This is a parameterized model: every calculation is expressed so you can swap inputs (store count, base sales, discount, costs) to evaluate scenarios. Assumptions are clearly labeled. I show digit-by-digit arithmetic for the worked examples and list verification/uncertainty points at the end.

---

# 1. Executive summary

* Goal: quantify incremental revenue, incremental gross profit, and ROI for three promotion types over a 12-week campaign; provide break-even and sensitivity analysis.
* Approach: build a per-campaign, per-network finance model that is (a) computed weekly, (b) aggregated across pilot stores, and (c) exposes key levers (uplift, discount, cannibalization, promo cost).
* Outputs you’ll get from the model: incremental units, incremental revenue, incremental gross profit, campaign costs, net incremental profit, ROI (return on promo spend), break-even units, and 12-week cumulative figures.

---

# 2. Model structure, notation, and how to use it

## 2.1 Notation (variables)

* `N_stores` = number of pilot stores (integer)
* `T_weeks` = campaign length in weeks (integer)
* `base_units_week` = baseline weekly units sold of the targeted SKU(s) across the pilot (network-level)
* `price` = full retail price of an item (or combined price for a bundle) ($)
* `discount_pct` = percent discount applied to bundle or item (e.g., 20 means 20%)
* `bundle_price` = effective sale price after discount ($)
* `elasticity` = promo elasticity (% sales lift per % price drop). If elasticity = 1.2, a 10% price drop → 12% sales lift.
* `sales_lift_pct` = elasticity × discount_pct (percent)
* `new_units_week` = base_units_week × (1 + sales_lift_pct/100)
* `incremental_units_week` = new_units_week − base_units_week
* `unit_cost` = COGS per unit (cost to the retailer) ($)
* `gross_profit_per_unit` = bundle_price − unit_cost ($)
* `promo_marketing_cost_total` = total marketing/advertising spend for pilot campaign (over full T_weeks) ($)
* `promo_marketing_cost_week` = `promo_marketing_cost_total` ÷ T_weeks ($/week)
* `incremental_labor_cost_per_unit` = incremental staff cost per incremental unit sold ($)
* `cannibalization_pct` = share of incremental units that cannibalize other store sales (0–100%)
* `other_fixed_costs_total` = other fixed campaign costs across pilot (material, bundling, POS signage) ($)
* `ROI` = (Net Incremental Profit) ÷ (Total Promo Cost) — expressed as ratio or percent

## 2.2 Model steps (per week, network-level)

1. compute `bundle_price` (if discount applies)
2. compute `sales_lift_pct` and `new_units_week`
3. compute `incremental_units_week`
4. compute incremental revenue = `incremental_units_week × bundle_price`
5. compute incremental gross profit = `incremental_units_week × gross_profit_per_unit`
6. reduce incremental gross profit by `cannibalization_pct` (only the non-cannibalized portion is truly incremental)
7. subtract promo costs (marketing allocated per week, incremental labor × incremental_units_week, weekly share of other fixed costs)
8. compute net incremental profit and ROI.
9. aggregate across `T_weeks` for campaign totals.

---

# 3. Key assumptions (labelled as ASSUMPTION where needed)

ASSUMPTION A1: pilot scope is `N_stores = 50` stores (network-level base numbers will be expressed for 50 stores). You can change this.

ASSUMPTION A2: campaign length `T_weeks = 12` weeks.

ASSUMPTION A3: cannibalization default = `30%` (meaning 30% of incremental units would have been purchased anyway as other items; therefore only 70% of incremental gross profit is truly incremental). This is an assumption we will vary in sensitivity tests.

ASSUMPTION A4: Elasticity interpretation: elasticity = percent sales lift PER percent price drop. Example: elasticity 1.2 and discount 20% → sales lift = 1.2 × 20% = 24%.

ASSUMPTION A5: Costs such as unit_cost are constant across the campaign and don't step up dramatically with scale in the pilot.

ASSUMPTION A6: All figures are in US dollars for illustrative clarity.

(Every assumption above is modifiable in the spreadsheet or model.)

---

# 4. Input parameter table (baseline values used in the worked examples)

These baseline values are *example* inputs for the three promotions. You can change them later.

Common:

* `N_stores = 50`
* `T_weeks = 12`
* `promo_marketing_cost_total` (network, 12 weeks) = $3,000 (Early Bird), $2,000 (Night Owl), $2,000 (Wellness Kit) — sample allocation.
* `other_fixed_costs_total` (signage, packaging) = $1,500 per promo (one-time across pilot).

Promotion-specific baseline inputs:

1. Early Bird Bundle (sandwich + energy drink)

* `base_units_week` (network) = 1,000 bundles per week
* `sandwich_price` = 4.50
* `energy_drink_price` = 2.00
* `discount_pct` = 20
* `elasticity` = 1.2
* `sandwich_margin_pct` = 40% (=> sandwich_cost = 4.50 × (1 − 0.40) = 2.70)
* `drink_margin_pct` = 30% (=> drink_cost = 2.00 × (1 − 0.30) = 1.40)
* `incremental_labor_cost_per_unit` = $0.10

2. Night Owl Deal (free chips with alcohol purchase)

* `base_units_week` (network: alcohol purchases in target window that are eligible) = 500 alcohol transactions/week
* `alcohol_price_avg` = 6.00
* `chip_retail_price` = 1.00
* `chip_cost` = 0.30
* `discount_pct` (effective bundle discount) — because chips are free, discount relative to alcohol alone is: chip price / (alcohol_price) expressed differently. For modeling we will compute incremental revenue from additional alcohol units only, and cost of fulfilling free chips.
* `elasticity` (alcohol uplift per free chips incentive) = 0.10 (i.e., a modest 10% lift)
* `incremental_labor_cost_per_unit` = $0.05

3. Wellness Kit (electrolyte + painkiller + bottled water)

* `base_units_week` (network) = 300 kits/week
* `electro_price` = 2.50
* `painkiller_price` = 1.50
* `water_price` = 1.00
* `kit_price_discount_pct` = 10 (discount relative to sum of SKUs)
* `elasticity` = 0.8 (i.e., fairly responsive)
* `kit_unit_cost` = sum of component costs; assume component margins: electrolytes margin 45% (cost = 2.50×0.55=1.375), painkiller margin 50% (cost = 1.50×0.5=0.75), water margin 30% (cost = 1.00×0.7=0.70) → total cost = 1.375 + 0.75 + 0.70 = 2.825 (we will compute precisely below)
* `incremental_labor_cost_per_unit` = $0.08

---

# 5. Early Bird Bundle — detailed line-by-line worked example (network-level, weekly and 12-week totals)

## 5.1 Inputs (restating only those used)

* `base_units_week = 1,000`
* `sandwich_price = 4.50`
* `energy_drink_price = 2.00`
* `discount_pct = 20`
* `elasticity = 1.2`
* `sandwich_cost = 4.50 × (1 − 0.40) = 4.50 × 0.60 = 2.70` (digit-by-digit shown below)
* `drink_cost = 2.00 × (1 − 0.30) = 2.00 × 0.70 = 1.40`
* `unit_cost = sandwich_cost + drink_cost`
* `promo_marketing_cost_total = 3,000` (for 12 weeks)
* `other_fixed_costs_total = 1,500` (one-time for pilot)
* `incremental_labor_cost_per_unit = 0.10`
* `cannibalization_pct = 30` (0.30)

### 5.1.1 Calculate sandwich_cost step-by-step

* sandwich_price = 4.50
* sandwich_margin_pct = 40% → margin fraction = 0.40
* cost fraction = 1 − margin = 1 − 0.40 = 0.60
* sandwich_cost = 4.50 × 0.60

  * 4.50 × 0.60 = (4.50 × 6) ÷ 10
  * 4.50 × 6 = 27.00
  * 27.00 ÷ 10 = 2.70
* So `sandwich_cost = $2.70`

### 5.1.2 Calculate drink_cost step-by-step

* drink_price = 2.00
* drink_margin_pct = 30% → margin fraction = 0.30
* cost fraction = 1 − 0.30 = 0.70
* drink_cost = 2.00 × 0.70

  * 2.00 × 0.70 = (2.00 × 7) ÷ 10
  * 2.00 × 7 = 14.00
  * 14.00 ÷ 10 = 1.40
* So `drink_cost = $1.40`

### 5.1.3 Compute unit_cost and full bundle price

* `unit_cost = sandwich_cost + drink_cost`

  * sandwich_cost = 2.70
  * drink_cost = 1.40
  * unit_cost = 2.70 + 1.40

    * 2.70 + 1.40 = 4.10
* Full (no-discount) bundle price = sandwich_price + drink_price = 4.50 + 2.00

  * 4.50 + 2.00 = 6.50

### 5.1.4 Compute bundle_price after discount

* discount_pct = 20 → discount fraction = 20% = 0.20
* bundle_price = full_bundle_price × (1 − discount_fraction)

  * = 6.50 × (1 − 0.20)
  * 1 − 0.20 = 0.80
  * 6.50 × 0.80 = (6.50 × 8) ÷ 10
  * 6.50 × 8 = 52.00
  * 52.00 ÷ 10 = 5.20
* So `bundle_price = $5.20`

### 5.1.5 Compute gross_profit_per_unit

* gross_profit_per_unit = bundle_price − unit_cost

  * bundle_price = 5.20
  * unit_cost = 4.10
  * gross_profit_per_unit = 5.20 − 4.10

    * 5.20 − 4.10 = 1.10
* So `gross_profit_per_unit = $1.10`

### 5.1.6 Compute sales_lift_pct and new_units_week

* sales_lift_pct = elasticity × discount_pct

  * elasticity = 1.2
  * discount_pct = 20
  * 1.2 × 20 = (1.2 × 2) × 10
  * 1.2 × 2 = 2.4
  * 2.4 × 10 = 24.0

* So `sales_lift_pct = 24%`

* new_units_week = base_units_week × (1 + sales_lift_pct / 100)

  * sales_lift_pct / 100 = 24 / 100 = 0.24
  * 1 + 0.24 = 1.24
  * base_units_week = 1,000
  * new_units_week = 1,000 × 1.24

    * 1,000 × 1.24 = 1,000 × (1 + 0.24) = 1,000 + 240 = 1,240

* So `new_units_week = 1,240`

### 5.1.7 Compute incremental_units_week

* incremental_units_week = new_units_week − base_units_week

  * = 1,240 − 1,000 = 240
* So `incremental_units_week = 240`

### 5.1.8 Compute incremental revenue (weekly) and incremental gross profit (weekly)

* incremental_revenue_week = incremental_units_week × bundle_price

  * incremental_units_week = 240
  * bundle_price = 5.20
  * 240 × 5.20 = 240 × (5 + 0.2) = 240 × 5 + 240 × 0.2

    * 240 × 5 = 1,200
    * 240 × 0.2 = 48
    * Sum = 1,200 + 48 = 1,248
  * So `incremental_revenue_week = $1,248`

* incremental_gross_profit_week = incremental_units_week × gross_profit_per_unit

  * incremental_units_week = 240
  * gross_profit_per_unit = 1.10
  * 240 × 1.10 = 240 × (1 + 0.10) = 240 + 24 = 264
  * So `incremental_gross_profit_week = $264`

### 5.1.9 Apply cannibalization adjustment (true incremental gross profit)

* cannibalization_pct = 30% → cannibalization_fraction = 0.30
* non_cannibalized_fraction = 1 − 0.30 = 0.70
* true_incremental_gross_profit_week = incremental_gross_profit_week × non_cannibalized_fraction

  * = 264 × 0.70
  * 264 × 0.7 = (264 × 7) ÷ 10
  * 264 × 7 = 1,848
  * 1,848 ÷ 10 = 184.8
  * So `true_incremental_gross_profit_week = $184.80`

### 5.1.10 Weekly incremental labor and allocated weekly marketing

* incremental_labor_cost_week = incremental_units_week × incremental_labor_cost_per_unit

  * incremental_units_week = 240
  * incremental_labor_cost_per_unit = 0.10
  * 240 × 0.10 = 24.0
  * So `incremental_labor_cost_week = $24.00`

* promo_marketing_cost_week = promo_marketing_cost_total ÷ T_weeks

  * promo_marketing_cost_total = 3,000
  * T_weeks = 12
  * 3,000 ÷ 12 = 250.0
  * So `promo_marketing_cost_week = $250.00`

### 5.1.11 Compute net incremental profit (weekly)

* net_incremental_profit_week = true_incremental_gross_profit_week − promo_marketing_cost_week − incremental_labor_cost_week − (allocated share of other fixed costs per week)

  * other_fixed_costs_total = 1,500 → per week allocation = 1,500 ÷ 12 = 125.00
  * true_incremental_gross_profit_week = 184.80
  * Subtract marketing 250.00 → 184.80 − 250.00 = −65.20
  * Subtract labor 24.00 → −65.20 − 24.00 = −89.20
  * Subtract other_fixed_costs_week 125.00 → −89.20 − 125.00 = −214.20
  * So `net_incremental_profit_week = −$214.20` (a weekly loss under these baseline assumptions)

### 5.1.12 12-week totals (aggregate)

* incremental_gross_profit_total_12w = incremental_gross_profit_week × 12

  * 264 × 12 = (264 × 10) + (264 × 2) = 2,640 + 528 = 3,168
* true_incremental_gross_profit_total_12w = true_incremental_gross_profit_week × 12

  * 184.8 × 12 = (184.8 × 10) + (184.8 × 2)

    * 184.8 × 10 = 1,848.0
    * 184.8 × 2 = 369.6
    * Sum = 1,848.0 + 369.6 = 2,217.6
* incremental_labor_total_12w = 24 × 12 = 288
* promo_marketing_cost_total = 3,000 (given)
* other_fixed_costs_total = 1,500 (given)
* net_incremental_profit_total_12w = true_incremental_gross_profit_total_12w − promo_marketing_cost_total − incremental_labor_total_12w − other_fixed_costs_total

  * = 2,217.6 − 3,000 − 288 − 1,500
  * 2,217.6 − 3,000 = −782.4
  * −782.4 − 288 = −1,070.4
  * −1,070.4 − 1,500 = −2,570.4
  * So `net_incremental_profit_total_12w = −$2,570.40`

### 5.1.13 Compute ROI (definition: Net incremental profit ÷ Total promo cost)

* Total promo cost = promo_marketing_cost_total + other_fixed_costs_total + incremental_labor_total_12w (we treat labor as part of promo cost)

  * = 3,000 + 1,500 + 288 = 4,788
* Net incremental profit = −2,570.4 (from above)
* ROI = Net incremental profit ÷ Total promo cost = (−2,570.4) ÷ 4,788 = negative

  * Compute division: 2,570.4 ÷ 4,788 ≈ 0.537 (approx) → so ROI = −0.537 → expressed as −53.7%
  * Detailed division (approx): 4,788 × 0.5 = 2,394; remainder 2,570.4 − 2,394 = 176.4; 176.4 ÷ 4,788 ≈ 0.0368; 0.5 + 0.0368 ≈ 0.5368 → 53.68% → so ROI = −53.68%
* So `ROI ≈ −53.7%` (loss relative to promo cost under these baseline assumptions)

#### Interim conclusion for Early Bird under baseline parameters:

* With these sample numbers (marketing spend $3k, other fixed costs $1.5k, 30% cannibalization), the Early Bird campaign *loses money* across the 12-week pilot. This highlights that either marketing/spend allocation is too high for the expected uplift or assumptions on elasticity / cannibalization need revising.

---

# 6. Night Owl Deal — detailed line-by-line worked example

## 6.1 Overview and modeling approach

* Offer: free chips when alcohol is purchased in the night window. The revenue uplift is assumed to come mainly from **increased alcohol transactions** (higher units of alcohol sold), not from the free chip (chip is an incremental cost, not incremental revenue). We therefore model incremental alcohol units and subtract the cost of chips fulfilled.

## 6.2 Inputs

* `base_units_week` (alcohol eligible purchases) = 500
* `alcohol_price_avg = 6.00`
* `chip_cost = 0.30` (cost to retailer per chip unit)
* `chip_retail_price = 1.00` (irrelevant to revenue because chip is free)
* `elasticity = 0.10` (10% lift)
* `incremental_labor_cost_per_unit = 0.05`
* `promo_marketing_cost_total = 2,000` (for 12 weeks; network)
* `other_fixed_costs_total = 1,500` (one-time)
* `cannibalization_pct = 20%` (we assume less cannibalization than Early Bird)

### 6.2.1 Compute sales uplift and incremental units

* sales_lift_pct = elasticity × 100%? Here elasticity is already expressed in percent lift per sample (we set elasticity = 0.10 meaning 10% lift for the promo) — to keep consistent, we treat `sales_lift_pct = 10%`
* new_units_week = base_units_week × (1 + 10/100) = 500 × 1.10 = 550

  * 500 × 1.10 = 500 + 50 = 550
* incremental_units_week = 550 − 500 = 50

### 6.2.2 Incremental revenue (alcohol revenue) weekly

* incremental_revenue_week = incremental_units_week × alcohol_price_avg

  * = 50 × 6.00 = 300.00

### 6.2.3 Incremental gross profit from alcohol (before chip cost)

We need alcohol unit cost or margin; if not given assume alcohol margin_pct = 35% (ASSUMPTION). So alcohol cost = 6.00 × (1 − 0.35) = 6.00 × 0.65 = 3.90. Then gross profit per extra alcohol unit = 6.00 − 3.90 = 2.10.

Show digits:

* alcohol_cost = 6.00 × 0.65

  * 6.00 × 0.65 = (6 × 65) ÷ 100 = 390 ÷ 100 = 3.90

* gross_profit_per_alcohol_unit = 6.00 − 3.90 = 2.10

* incremental_gross_profit_week_before_chips = incremental_units_week × gross_profit_per_alcohol_unit

  * = 50 × 2.10 = 50 × (2 + 0.1) = 50 × 2 + 50 × 0.1 = 100 + 5 = 105.00

### 6.2.4 Subtract chip cost for each incremental transaction

* chip_cost_total_week = incremental_units_week × chip_cost

  * = 50 × 0.30
  * 50 × 0.30 = 15.00

* incremental_gross_profit_week_after_chips = 105.00 − 15.00 = 90.00

### 6.2.5 Apply cannibalization

* cannibalization_pct = 20% → non_cannibalized_fraction = 0.80
* true_incremental_gross_profit_week = 90.00 × 0.80 = 72.00

### 6.2.6 Incremental labor and weekly marketing allocation

* incremental_labor_cost_week = incremental_units_week × incremental_labor_cost_per_unit

  * = 50 × 0.05 = 2.50

* promo_marketing_cost_week = promo_marketing_cost_total ÷ T_weeks = 2,000 ÷ 12

  * 2,000 ÷ 12 = 166.666... ≈ 166.67 (round to cents)

* other_fixed_costs_week = 1,500 ÷ 12 = 125.00

### 6.2.7 Net incremental profit (weekly)

* true_incremental_gross_profit_week = 72.00
* Subtract marketing 166.67 → 72.00 − 166.67 = −94.67
* Subtract labor 2.50 → −94.67 − 2.50 = −97.17
* Subtract other_fixed_costs_week 125.00 → −97.17 − 125.00 = −222.17
* So `net_incremental_profit_week = −$222.17` (loss weekly under baseline)

### 6.2.8 12-week totals

* incremental_gross_profit_total_12w_before_chips = 105 × 12 = 1,260
* chip_cost_total_12w = 15 × 12 = 180
* incremental_gross_profit_total_12w_after_chips = 1,260 − 180 = 1,080
* true_incremental_gross_profit_total_12w = 1,080 × 0.80 = 864
* incremental_labor_total_12w = 2.50 × 12 = 30.00
* promo_marketing_cost_total = 2,000
* other_fixed_costs_total = 1,500
* net_incremental_profit_total_12w = 864 − 2,000 − 30 − 1,500

  * 864 − 2,000 = −1,136
  * −1,136 − 30 = −1,166
  * −1,166 − 1,500 = −2,666
* So `net_incremental_profit_total_12w = −$2,666.00`
* Total promo costs = 2,000 + 1,500 + 30 = 3,530
* ROI = −2,666 ÷ 3,530 ≈ −0.755 → −75.5%

#### Interim conclusion for Night Owl:

* Under these sample assumptions the promo is loss-making. Achieving positive ROI would require higher uplift (elasticity), lower marketing/fixed costs, or lower cannibalization.

---

# 7. Wellness Kit — detailed line-by-line worked example

## 7.1 Inputs

* `base_units_week = 300`
* `electro_price = 2.50`
* `painkiller_price = 1.50`
* `water_price = 1.00`
* `kit_discount_pct = 10`
* `elasticity = 0.8`
* component margins: electrolyte margin 45%, painkiller margin 50%, water margin 30% (ASSUMPTION)
* `incremental_labor_cost_per_unit = 0.08`
* `promo_marketing_cost_total = 2,000`
* `other_fixed_costs_total = 1,500`
* `cannibalization_pct = 25%`

### 7.1.1 Compute component costs and full kit price

* electrolyte_cost = 2.50 × (1 − 0.45) = 2.50 × 0.55

  * 2.50 × 0.55 = (250 × 55) ÷ 10000 = easier: 2.5 × 0.55 = 1.375
* painkiller_cost = 1.50 × (1 − 0.50) = 1.50 × 0.50 = 0.75
* water_cost = 1.00 × (1 − 0.30) = 1.00 × 0.70 = 0.70
* unit_cost = 1.375 + 0.75 + 0.70

  * 1.375 + 0.75 = 2.125
  * 2.125 + 0.70 = 2.825
* full_kit_price = 2.50 + 1.50 + 1.00 = 5.00

### 7.1.2 Kit price after discount

* kit_discount_pct = 10 → discount fraction = 0.10
* kit_price = 5.00 × (1 − 0.10) = 5.00 × 0.90 = 4.50

### 7.1.3 gross_profit_per_kit

* gross_profit_per_kit = kit_price − unit_cost

  * kit_price = 4.50
  * unit_cost = 2.825
  * 4.50 − 2.825 = 1.675
  * So `gross_profit_per_kit = $1.675`

### 7.1.4 sales uplift and incremental units (weekly)

* sales_lift_pct = elasticity × discount_pct? Using A4, elasticity = 0.8 and discount_pct = 10 → sales_lift_pct = 0.8 × 10 = 8%
* new_units_week = base_units_week × (1 + 8/100) = 300 × 1.08

  * 300 × 1.08 = 300 + 24 = 324
* incremental_units_week = 324 − 300 = 24

### 7.1.5 incremental revenue and gross profit (weekly)

* incremental_revenue_week = 24 × kit_price = 24 × 4.50

  * 24 × 4.50 = 24 × (4 + 0.5) = 24 × 4 + 24 × 0.5 = 96 + 12 = 108
* incremental_gross_profit_week = 24 × 1.675

  * 1.675 × 24 = 1.675 × (20 + 4) = 1.675 × 20 + 1.675 × 4

    * 1.675 × 20 = 33.50
    * 1.675 × 4 = 6.70
    * Sum = 33.50 + 6.70 = 40.20
  * So `incremental_gross_profit_week = $40.20`

### 7.1.6 Apply cannibalization (25%)

* non_cannibalized_fraction = 1 − 0.25 = 0.75
* true_incremental_gross_profit_week = 40.20 × 0.75

  * 40.20 × 0.75 = 40.20 × (3/4) = (40.20 × 3) ÷ 4
  * 40.20 × 3 = 120.60
  * 120.60 ÷ 4 = 30.15
  * So `true_incremental_gross_profit_week = $30.15`

### 7.1.7 Weekly labor and marketing allocation

* incremental_labor_cost_week = 24 × 0.08 = 1.92
* promo_marketing_cost_week = 2,000 ÷ 12 = 166.666... ≈ 166.67
* other_fixed_costs_week = 1,500 ÷ 12 = 125.00

### 7.1.8 Net incremental profit (weekly)

* Start with true_incremental_gross_profit_week = 30.15
* Subtract marketing 166.67 → 30.15 − 166.67 = −136.52
* Subtract labor 1.92 → −136.52 − 1.92 = −138.44
* Subtract other_fixed_costs_week 125.00 → −138.44 − 125.00 = −263.44
* So `net_incremental_profit_week = −$263.44`

### 7.1.9 12-week totals

* true_incremental_gross_profit_total_12w = 30.15 × 12

  * 30.15 × 12 = (30.15 × 10) + (30.15 × 2) = 301.5 + 60.3 = 361.8
* incremental_labor_total_12w = 1.92 × 12 = 23.04
* promo_marketing_cost_total = 2,000
* other_fixed_costs_total = 1,500
* net_incremental_profit_total_12w = 361.8 − 2,000 − 23.04 − 1,500

  * 361.8 − 2,000 = −1,638.2
  * −1,638.2 − 23.04 = −1,661.24
  * −1,661.24 − 1,500 = −3,161.24
* So `net_incremental_profit_total_12w = −$3,161.24`
* Total promo costs = 2,000 + 1,500 + 23.04 = 3,523.04
* ROI = −3,161.24 ÷ 3,523.04 ≈ −0.897 → −89.7%

#### Interim conclusion for Wellness Kit:

* Baseline parameterization yields a negative ROI. The main driver is the small incremental volume against relatively fixed marketing and setup costs. To improve economics you need larger uplift, lower fixed marketing spend, or cheaper fulfillment costs.

---

# 8. Break-even analysis (example: Early Bird)

We want to compute `required_incremental_units_total_12w` (over the 12 weeks) to reach break-even i.e., Net incremental profit_total_12w = 0. Solve for incremental units per week `x` (constant week-over-week) such that net profit = 0.

Define variables for Early Bird:

* Let `x = incremental_units_week` (unknown)
* gross_profit_per_unit = $1.10 (from earlier)
* non_cannibalized_fraction = 0.70
* true_gross_per_unit = gross_profit_per_unit × 0.70 = 1.10 × 0.70

  * 1.10 × 0.70 = (1.10 × 7) ÷ 10 = 7.70 ÷ 10 = 0.77
  * So `true_gross_per_unit = $0.77` per incremental unit (after cannibalization)
* incremental_labor_cost_per_unit = 0.10
* net_contribution_per_unit = true_gross_per_unit − incremental_labor_cost_per_unit

  * = 0.77 − 0.10 = 0.67

Total campaign contribution from incremental units across 12 weeks: `contribution_total = x × net_contribution_per_unit × 12`

Total campaign costs (fixed) = `promo_marketing_cost_total + other_fixed_costs_total` = 3,000 + 1,500 = 4,500

Break-even condition:

* contribution_total = total_fixed_costs
* x × 0.67 × 12 = 4,500
* x × 8.04 = 4,500  (since 0.67 × 12 = 8.04)

  * 0.67 × 12 = 0.67 × (10 + 2) = 0.67 × 10 + 0.67 × 2 = 6.7 + 1.34 = 8.04
* x = 4,500 ÷ 8.04

  * 4,500 ÷ 8.04 ≈ 559.701... ≈ 560 units (approx) incremental units/week required
* Therefore, weekly incremental units needed ≈ 560; since baseline incremental units under sample assumptions were only 240/week, we need more than double the uplift to break even.

Digits:

* 4,500 ÷ 8.04: multiply numerator and denominator by 100 to eliminate decimal: 450,000 ÷ 804

  * 804 × 500 = 402,000; remainder 48,000
  * 804 × 50 = 40,200; remainder 7,800
  * 804 × 9 = 7,236; remainder 564
  * 804 × 0.7 ≈ 562.8
  * So total ≈ 559.7 → rounds to 560.

Break-even insight: either reduce fixed costs from 4,500 to a lower number or increase sales lift (elasticity or discount) to generate ~560 incremental units/week.

---

# 9. Sensitivity analysis (summary table concept + two scenarios)

Create a two-way sensitivity table in your spreadsheet comparing ROI across ranges of:

* Elasticity (low/medium/high) and
* Promo marketing spend (low/medium/high) or cannibalization.

Below I compute two alternative scenarios for Early Bird to show sensitivity.

## Scenario S1: Improved elasticity (elasticity = 2.0 instead of 1.2), same other inputs

* sales_lift_pct = 2.0 × 20 = 40%
* new_units_week = 1,000 × 1.40 = 1,400 → incremental_units_week = 400
* incremental_gross_profit_week = 400 × 1.10 = 440
* true_incremental_gross_profit_week = 440 × 0.70 = 308
* incremental_labor_week = 400 × 0.10 = 40
* weekly marketing = 250, other_fixed_week = 125
* net_inc_profit_week = 308 − 250 − 40 − 125 = −107
* 12-week net = −107 × 12 = −1,284
* This is still negative but much improved (net loss smaller). To reach break-even, either cut fixed costs or increase pilot size.

## Scenario S2: Reduced marketing and lower cannibalization

* Keep elasticity = 1.2 but reduce promo_marketing_cost_total to $1,000 and cannibalization to 10%
* promo_marketing_cost_week = 1,000 ÷ 12 ≈ 83.33
* non_cannibalized_fraction = 0.90
* earlier incremental_gross_profit_week = 264 (from baseline)
* true_incremental_gross_profit_week = 264 × 0.90 = 237.6
* incremental_labor_week = 24
* other_fixed_week = 125
* net_inc_profit_week = 237.6 − 83.33 − 24 − 125 = 5.27 (positive weekly)
* 12-week net = 5.27 × 12 = 63.24 → positive but small
* Total promo costs = 1,000 + 1,500 + 288 = 2,788
* ROI = 63.24 ÷ 2,788 ≈ 2.3% (small positive ROI)

Interpretation: improving cannibalization and reducing marketing dramatically improves economics. This is common: for bundles with low per-unit margin, fixed marketing costs dominate for small pilots.

---

# 10. 12-week campaign cashflow projection template (what to put into your spreadsheet)

Columns (week 1 to week 12), plus totals:

* Week
* Base units (week)
* Sales lift % (week) (assume constant or changeable week-to-week)
* New units (week)
* Incremental units (week)
* Bundle price
* Incremental revenue
* Gross profit per unit
* Incremental gross profit
* Cannibalization adjustment → true incremental gross profit
* Incremental labor cost
* Promo marketing cost allocated
* Other fixed cost allocated
* Net incremental profit (week)
* Cumulative net incremental profit (running sum)

Make sure the spreadsheet calculates totals automatically and shows ROI = Cumulative net incremental profit ÷ (Total promo marketing + Other fixed + incremental labor total).

---

# 11. KPIs and dashboards to track during pilot

* Weekly incremental units sold (by promo)
* Weekly incremental revenue and gross profit (by promo)
* Promo redemption rate (for codes or POS flags)
* Cannibalization proxy: change in non-target SKU sales in promo window
* Stockouts of promoted SKUs (units and revenue lost)
* Incremental margin per unit (realized)
* Break-even remaining units to cover remaining fixed cost

---

# 12. Practical recommendations to improve ROI (operational levers)

* Reduce fixed marketing spend per pilot by using in-store signage and App push rather than paid media.
* Increase pilot scale (more stores) so fixed costs dilute across volume. If fixed costs are large relative to per-unit margin, scale matters.
* Reduce cannibalization by offering bundles that add new value rather than discounting items that customers would buy anyway (i.e., pair complementary items rather than substitutable ones).
* Improve targeting to customers most likely to respond (loyalty members, recent night-time buyers) to raise elasticity.
* Negotiate lower COGS with vendors for pilot period for bundle SKUs.
* Shorten campaign to high-intensity bursts to test product-market fit before large spend.

---

# 13. Short concise reasoning steps I followed

* I parameterized a weekly, network-level model because promotions and pilot economics are easier to reason about week-by-week and then aggregate.
* For each promo I calculated: price after discount, incremental units from uplift, incremental revenue, gross profit (revenue minus unit cost), adjustment for cannibalization, and subtracted fixed and variable promo costs to get net incremental profit.
* I then computed ROI as net incremental profit divided by total promo cost.
* I ran break-even math to determine incremental units needed to cover fixed costs and provided sensitivity scenarios to show which levers matter most.

---

# 14. Points that require verification or are uncertain (must validate)

1. **Elasticity values** for each promotion and SKU (very sensitive). I cannot verify these; run small A/B tests or analyze historical promo lifts to estimate.
2. **Baseline volumes and per-store distribution.** I used network-level base units; verify actual baseline weekly units for the specified pilot stores.
3. **Accurate unit-level COGS and margins** for sandwiches, energy drinks, alcohol and chips, electrolytes, painkillers, water. I estimated margins; confirm with procurement/finance.
4. **Actual marketing cost allocation** and the degree to which store-level signage or app push can replace paid marketing. Confirm budgets.
5. **Cannibalization percentage** — requires historical analysis or test measurement. I used 20–30% as plausible default but it can vary widely.
6. **Operational fulfillment costs** (e.g., packaging for bundles, labor impact), shipping or supplier premiums when scaling. Validate with ops team.
7. **Regulatory or store policy constraints** (e.g., promoting alcohol in some jurisdictions) that may alter feasible promotions. Confirm with legal.
8. **Pilot store selection bias** (are pilot stores similar to chain average?). Verify representativeness.

If any of these are uncertain, run a small two-arm pilot in a controlled subset of stores (A/B with holdouts) to estimate real uplift and cannibalization before scaling.

---

# 15. Deliverables I can produce next (pick any)

* A ready-to-run Excel template with the input table, weekly projection columns, sensitivity tables, and charts (I will produce the sheet formatted as a downloadable file).
* A Power BI semantic model mapping the finance outputs to visuals (KPIs, trend, sensitivity slicers).
* A Monte Carlo simulation of ROI where elasticity, cannibalization, and marketing cost are distributional variables (to estimate probability of positive ROI).
* A step-by-step pilot measurement plan with the exact statistical test to estimate incremental revenue and cannibalization.

Tell me which of the above you want next and I will produce it.
