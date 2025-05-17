
---

# Customer Churn Prediction and Retention System
**Tools**: Python, SQL, Power BI, Excel | **Duration**: 8-week Internship  
**Business Context**: *ConnectTel Telecom*, a $500M revenue company, faces a 25% annual churn rate, costing $45M/year. They need to:  
1. **Predict churn risk** with 90% accuracy using CRM and usage data.  
2. **Reduce churn by 20%** in 6 months via automated retention campaigns.  
3. **Increase CLTV (Customer Lifetime Value)** by 15% through personalized offers.  

---

## **Problem Statement**  
*ConnectTel*’s reactive approach (e.g., retention offers after cancellation requests) fails to address early warning signs. Manual processes miss 40% of at-risk customers.  

---

## **Your Role as an Intern**  
Analyze customer behavior, build predictive models, and design a retention engine.  

---

### **Phase 1: Data Aggregation & Cleaning**  
**Objective**: Merge fragmented CRM, billing, and support data.  

#### **Data Sources**  
1. **CRM Data** (SQL):  
   - `Customer_ID, Plan_Type, Tenure, Monthly_Charges, Upgrade_History`.  
   - Issues: 15% missing `Upgrade_History`; conflicting tenure values.  
2. **Usage Logs** (CSV, 2M+ rows):  
   - `Customer_ID, Data_Usage, Call_Duration, Outage_Count`.  
3. **Support Tickets** (JSON):  
   - Sentiment scores from NLP analysis of ticket text (e.g., "frustrated" = high risk).  

#### **Tasks**  
1. **Clean CRM Data** (SQL):  
   ```sql  
   -- Fix tenure inconsistencies (e.g., negative values)  
   UPDATE customers  
   SET Tenure = CASE  
       WHEN Tenure < 0 THEN ABS(Tenure)  
       ELSE Tenure  
   END  
   WHERE Tenure IS NOT NULL;  
   ```  

2. **Merge Datasets** (Python):  
   ```python  
   import pandas as pd  

   # Merge usage and support data on Customer_ID  
   merged_data = pd.merge(usage, support, on='Customer_ID', how='left')  
   merged_data['Sentiment_Score'] = merged_data['Sentiment_Score'].fillna(0)  # Assume no tickets = neutral  
   ```  

**Deliverable**:  
- Cleaned dataset with 95% completeness.  
- Data dictionary mapping sentiment scores to risk levels.  

---

### **Phase 2: Exploratory Analysis**  
**Objective**: Identify churn drivers like outage frequency or price hikes.  

#### **Key Insights**  
1. **Churn Triggers** (Power BI):  
   - 62% of churners experienced >3 outages/month.  
   - Customers on legacy plans (no upgrades in 12 months) churn 3x faster.  
2. **Sentiment Impact** (Python):  
   ```python  
   # Correlation matrix: Sentiment vs. Churn  
   print(merged_data[['Sentiment_Score', 'Churned']].corr())  
   # Output: -0.71 (strong negative correlation)  
   ```  

#### **Deliverable**:  
- Power BI report: "Top 5 Churn Drivers: Outages, Plan Age, Sentiment, Usage Drops, Billing Complaints."  

---

### **Phase 3: Predictive Modeling**  
**Objective**: Build a model to flag at-risk customers 30 days pre-churn.  

#### **Model Development**  
1. **Algorithm**: XGBoost (handles imbalanced data with scale_pos_weight).  
2. **Features**:  
   - `Outage_Count`, `Sentiment_Score`, `Percent_Usage_Drop`, `Months_Since_Upgrade`.  
3. **Validation**:  
   - AUC-ROC: 0.92 | Precision: 88% | Recall: 85%.  

#### **Code Snippet** (Python):  
```python  
from xgboost import XGBClassifier  
from sklearn.model_selection import train_test_split  

# Handle class imbalance (20% churners)  
model = XGBClassifier(scale_pos_weight=4)  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  
model.fit(X_train, y_train)  

# Predict risk for a high-value customer  
high_value_customer = [[3, -0.8, 45, 18]]  # 3 outages, negative sentiment, 45% usage drop, 18mo no upgrade  
risk = model.predict_proba(high_value_customer)[0][1]  # Output: 94% risk  
```  

**Challenge**: Model initially flagged 60% false positives (fixed by adjusting classification thresholds).  

---

### **Phase 4: Retention Automation**  
**Objective**: Trigger personalized campaigns for at-risk customers.  

#### **Workflows**  
1. **Tier 1 (Risk > 80%)**:  
   - Offer free month + plan upgrade.  
2. **Tier 2 (Risk 50-80%)**:  
   - Send loyalty discount (15% off next bill).  
3. **Tier 3 (Risk 30-50%)**:  
   - Proactive support call.  

#### **SQL Automation**:  
```sql  
-- Flag high-risk customers nightly  
INSERT INTO retention_campaigns (Customer_ID, Campaign)  
SELECT Customer_ID,  
    CASE  
        WHEN Churn_Risk >= 0.8 THEN 'Tier 1 Offer'  
        WHEN Churn_Risk >= 0.5 THEN 'Tier 2 Offer'  
        ELSE NULL  
    END  
FROM churn_predictions  
WHERE Campaign IS NULL;  
```  

---

### **Phase 5: Dashboard & Playbook**  
**Objective**: Empower managers to monitor and refine strategies.  

#### **Power BI Dashboard**  
- **Home Tab**:  
  - Real-time churn risk distribution.  
  - Campaign performance (e.g., Tier 1 acceptance rate: 68%).  
- **Drill-Down**:  
  - Customer profiles: "Customer 8921: 92% risk – 4 outages, 2 angry tickets."  

#### **Playbook Components**  
1. **Escalation Protocols**: When to escalate to human agents.  
2. **Offer Expiry Rules**: Auto-retire stale discounts.  
3. **A/B Test Results**: "Free month" beats "20% off" by 22% acceptance.  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Monthly Churn Rate   | 4.1%    | 3.3% (-19.5%)     |  
| Retention ROI        | N/A     | $8.2M saved       |  
| CLTV                 | $1,200  | $1,380 (+15%)     |  

---

## **Real-World Challenges**  
1. **Data Privacy**: Masked `Customer_ID` in dashboards to comply with CCPA.  
2. **Channel Overload**: SMS offers annoyed customers (fixed with opt-in rules).  
3. **Model Decay**: Accuracy dropped 12% in 3 months (retrained biweekly).  

---

## **Deliverables**  
1. **Technical**:  
   - Python scripts for model training and sentiment analysis.  
   - SQL automation scripts for campaign triggers.  
2. **Business**:  
   - Power BI dashboard with customer risk profiles.  
   - Excel playbook: "10 Retention Campaigns with ROI."  

---

## **Executive Summary**  
*By treating churn as a preventable event, not an inevitability, ConnectTel turned a $45M leak into a $8.2M plug. The intern’s work showcases how predictive analytics and empathy-driven automation can transform customer retention.*  

---

This case study immerses the intern in real-world chaos—data messiness, stakeholder politics, and balancing automation with human touch—to deliver measurable business impact.
