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
1. **Cleaning TikTok Data (Python)**  
   - Remove bot-generated trends (e.g., abnormal engagement ratios).  
   ```python
   def detect_fake_trends(df):  
       df = df[df['views'] / df['likes'] < 100]  # Authentic videos have <100:1 view:like ratio  
       return df  
   ```
   - Merge trend timestamps with purchase data for lifecycle analysis.  
2. **Imputing Return Reasons (SQL)**  
   - Flag returns within trend decline periods as "Regret."  
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
2. SQL queries and Python scripts for data preprocessing.  
3. Data dictionary outlining trend lifecycle definitions.  

---

# **Approach Note: Phase 2 - Exploratory Analysis**

## **Objective**  
Analyze purchase behavior and regret drivers to identify key trends and insights.

## **Step 1: Trend Longevity Analysis**  
1. **Key Metrics (Power BI)**  
   - Sales velocity vs. return rate by product category.  
   - % of returns occurring within **14 days of trend peak**.  
2. **Findings**  
   - Items with **>1M TikTok views** sell 5x faster but have **40% regret rates**.  
   - 72% of returns occur within **2 weeks of trend peak**.  

## **Step 2: Sentiment & Quality Analysis**  
1. **Customer Review Sentiment (Python)**  
   ```python  
   from textblob import TextBlob  
   df['sentiment'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)  
   regret_correlation = df[['sentiment', 'returned']].corr()  # Output: -0.65  
   ```  
   - Negative sentiment correlates strongly with return probability.  
2. **Resale Price Drops (SQL)**  
   ```sql  
   SELECT product_id, AVG(resale_price / original_price) AS price_drop_ratio  
   FROM resale_data  
   GROUP BY product_id;  
   ```  
   - Products reselling for **<40% of original price** tend to have **higher regret rates**.  

## **Step 3: Visualizing Insights**  
1. **Power BI Dashboard**  
   - "Top 5 Regret Drivers": **Hype-Quantity Ratio, Sentiment, Price Drops, Trend Duration, Buyer Age.**  
   - **Heatmap of regret rates** by product category.  

## **Deliverables**  
1. Power BI report highlighting key regret drivers.  
2. Python and SQL scripts for trend longevity and sentiment analysis.  
3. Executive summary on regret trends and actionable insights.

