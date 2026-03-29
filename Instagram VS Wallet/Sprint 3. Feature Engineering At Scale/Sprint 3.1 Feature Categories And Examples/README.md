## Sprint 3.1

**Instagram vs Wallet**
**Feature Categories and Examples**

---

### 1. Objective

Build the feature system that converts raw exposure, purchase, product, and return data into model-ready signals.

This sprint is not about model choice.
It is about feature architecture.

If the features are weak, the model will just become a sophisticated rumor machine.

---

### 2. Design Principle

Every feature must answer one of four questions:

* **What did the user see?**
* **What state were they in when they bought?**
* **What kind of product was it?**
* **What happened after the purchase?**

Anything outside that chain is noise.

---

### 3. Feature Architecture Overview

The feature set is organized into six blocks:

1. **Trend Exposure Features**
2. **Purchase Context Features**
3. **Customer Behavior Features**
4. **Product Risk Features**
5. **Text and Sentiment Features**
6. **Behavioral Interaction Features**

Each block captures a different slice of regret formation.

---

### 4. Trend Exposure Features

These features describe the pressure field around the purchase.

| Feature                     | Meaning                                           | Why It Matters                                  |
| --------------------------- | ------------------------------------------------- | ----------------------------------------------- |
| `trend_velocity_24h`        | Engagement growth in the 24 hours before purchase | Fast spikes often trigger impulse buying        |
| `trend_half_life_hours`     | How quickly the trend decays                      | Short half-life trends are hype-heavy           |
| `trend_peak_distance_hours` | Hours from trend peak to purchase                 | Closer purchases may reflect stronger influence |
| `exposure_count_12h`        | Number of exposures in prior 12 hours             | Repetition can amplify desire                   |
| `creator_reach`             | Size of creator audience                          | Wider reach can increase purchase pressure      |
| `comment_sentiment_score`   | Average sentiment in comments                     | Positive hype often inflates expectations       |

#### What this block is trying to capture

Not popularity.
Pressure. Momentum. Hype density.

#### Useful derived patterns

* High velocity + short half-life
* Repeated exposure in a short window
* Trend peak very near purchase time

---

### 5. Purchase Context Features

These describe the moment the wallet opened.

| Feature                    | Meaning                          | Why It Matters                                    |
| -------------------------- | -------------------------------- | ------------------------------------------------- |
| `discount_pct`             | Percent discount applied         | Deep discounts can reduce deliberation            |
| `time_of_day_bucket`       | Purchase hour grouped into bands | Late-night purchases are often less reflective    |
| `day_type`                 | Weekday or weekend               | Weekends often carry more impulse behavior        |
| `session_duration_seconds` | Time spent before purchase       | Short sessions often signal weaker evaluation     |
| `device_type`              | Mobile, desktop, app             | Mobile often means faster, less deliberate buying |
| `channel_source`           | Instagram, direct, search, other | Exposure channel matters for attribution          |

#### What this block is trying to capture

Decision speed and decision quality.

A fast decision is not automatically bad.
But fast plus discounted plus trend-driven is where regret usually starts to crawl out of the walls.

---

### 6. Customer Behavior Features

These features encode the buyer’s historical relationship with regret.

| Feature                        | Meaning                             | Why It Matters                                    |
| ------------------------------ | ----------------------------------- | ------------------------------------------------- |
| `prior_return_rate_90d`        | Return frequency in prior 90 days   | Strong proxy for regret-prone behavior            |
| `purchase_frequency_30d`       | Number of purchases in last 30 days | High activity can reflect impulse cycles          |
| `avg_order_value_90d`          | Average spend in prior 90 days      | Helps segment buyer type                          |
| `recency_days`                 | Days since last purchase            | Recent buyers may behave differently              |
| `historical_discount_affinity` | Tendency to buy discounted items    | Discount-sensitive buyers may be more impulsive   |
| `impulse_score`                | Derived behavioral risk index       | Compresses multiple weak signals into one feature |

#### What this block is trying to capture

Not who is “bad.”
Who is structurally more vulnerable to post-purchase reversal.

---

### 7. Product Risk Features

These separate bad product experiences from bad decisions.

| Feature                  | Meaning                                   | Why It Matters                                  |
| ------------------------ | ----------------------------------------- | ----------------------------------------------- |
| `category`               | Product category                          | Some categories are naturally more regret-prone |
| `price_band`             | Low, mid, premium                         | Price changes the emotional threshold           |
| `size_fit_issue_rate`    | Historical fit-related return rate        | Crucial for apparel                             |
| `baseline_return_rate`   | Historical return rate for SKU            | High-return items may be intrinsically unstable |
| `trend_sensitivity`      | How often item trends before return       | Some products are trend magnets                 |
| `quality_complaint_rate` | Historical quality-related complaint rate | Helps separate regret from product failure      |

#### What this block is trying to capture

The product’s own volatility.
Sometimes the item is the trapdoor, not the customer.

---

### 8. Text and Sentiment Features

These features translate human language into regret signals.

| Feature                   | Meaning                              | Why It Matters                                     |
| ------------------------- | ------------------------------------ | -------------------------------------------------- |
| `comment_sentiment_score` | Sentiment in pre-purchase comments   | Helps estimate expectation formation               |
| `return_reason_text_flag` | Binary flag from return language     | Captures regret expressions                        |
| `mismatch_term_count`     | Count of expectation mismatch words  | Strong regret indicator                            |
| `impulse_term_count`      | Count of impulse-related words       | Reveals post-purchase reversal                     |
| `fit_issue_term_count`    | Count of fit-related terms           | Often linked to regret, sometimes defect           |
| `surprise_index`          | Frequency of unexpectedness language | Measures shock gap between expectation and reality |

#### What this block is trying to capture

The story behind the return.

Numbers tell you the item came back.
Language tells you the purchase betrayed a mental model.

---

### 9. Behavioral Interaction Features

This is where the signal starts to bite.

| Feature                    | Formula Idea                                     | Why It Matters                                       |
| -------------------------- | ------------------------------------------------ | ---------------------------------------------------- |
| `velocity_x_discount`      | `trend_velocity_24h * discount_pct`              | High hype plus deep discount often multiplies regret |
| `velocity_x_prior_return`  | `trend_velocity_24h * prior_return_rate_90d`     | Detects vulnerable customers under hype pressure     |
| `time_x_mobile`            | `late_night_flag * mobile_flag`                  | Fast mobile purchases are often less reflective      |
| `category_x_fit_risk`      | `category * size_fit_issue_rate`                 | Identifies structurally risky product areas          |
| `sentiment_gap`            | Pre-purchase hype minus post-purchase negativity | Direct regret proxy                                  |
| `exposure_x_session_speed` | `exposure_count_12h / session_duration_seconds`  | Measures whether exposure compressed the decision    |

#### Why interactions matter

Regret rarely comes from one clean factor.
It usually emerges when multiple weak forces collide and produce a stupidly expensive decision.

---

### 10. Feature Families by Use Case

#### A. Detection Features

Used to identify likely regret cases.

* `trend_velocity_24h`
* `discount_pct`
* `prior_return_rate_90d`
* `mismatch_term_count`

#### B. Explanation Features

Used to explain why the model flagged a case.

* `velocity_x_discount`
* `surprise_index`
* `size_fit_issue_rate`

#### C. Intervention Features

Used to decide what action to take.

* `time_of_day_bucket`
* `device_type`
* `category`
* `historical_discount_affinity`

#### D. Segmentation Features

Used to cluster customers and products.

* `purchase_frequency_30d`
* `avg_order_value_90d`
* `baseline_return_rate`

---

### 11. Feature Selection Rules

A feature survives only if it meets at least one of these tests:

* It is available **before the purchase**
* It is stable enough to reproduce
* It improves prediction or explanation
* It maps to a real intervention lever

If none of those are true, it is decorative clutter.

---

### 12. What to Avoid

Do not include features that:

* Use return information before the purchase
* Leak future trend data
* Duplicate the same signal in six disguises
* Are so sparse they become statistical ghosts
* Look clever but cannot be acted on

A feature that cannot influence a decision is often just a vanity metric in a trench coat.

---

### 13. Recommended Feature Schema Shape

The final dataset should be organized into columns like this:

* **Identifiers**

  * `order_id`
  * `customer_id`
  * `product_id`
* **Trend signals**

  * `trend_velocity_24h`
  * `trend_half_life_hours`
* **Transaction signals**

  * `discount_pct`
  * `session_duration_seconds`
* **Customer signals**

  * `prior_return_rate_90d`
  * `impulse_score`
* **Product signals**

  * `category`
  * `size_fit_issue_rate`
* **Text signals**

  * `surprise_index`
  * `mismatch_term_count`
* **Interactions**

  * `velocity_x_discount`
  * `velocity_x_prior_return`
* **Labels**

  * `regret_flag`
  * `return_type`

---

### 14. Definition of Done

This sprint is done when:

* Feature categories are clearly defined
* Each feature is tied to a business or behavioral meaning
* Leakage risk is eliminated
* Interaction features are identified
* The schema is ready for implementation

---

### 15. What This Unlocks

Once this feature map exists, the project can move into:

* actual feature engineering
* model training
* interpretability
* intervention design

The feature layer is where behavior becomes computable.
Without it, the model is just staring at the wall and calling it insight.
