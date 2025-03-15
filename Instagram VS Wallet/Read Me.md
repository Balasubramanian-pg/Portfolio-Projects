
---

# **Hyper-Realistic Case Study: TikTok Purchase Regret Predictor**  
**Tools**: Python, SQL, Power BI, Google Cloud | **Duration**: 12-week Internship  
**Business Context**: *TrendBuy Inc.*, a fast-fashion retailer, sees 30% returns on TikTok-driven purchases ($10M/year loss). Viral products like "TikTok Leggings" and "Viral Blushes" spike sales but lead to buyer remorse. Their goals:  
1. Predict regret likelihood for TikTok-influenced purchases with 85% accuracy.  
2. Reduce return rates by 25% in 6 months.  
3. Build a consumer app to nudge smarter purchases.  

---

## **Problem Statement**  
*TrendBuy* struggles with impulsive buyers who return items after trends fade. Manual trend tracking and generic reviews fail to address regret drivers like poor quality or "trend fatigue."  

---

## **Your Role as an Intern**  
Analyze TikTok trends, purchase behavior, and regret signals to build a predictive model and intervention engine.  

---

### **Phase 1: Data Aggregation & Cleaning**  
**Objective**: Merge TikTok trend data with purchase/return logs.  

#### **Data Sources**  
1. **TikTok API**:  
   - Trending hashtags (#TikTokMadeMeBuyIt), product videos, engagement spikes.  
2. **Transaction Data** (SQL):  
   - `Order_ID, Product_ID, Purchase_Date, Return_Status, Customer_Age`.  
   - Issues: 15% of returns lack reason codes.  
3. **Resale Platforms**:  
   - Scrape eBay/Poshmark for price drops on viral items (e.g., $50 leggings resold for $15).  

#### **Tasks**  
1. **Clean TikTok Data** (Python):  
   ```python  
   def detect_fake_trends(df):  
       # Filter out bots using engagement patterns  
       df = df[df['views'] / df['likes'] < 100]  # Authentic videos have <100:1 view:like ratio  
       return df  

   # Merge trend dates with purchase dates  
   merged_data = pd.merge(trends, purchases, left_on='trend_date', right_on='purchase_date')  
   ```  

2. **Impute Return Reasons** (SQL):  
   ```sql  
   -- Label returns during trend decline as "regret"  
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

**Deliverable**:  
- Dataset linking TikTok trends to purchases/returns (500K+ rows).  
- Data dictionary: Trend lifecycle stages (Peak, Decline, Death).  

---

### **Phase 2: Exploratory Analysis**  
**Objective**: Identify regret drivers like quality issues or trend decay.  

#### **Key Insights**  
1. **Trend Longevity** (Power BI):  
   - Products with >1M TikTok views sell 5x faster but have 40% regret rates.  
   - 72% of returns occur within 14 days of a trend’s peak.  
2. **Quality vs. Hype** (Python):  
   ```python  
   # Sentiment analysis of reviews  
   from textblob import TextBlob  
   df['sentiment'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)  
   regret_correlation = df[['sentiment', 'returned']].corr()  # Output: -0.65  
   ```  

**Deliverable**:  
- Power BI report: "Top 5 Regret Drivers: Hype-Quantity Ratio, Price Drops, Negative Reviews."  

---

### **Phase 3: Predictive Modeling**  
**Objective**: Flag high-regret-risk purchases in real time.  

#### **Model Development**  
1. **Algorithm**: XGBoost (handles imbalanced data).  
2. **Features**:  
   - `Days_Since_Trend_Peak`, `Resale_Price_Drop`, `Sentiment_Score`, `Customer_Age`.  
3. **Validation**:  
   - AUC-ROC: 0.88 | Precision: 82% | Recall: 79%.  

#### **Code Snippet** (Python):  
```python  
from xgboost import XGBClassifier  
import joblib  

# Train model  
model = XGBClassifier(scale_pos_weight=3)  # 25% regret class  
model.fit(X_train, y_train)  

# Save for real-time scoring  
joblib.dump(model, 'regret_model.pkl')  

# Predict for a viral hair tool  
sample = [[7, 0.65, -0.4, 19]]  # 7 days post-peak, 65% resale drop, negative reviews, teen buyer  
risk = model.predict_proba(sample)[0][1]  # Output: 91% regret risk  
```  

**Challenge**: Model initially flagged luxury buyers as low-risk but missed their high regret rates (fixed by adding income estimates via ZIP code).  

---

### **Phase 4: Intervention Engine**  
**Objective**: Reduce regret via real-time nudges and offers.  

#### **Strategies**  
1. **Pre-Purchase Pop-up**:  
   - "Trend Alert: 68% buyers keep this >6 months. Still want it?"  
2. **Post-Purchase Offer**:  
   - "Keep this jacket 30 days, get $10 credit!"  
3. **Resale Integration**:  
   - Auto-list returns on Poshmark if regret risk >70%.  

#### **SQL Automation**:  
```sql  
-- Nightly batch of high-risk customers  
INSERT INTO interventions (customer_id, intervention_type)  
SELECT customer_id,  
    CASE  
        WHEN regret_risk >= 0.8 THEN 'Email + $15 Offer'  
        WHEN regret_risk >= 0.6 THEN 'SMS Reminder'  
    END  
FROM predictions  
WHERE created_at = CURDATE() - INTERVAL 2 DAY;  # 48-hour post-purchase window  
```  

---

### **Phase 5: Consumer App & Dashboard**  
**Objective**: Empower users and managers to act.  

#### **Consumer App Features**  
1. **Trend Lifespan Tracker**:  
   - "This dress trended for 18 days. 60% of buyers kept it."  
2. **Personalized Nudges**:  
   - "You’re buying 3 trending items. 2 have 50%+ regret rates. Proceed?"  

#### **Power BI Dashboard**  
- **Manager View**:  
  - Real-time regret risk by product category.  
  - ROI of interventions: SMS nudges cut returns by 18%.  
- **Supply Chain Alerts**:  
  - "Cancel reorder: #TikTokSweaters regret risk spiked to 88%."  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Return Rate          | 30%     | 22.5% (-25%)      |  
| Customer Satisfaction| 3.2/5   | 4.1/5 (+28%)      |  
| Resale Recovery      | $0      | $2.1M             |  

---

## **Real-World Challenges**  
1. **Ethical Dilemmas**:  
   - Pop-ups annoyed 12% of customers (fixed with opt-out toggle).  
2. **Data Bias**:  
   - Gen Z buyers underrepresented in surveys (added TikTok poll integration).  
3. **Legal Hurdles**:  
   - GDPR compliance for real-time data (implemented anonymization pipeline).  

---

## **Deliverables**  
1. **Technical**:  
   - Python scripts for trend scraping and model training.  
   - SQL pipelines for intervention triggers.  
2. **Business**:  
   - Power BI dashboard with regret risk analytics.  
   - Prototype of "TrendGuard" consumer app (Figma).  

---

## **Executive Summary**  
*By treating TikTok trends as perishable inventory, TrendBuy turned a $10M problem into a $2.1M recovery engine. The intern’s work proves that in the age of virality, data isn’t just king—it’s the antidote to regret.*  

---

This case study mirrors the chaos of social media-driven retail, challenging the intern to balance hype with hard data—and turn buyer remorse into actionable insights.
