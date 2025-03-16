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

---

### **Step 2: Data Merging & Feature Engineering**
#### **2.1 Merging TikTok & Transaction Data**
- Join trend data with purchase logs using `trend_date ≈ purchase_date`:
  ```python
  merged_data = pd.merge(trends, purchases, left_on='trend_date', right_on='purchase_date')
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
- **Engagement Decay Rate**: Speed of trend decline.
- **Resale Price Drop %**: Indicator of regret likelihood.

---

## **Deliverables**
- **Final Dataset** (500K+ rows): Integrated purchase, return, and trend data.
- **Data Dictionary**: Trend lifecycle definitions, engineered features.
- **SQL & Python Scripts**: Extraction, cleaning, and merging processes.

---

## **Next Steps**
Proceed to **Phase 2: Exploratory Analysis** to identify key regret drivers.

