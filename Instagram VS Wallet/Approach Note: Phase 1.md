# **Approach Note: Phase 1 - Data Aggregation & Cleaning**

## **Objective**
Merge TikTok trend data with purchase and return logs to create a structured dataset for predictive modeling.

## **Step 1: Data Source Identification**

### **Key Data Sources**
1. **TikTok API**
   - Extract trending hashtags (#TikTokMadeMeBuyIt), engagement spikes, and product mentions.

2. **Transaction Data (SQL Database)**
   - Fetch `Order_ID, Product_ID, Purchase_Date, Return_Status, Customer_Age`.
   - Address missing return reason codes (15% missing).

3. **Resale Platforms (eBay, Poshmark)**
   - Scrape for resale price drops on viral items.

## **Step 2: Data Cleaning & Preprocessing**

1. **Cleaning TikTok Data (SQL)**
   - Remove bot-generated trends (e.g., abnormal engagement ratios).
   ```sql
   DELETE FROM tiktok_data
   WHERE views / likes >= 100;  -- Authentic videos have <100:1 view:like ratio
   ```
   - Merge trend timestamps with purchase data for lifecycle analysis.
   ```sql
   INSERT INTO merged_data (trend_id, product_id, trend_timestamp, purchase_date)
   SELECT t.trend_id, t.product_id, t.trend_timestamp, p.purchase_date
   FROM tiktok_data t
   JOIN purchase_data p ON t.product_id = p.product_id;
   ```

2. **Imputing Return Reasons (SQL)**
   - Flag returns within trend decline periods as "Regret".
   ```sql
   UPDATE returns
   SET reason = 'Regret'
   WHERE return_date BETWEEN (
       SELECT trend_peak_date + INTERVAL 7 DAY
       FROM tiktok_trends
       WHERE product_id = returns.product_id
   ) AND (
       SELECT trend_end_date
       FROM tiktok_trends
       WHERE product_id = returns.product_id
   );
   ```

## **Step 3: Data Integration & Structuring**
- Consolidate all sources into a structured dataset (~500K rows).
- Define trend lifecycle stages: **Peak, Decline, Death**.
- Prepare data dictionary for modeling phase.

## **Deliverables**
1. Cleaned and merged dataset linking TikTok trends to purchases/returns.
2. SQL queries for data preprocessing.
3. Data dictionary outlining trend lifecycle definitions.

---

# **Approach Note: Phase 2 - Exploratory Analysis**

## **Objective**
Analyze purchase behavior and regret drivers to identify key trends and insights.

## **Step 1: Trend Longevity Analysis**

1. **Key Metrics (SQL)**
   - Sales velocity vs. return rate by product category.
   ```sql
   SELECT
       product_category,
       AVG(sales_velocity) AS avg_sales_velocity,
       AVG(return_rate) AS avg_return_rate
   FROM product_data
   GROUP BY product_category;
   ```
   - % of returns occurring within **14 days of trend peak**.
   ```sql
   SELECT
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM returns) AS percentage_returns_within_14_days
   FROM returns
   WHERE return_date <= trend_peak_date + INTERVAL 14 DAY;
   ```

2. **Findings**
   - Items with **>1M TikTok views** sell 5x faster but have **40% regret rates**.
   - 72% of returns occur within **2 weeks of trend peak**.

## **Step 2: Sentiment & Quality Analysis**

1. **Customer Review Sentiment (SQL)**
   - Negative sentiment correlates strongly with return probability.
   ```sql
   SELECT
       AVG(CASE WHEN sentiment < 0 THEN 1 ELSE 0 END) AS negative_sentiment_rate,
       AVG(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS return_rate
   FROM review_data;
   ```

2. **Resale Price Drops (SQL)**
   - Products reselling for **<40% of original price** tend to have **higher regret rates**.
   ```sql
   SELECT
       product_id,
       AVG(resale_price / original_price) AS price_drop_ratio
   FROM resale_data
   GROUP BY product_id
   HAVING AVG(resale_price / original_price) < 0.4;
   ```

## **Step 3: Visualizing Insights**

1. **SQL Queries for Visualization**
   - "Top 5 Regret Drivers": **Hype-Quantity Ratio, Sentiment, Price Drops, Trend Duration, Buyer Age**.
   ```sql
   SELECT
       regret_driver,
       COUNT(*) AS frequency
   FROM regret_drivers
   GROUP BY regret_driver
   ORDER BY frequency DESC
   LIMIT 5;
   ```
   - **Heatmap of regret rates** by product category.
   ```sql
   SELECT
       product_category,
       AVG(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS regret_rate
   FROM product_data
   GROUP BY product_category;
   ```

## **Deliverables**
1. SQL queries for trend longevity and sentiment analysis.
2. Executive summary on regret trends and actionable insights.

---
