# **Approach Note: Phase 1 - Data Aggregation & Cleaning**

## **Objective**
To integrate and clean TikTok trend data with purchase and return logs, creating a structured dataset for predictive modeling.

## **Key Challenges & Considerations**
1. **Data Silos**: Trend data (TikTok API), transaction data (SQL), and resale data (scraping) exist in separate sources.
2. **Data Quality**: Missing return reasons (~15%) and inconsistent timestamps need imputation.
3. **Trend Alignment**: Purchases must be mapped to trend lifecycles (Peak, Decline, Death).

---

## **Approach**

### **Step 1: Extract & Preprocess Data**

#### **1.1 TikTok Trend Data (API Extraction)**
- Pull engagement metrics for viral products using TikTok API:
  - Hashtags: `#TikTokMadeMeBuyIt`, `#TrendingNow`
  - Engagement: `views`, `likes`, `shares`, `comments`
  - Video metadata: `upload_date`, `product_mentions`
- **Cleaning:**
  - Remove bot-driven anomalies using engagement ratio (`views/likes < 100`).
  ```sql
  DELETE FROM tiktok_data
  WHERE views / likes >= 100;
  ```
  - Normalize timestamps to match purchase records.

#### **1.2 Transaction Data (SQL Extraction)**
- Query purchase logs with key attributes:
  ```sql
  SELECT Order_ID, Product_ID, Purchase_Date, Return_Status, Customer_Age
  FROM transactions;
  ```
- **Cleaning:**
  - Standardize date formats.
  - Handle missing return reasons by inferring from trend lifecycles.

#### **1.3 Resale Data (Web Scraping)**
- Scrape eBay/Poshmark for resale pricing trends.
- **Key Variables:** Product_ID, Resale_Price, Days_Since_Trend_Peak.
- **Cleaning:** Convert price variations into % drop relative to original price.
  ```sql
  UPDATE resale_data
  SET price_drop_percent = ((original_price - resale_price) / original_price) * 100;
  ```

---

### **Step 2: Data Merging & Feature Engineering**

#### **2.1 Merging TikTok & Transaction Data**
- Join trend data with purchase logs using `trend_date ≈ purchase_date`:
  ```sql
  INSERT INTO merged_data (trend_id, product_id, trend_date, purchase_date)
  SELECT t.trend_id, t.product_id, t.trend_date, p.purchase_date
  FROM tiktok_data t
  JOIN purchase_data p ON t.trend_date = p.purchase_date;
  ```
- Create **Trend Lifecycle Stages**:
  - **Peak**: Max engagement date
  - **Decline**: Engagement drop >50%
  - **Death**: <5% of peak engagement

#### **2.2 Impute Return Reasons (SQL Update)**
- Assign missing return reasons based on trend stage:
  ```sql
  UPDATE returns
  SET reason = 'Regret'
  WHERE return_date BETWEEN (
      SELECT trend_peak_date + INTERVAL 7 DAY FROM tiktok_trends
      WHERE product_id = returns.product_id
  ) AND (
      SELECT trend_end_date FROM tiktok_trends
      WHERE product_id = returns.product_id
  );
  ```

#### **2.3 Feature Engineering**
- **Days Since Trend Peak**: Time gap between purchase and peak.
  ```sql
  UPDATE merged_data
  SET days_since_trend_peak = DATEDIFF(purchase_date, trend_peak_date);
  ```
- **Engagement Decay Rate**: Speed of trend decline.
  ```sql
  UPDATE tiktok_trends
  SET engagement_decay_rate = (peak_engagement - current_engagement) / DATEDIFF(current_date, peak_date);
  ```
- **Resale Price Drop %**: Indicator of regret likelihood.
  ```sql
  UPDATE resale_data
  SET price_drop_percent = ((original_price - resale_price) / original_price) * 100;
  ```

---

## **Deliverables**
- **Final Dataset** (500K+ rows): Integrated purchase, return, and trend data.
- **Data Dictionary**: Trend lifecycle definitions, engineered features.
- **SQL Scripts**: Extraction, cleaning, and merging processes.

---

## **Next Steps**
Proceed to **Phase 2: Exploratory Analysis** to identify key regret drivers.
