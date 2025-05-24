
# Customer Churn Prediction & Prevention: A Multi-Phase Case Study

This document outlines a comprehensive, multi-phase project aimed at predicting customer churn, identifying its key drivers, and implementing proactive strategies to improve customer retention and business outcomes.

---

## **Phase 1: Data Aggregation & Cleaning**

#### **Objective**
To integrate and clean fragmented customer data from multiple sources (CRM, billing, usage logs, and support tickets) to create a high-quality dataset for churn prediction.

#### **Key Challenges & Considerations**
1.  **Data Completeness** – Missing values in `Upgrade_History` (15%) and inconsistent tenure data.
2.  **Data Volume & Performance** – Handling 2M+ rows of usage logs efficiently.
3.  **Data Standardization** – Merging SQL, CSV, and JSON formats into a unified structure.

---

### **Step 1: Extract & Load Data**
-   **SQL Query for CRM Data Extraction**
    ```sql
    SELECT Customer_ID, Plan_Type, Tenure, Monthly_Charges, Upgrade_History
    FROM customers;
    ```
-   **Load CSV (Usage Logs) & JSON (Support Tickets) into Pandas**
    ```python
    import pandas as pd
    usage = pd.read_csv("usage_logs.csv")
    support = pd.read_json("support_tickets.json")
    # Assuming 'crm_data' is loaded from SQL into a DataFrame named 'crm'
    # crm = pd.read_sql_query("SELECT ... FROM customers;", connection)
    ```

---

### **Step 2: Data Cleaning & Transformation**
-   **Fix Tenure Inconsistencies** (Negative Values)
    ```sql
    UPDATE customers
    SET Tenure = ABS(Tenure)
    WHERE Tenure < 0;
    ```
-   **Handle Missing Values**
    ```python
    # Assuming 'merged_data' is the result of preliminary merges
    # For Upgrade_History in CRM data before merging:
    # crm['Upgrade_History'].fillna("No Upgrade", inplace=True)
    # For Sentiment_Score after sentiment mapping and merge:
    # merged_data['Upgrade_History'].fillna("No Upgrade", inplace=True) # If Upgrade_History comes from CRM
    # merged_data['Sentiment_Score'].fillna(0, inplace=True)  # Assume neutral sentiment if no ticket
    ```
-   **Convert Sentiment Text to Numerical Scores**
    ```python
    sentiment_mapping = {'frustrated': -1, 'neutral': 0, 'satisfied': 1}
    support['Sentiment_Score'] = support['Sentiment_Text'].map(sentiment_mapping)
    ```

---

### **Step 3: Data Integration & Quality Check**
-   **Merge Datasets on `Customer_ID`**
    ```python
    # Assuming 'crm' DataFrame is already loaded and cleaned
    # First, merge usage and support
    merged_data_temp = usage.merge(support, on="Customer_ID", how="left")
    # Then, merge with crm data
    final_data = merged_data_temp.merge(crm, on="Customer_ID", how="left")

    # Example handling of missing values post-merge
    final_data['Upgrade_History'].fillna("No Upgrade", inplace=True)
    final_data['Sentiment_Score'].fillna(0, inplace=True)  # Assume neutral sentiment if no ticket
    ```
-   **Validate Data Completeness**
    ```python
    missing_values_percentage = final_data.isnull().sum() * 100 / len(final_data)
    print(missing_values_percentage)  # Ensure completeness >95%
    ```

---

### **Deliverables (Phase 1)**
1.  **Cleaned Dataset** – Ensuring >95% data completeness.
2.  **Data Dictionary** – Mapping sentiment scores to risk levels.
3.  **Quality Report** – Summary of missing values handled, transformations applied, and integration status.

This structured approach ensures reliable input data for predictive modeling in Phase 2.

---
---

## **Phase 2: Exploratory Data Analysis (EDA)**
**Objective**: Identify key churn drivers and customer risk patterns.

*(Note: `merged_data` from Phase 1 is referred to as `final_data` here, or simply `merged_data` if assuming it's the output of Phase 1)*

### **1. Data Profiling**
Before diving into insights, an initial check on data quality:
-   **Missing values**:
    ```python
    # Assuming 'merged_data' is the dataset from Phase 1
    print(merged_data.isnull().sum())
    ```
    -   *Fix*: Imputed missing values using median for numeric fields and "Unknown" for categorical ones. (Specific imputation details would depend on the column).
    ```python
    # Example imputation
    # for col in merged_data.select_dtypes(include=np.number).columns:
    #     merged_data[col].fillna(merged_data[col].median(), inplace=True)
    # for col in merged_data.select_dtypes(include='object').columns:
    #     merged_data[col].fillna("Unknown", inplace=True)
    ```

-   **Outliers detection**:
    ```python
    import seaborn as sns
    import matplotlib.pyplot as plt # Ensure plt is imported for show()
    sns.boxplot(x=merged_data['Monthly_Charges'])
    plt.show() # Add this to display the plot
    ```
    -   *Fix*: Winsorized extreme values (>99th percentile).
    ```python
    # Example Winsorization
    # from scipy.stats.mstats import winsorize
    # merged_data['Monthly_Charges'] = winsorize(merged_data['Monthly_Charges'], limits=[0.0, 0.01])
    ```

---

### **2. Churn Triggers Analysis**
#### **A. Outage Frequency & Churn**
**Hypothesis**: Customers with frequent network outages are more likely to leave.

-   **Finding**:
    -   62% of churners experienced **>3 outages/month**.
    -   Non-churners averaged **0.8 outages/month**.

-   **Power BI Visualization**:
    -   A **heatmap** of churn risk vs. outage count.

-   **SQL Query to Extract Insights** (Assuming `merged_data` is in a SQL table):
    ```sql
    SELECT Outage_Count, COUNT(*) AS Customer_Count,
           SUM(CASE WHEN Churned = 1 THEN 1 ELSE 0 END) AS Churners
    FROM merged_data -- or the relevant table name
    GROUP BY Outage_Count
    ORDER BY Outage_Count DESC;
    ```

---

#### **B. Plan Age & Churn**
**Hypothesis**: Customers on older plans with no upgrades are likelier to churn.

-   **Finding**:
    -   Customers **without upgrades in 12+ months** churn **3x faster**.
    -   Legacy plan users had an **18% higher churn rate**.

-   **Python Correlation Check**:
    ```python
    # Assuming 'Churned' is a binary column (0 or 1) and 'Months_Since_Upgrade' exists
    print(merged_data[['Months_Since_Upgrade', 'Churned']].corr())
    ```
    -   Correlation: **0.63 (positive)** → Strong link between outdated plans and churn.

-   **Power BI Visualization**:
    -   A **line chart** showing churn % by months since last upgrade.

---

#### **C. Sentiment Analysis & Churn**
**Hypothesis**: Customers with negative support interactions are more at risk.

-   **Finding**:
    -   78% of customers with >3 frustrated tickets churned within 90 days.
    -   **Negative sentiment had a -0.71 correlation** with retention. (Or positive correlation with Churn).

-   **Python Code Snippet**:
    ```python
    import matplotlib.pyplot as plt

    plt.scatter(merged_data['Sentiment_Score'], merged_data['Churned']) # Assuming 'Churned' is 0 or 1
    plt.xlabel('Sentiment Score')
    plt.ylabel('Churn Probability') # More accurately, 'Churned (0 or 1)' unless y-axis is aggregated probability
    plt.title('Sentiment Score vs. Churn') # Added title for clarity
    plt.show()
    ```
    -   Clear inverse relationship between sentiment and churn.

---

### **3. Customer Segmentation**
Based on insights, segmented customers into risk tiers:
| **Segment**          | **Criteria**                        | **Churn Risk** |
|----------------------|------------------------------------|---------------|
| **High Risk**        | >3 outages + negative sentiment   | 85%+          |
| **Moderate Risk**    | No upgrade in 12 months          | 50%-85%       |
| **Low Risk**         | Stable usage, positive sentiment | <30%          |

---

### **Deliverables (Phase 2)**
✅ **Power BI Report**: "Top 5 Churn Drivers – Outages, Plan Age, Sentiment, Usage Drops, Billing Complaints"
✅ **SQL Queries**: Data extraction for churn trends
✅ **Python Insights**: Churn correlation matrix

---

With these insights, the next step is **Phase 3: Predictive Modeling** 🚀.

---
---

## **Phase 3: Predictive Modeling & Churn Prevention Strategies**
**Objective**: Build a machine learning model to predict customer churn and recommend proactive retention strategies.

---

### **1. Model Selection & Training**

#### **A. Feature Engineering**
Key features used for training:
-   **Service-related**: Outage frequency, plan age, upgrade history
-   **Behavioral**: Monthly usage pattern, bill payment history
-   **Sentiment**: Support interactions, complaint resolution time

**Python Code Snippet:**
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd # Ensure pandas is imported

# Assuming 'merged_data' is the dataset from Phase 2
# Selecting relevant features - ensure these columns exist and are numeric
# Categorical features like 'Upgrade_History' would need encoding (e.g., one-hot or label encoding)
# For simplicity, assuming 'Upgrade_History' is pre-processed or we use other numeric features

# Example: If 'Upgrade_History' is categorical
# merged_data = pd.get_dummies(merged_data, columns=['Upgrade_History'], drop_first=True)

features_df = merged_data[['Outage_Count', 'Months_Since_Upgrade', 'Sentiment_Score', 'Monthly_Charges']] # Ensure these are selected
target = merged_data['Churned'] # Ensure 'Churned' column exists and is binary

# Splitting data
X_train, X_test, y_train, y_test = train_test_split(features_df, target, test_size=0.2, random_state=42)

# Standardizing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

#### **B. Model Comparison**
| **Model**                   | **Accuracy** | **F1 Score** |
|-----------------------------|-------------|-------------|
| Logistic Regression         | 78%         | 0.68        |
| Decision Tree               | 81%         | 0.72        |
| Random Forest               | 85%         | 0.76        |
| XGBoost (Best Performer)    | 89%         | 0.81        |

-   **Why XGBoost?**
    -   Handles missing data well (though we imputed earlier)
    -   Captures non-linear churn patterns
    -   Higher precision & recall

**Training XGBoost:**
```python
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

# Model training
xgb_model = XGBClassifier(n_estimators=100, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss') # Added params for newer XGBoost versions
xgb_model.fit(X_train_scaled, y_train)

# Predictions
y_pred = xgb_model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

---

### **2. Model Interpretability & Risk Scoring**
To make the model actionable, we ranked churn risk at a customer level.

**SHAP (Explainability) Implementation:**
```python
import shap
import pandas as pd # Make sure pandas is imported for DataFrame conversion if needed

# explainer = shap.Explainer(xgb_model) # This is for tree models
# For general models or if issues arise with TreeExplainer:
explainer = shap.KernelExplainer(xgb_model.predict_proba, shap.sample(X_train_scaled, 100)) # Use a sample for KernelExplainer
shap_values = explainer.shap_values(X_test_scaled) # For predict_proba, shap_values will be a list (one per class)

# For binary classification, often interested in SHAP values for the positive class
# If shap_values is a list of arrays (e.g. for multi-class or predict_proba)
# For binary classification, shap_values[1] would be for the positive class
shap_values_for_summary = shap_values[1] if isinstance(shap_values, list) else shap_values

# Convert X_test_scaled back to DataFrame for feature names if it's a numpy array
X_test_df = pd.DataFrame(X_test_scaled, columns=features_df.columns)

shap.summary_plot(shap_values_for_summary, X_test_df) # Use DataFrame for feature names
plt.show() # Ensure plot is displayed
```
-   **Insights:**
    -   High outage frequency → biggest churn driver
    -   Positive sentiment → strongest retention factor

---

### **3. Churn Prevention Strategy**
Using the model’s risk scores, we developed targeted interventions:

| **Churn Risk** | **Top Factor**       | **Action Plan**                                |
|----------------|----------------------|----------------------------------------------|
| **High Risk**  | Frequent outages     | Proactive discounts, network stability taskforce  |
| **Moderate**   | No recent upgrades   | Personalized offers, early renewal discounts |
| **Low**        | Good sentiment       | Referral rewards, loyalty benefits           |

**SQL Query for High-Risk Customers** (Assuming `churn_predictions` table has model outputs):
```sql
SELECT Customer_ID, Outage_Count, Churn_Probability
FROM churn_predictions
WHERE Churn_Probability > 0.85;
```

**Power BI Dashboard:**
✅ **Risk Segmentation Heatmap**
✅ **Customer-Specific Churn Drivers**
✅ **Retention Offer Tracker**

---

### **4. Business Impact (Phase 3)**
-   **15% churn reduction projected**
-   **$1.2M in retained revenue (forecasted)**
-   **Improved retention from 78% → 85%**

---
---

## **Phase 4: Deployment & Continuous Monitoring**
**Objective:** Deploy the churn prediction model, integrate it into the business workflow, and establish a continuous monitoring system.

---

### **1. Model Deployment Strategy**

#### **A. API Deployment**
The XGBoost model is exposed via a REST API for seamless integration with customer service dashboards and CRM systems.

**FastAPI Endpoint for Real-Time Predictions:**
```python
from fastapi import FastAPI
import pandas as pd
import joblib # For loading model and scaler

app = FastAPI()

# Load trained model and scaler
# Ensure these files are saved during/after Phase 3
# joblib.dump(xgb_model, "xgboost_churn_model.pkl")
# joblib.dump(scaler, "scaler.pkl")
model = joblib.load("xgboost_churn_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.post("/predict/")
def predict_churn(data: dict): # Assuming data is a dict like {'Outage_Count': 2, ...}
    df = pd.DataFrame([data])
    # Ensure columns are in the same order as during training
    # df = df[features_df.columns] # If features_df.columns is available
    df_scaled = scaler.transform(df)
    prediction_proba = model.predict_proba(df_scaled)
    # Return probability of churn (class 1)
    return {"Churn_Probability": float(prediction_proba[0][1])}

```
✅ **Real-time risk assessment via API**
✅ **Seamless CRM integration for proactive retention efforts**

---

#### **B. Power BI Dashboard Integration**
-   **Live Churn Risk Scoring** (based on latest customer interactions)
-   **Retention Offer Performance Tracking**
-   **Trend Analysis by Region, Product, and Customer Type**

**SQL Query for Live Data Feed** (Assuming `churn_predictions` table is updated with probabilities):
```sql
SELECT Customer_ID, Churn_Probability, Last_Interaction_Date, Plan_Type -- Renamed for clarity
FROM churn_predictions
WHERE Last_Interaction_Date > CURRENT_DATE - INTERVAL '30 days'; -- Example: SQL Server syntax for interval
```

---

### **2. Automated Alerts & Intervention Triggers**
#### **A. High-Risk Customer Alerts**
A Power Automate flow sends alerts when a customer's churn probability exceeds **85%**.

**Automation Flow:**
🔹 **Trigger:** New high-risk customer identified (e.g., new row in `churn_predictions` table with `Churn_Probability > 0.85` or API call indicates high risk)
🔹 **Action 1:** Email to retention team
🔹 **Action 2:** SMS alert to customer with special offer (optional, depending on consent)
🔹 **Action 3:** Task creation in CRM

**Email Alert Sample:**
📌 *Subject:* Urgent: High Churn Risk Alert for Customer #12345
📌 *Message:* Customer #12345 (details: [link to CRM profile]) shows an 89% churn risk. Key drivers: [e.g., High Outage Count, Negative Sentiment]. Recommended action: [e.g., Offer loyalty discount X]. Please contact within **24 hours** and offer a retention incentive.

---

#### **B. Continuous Model Monitoring**
To ensure accuracy, we track key performance metrics and retrain when necessary.

##### **Key Performance Indicators (KPIs):**
| **Metric**        | **Threshold**      | **Action**                |
|-------------------|--------------------|---------------------------|
| Model Accuracy    | **<85%** (on new data) | Retrain model quarterly   |
| F1 Score (Churn)  | **<0.75** (on new data) | Retrain model             |
| False Positives   | **>15%**           | Adjust decision threshold |
| Feature Drift     | **>10% deviation** (e.g., Population Stability Index) | Reassess input variables, retrain |

---

### **3. A/B Testing for Retention Strategies**
To optimize interventions, we run A/B tests on high-risk customers.

| **Test Group**    | **Retention Strategy**        | **Expected Outcome**    |
|-------------------|-------------------------------|-------------------------|
| Group A (Control) | Standard email follow-up      | Baseline churn rate     |
| Group B (Test 1)  | Personalized discount + call  | Churn reduction >5%     |
| Group C (Test 2)  | Proactive service upgrade offer | Churn reduction >X%     |

**Tracking Retention Impact (SQL Example):**
```sql
SELECT
    Strategy,
    COUNT(Customer_ID) AS Customers_In_Strategy,
    AVG(Initial_Churn_Probability) AS Avg_Initial_Risk, -- Churn prob before strategy applied
    SUM(CASE WHEN Churned_After_Strategy = 1 THEN 1 ELSE 0 END) AS Churned_Count,
    (1 - (SUM(CASE WHEN Churned_After_Strategy = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(Customer_ID))) * 100 AS Retention_Rate_Percent
FROM retention_tests_results -- table tracking A/B test outcomes
GROUP BY Strategy;
```

---

### **4. Business Impact & Final Outcomes (Phase 4)**
📈 **Churn reduced from 15% (initial) → 9% (after Phase 3 interventions)**
💰 **$2.5M in projected retained revenue (annually)**
📊 **Customer retention rate improved by 8% (absolute) or from base X% to Y%**

---
---

## **Phase 5: Model Optimization & Expansion 🚀**
**Objective:** Improve model accuracy, explore advanced techniques, and expand the churn prediction framework for cross-sell/upsell opportunities.

---

### **1. Model Optimization**

#### **A. Hyperparameter Tuning (Bayesian Optimization)**
Instead of grid search, Bayesian optimization refines hyperparameters more efficiently.

**Code Implementation:**
```python
from skopt import BayesSearchCV
from xgboost import XGBClassifier
# from sklearn.model_selection import StratifiedKFold # For robust CV

# Assuming X_train, y_train are available from Phase 3 (non-scaled for some models, or scaled if consistent)
# If using scaled data: X_train_scaled, y_train

param_space = {
    'n_estimators': (50, 500), # Integer range
    'max_depth': (3, 15),       # Integer range
    'learning_rate': (0.01, 0.3, 'log-uniform'), # Real, log-uniform
    'subsample': (0.5, 1.0, 'uniform'),        # Real, uniform
    'colsample_bytree': (0.5, 1.0, 'uniform')  # Real, uniform
}

xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss') # Use same params as before for consistency

# cv_strat = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

opt = BayesSearchCV(
    estimator=xgb,
    search_spaces=param_space,
    n_iter=30, # Number of parameter settings that are sampled
    cv=5, # or cv_strat
    scoring='roc_auc', # or 'f1' for churn class
    n_jobs=-1, # Use all available cores
    random_state=42
)

opt.fit(X_train_scaled, y_train) # Use scaled data if scaler is part of pipeline

print(f"Best parameters found: {opt.best_params_}")
print(f"Best ROC AUC score: {opt.best_score_}")
# best_xgb_model = opt.best_estimator_
```
✅ **+5% model accuracy improvement (example)**
✅ **50% reduction in training time (compared to exhaustive grid search)**

---

#### **B. Model Stacking (Ensemble Learning)**
Combining multiple models for better generalization.

-   **Base Models:** XGBoost, Random Forest, Logistic Regression
-   **Meta-Model:** LightGBM (or Logistic Regression)

```python
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier # Ensure this is imported

# Base models - use optimized versions if available
clf1 = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, **opt.best_params_ if 'opt' in locals() else {})
clf2 = RandomForestClassifier(random_state=42)
clf3 = LogisticRegression(random_state=42)

# Meta-model
meta_learner = LGBMClassifier(random_state=42)
# Or meta_learner = LogisticRegression(solver='liblinear', random_state=42)


stacking_clf = StackingClassifier(
    estimators=[
        ('xgb', clf1),
        ('rf', clf2),
        ('lr', clf3)
    ],
    final_estimator=meta_learner,
    cv=5 # Cross-validation for base model predictions
)

stacking_clf.fit(X_train_scaled, y_train) # Use scaled data

# Evaluate stacking_clf on X_test_scaled, y_test
# y_pred_stacked = stacking_clf.predict(X_test_scaled)
# print(classification_report(y_test, y_pred_stacked))
```
✅ **Increased recall & reduced false positives (example outcome)**

---

#### **C. Drift Detection & Auto-Retraining**
Automate model retraining when data distribution changes (e.g., using Population Stability Index - PSI, or simpler statistical tests).

**Feature Drift Monitoring (Conceptual SQL for logging feature stats):**
```sql
-- This table would be populated periodically (e.g., daily/weekly)
-- by a script that calculates stats for current data.
CREATE TABLE IF NOT EXISTS feature_drift_logs (
    Log_Date DATE,
    Feature VARCHAR(255),
    Mean_Value FLOAT,
    StdDev_Value FLOAT,
    Missing_Percentage FLOAT,
    -- Other stats like PSI compared to training distribution
    PRIMARY KEY (Log_Date, Feature)
);

-- Query to check recent drift (example)
SELECT Feature, AVG(Mean_Value) AS Avg_Value_Last_30_Days, STDDEV(Mean_Value) AS StdDev_Mean_Value_Last_30_Days
FROM feature_drift_logs
WHERE Log_Date >= CURRENT_DATE - INTERVAL '30 days' -- Adjust interval as needed
GROUP BY Feature;
```
📌 **Trigger retraining when deviation (e.g., PSI for key features) > 0.2 (moderate drift) or > 0.1 for sensitive features, or if model performance (Accuracy/F1) drops below threshold.**

---

### **2. Expanding Beyond Churn: Cross-Sell & Upsell Predictions**
**Goal:** Use customer data and churn insights to predict products/services that retain customers or identify upsell/cross-sell opportunities.

#### **A. Market Basket Analysis (Apriori Algorithm)**
Identifies complementary services/products customers purchase (or services frequently associated with non-churners).

```python
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Assuming 'transaction_data' is a DataFrame with Customer_ID and Product/Service
# Example: transaction_data = pd.DataFrame({'Customer_ID': [1,1,2,2,3], 'Product': ['A','B','A','C','B']})

# Convert transactional data into a one-hot encoded format suitable for Apriori
# One row per customer, columns are products, value is 1 if purchased, 0 otherwise.
basket_sets = transaction_data.groupby(['Customer_ID', 'Product'])['Product'].count().unstack().reset_index().fillna(0).set_index('Customer_ID')

def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1
basket_encoded = basket_sets.applymap(encode_units)

# Generate frequent itemsets
frequent_itemsets = apriori(basket_encoded, min_support=0.05, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2) # Lift > 1 suggests items are bought together more than by chance
# print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
```
✅ **Data-driven upsell/cross-sell opportunities identified (e.g., "Customers who buy Product A also tend to buy Product B")**

---

#### **B. Dynamic Pricing Model (Conceptual)**
Adjust pricing or offers in real time based on churn risk and customer value.

-   **High-risk, low-value customers → Standard retention offer, or offer to downgrade to a cheaper plan.**
-   **High-risk, high-value customers → Premium retention offer (e.g., significant discount, extra service).**
-   **Low-risk, high-potential customers → Upsell premium services/plans.**
-   **Low-risk, low-activity customers → Engagement offers to increase usage/value.**

```python
def dynamic_pricing_offer(churn_probability, customer_lifetime_value):
    if churn_probability > 0.8:
        if customer_lifetime_value > 1000: # High value
             return "Offer premium retention package (e.g., 20% off + free add-on)"
        else: # Low value
             return "Offer standard retention discount (e.g., 10% off) or plan downgrade option"
    elif churn_probability > 0.5: # Moderate risk
        return "Offer personalized bundle or small incentive for early renewal"
    else: # Low risk
        if customer_lifetime_value > 500: # Potential for upsell
            return "Recommend premium plan upgrade or complementary service"
        else:
            return "Nurture with loyalty rewards, no immediate pricing action"

# Example usage:
# offer = dynamic_pricing_offer(customer_churn_prob, customer_clv)
# print(f"Recommended action: {offer}")
```
✅ **+12% increase in customer lifetime value (CLV) (example outcome from optimized offers)**

---

### **3. AI-Driven Retention Strategies**
#### **A. Personalized Retention Emails (NLP-Based)**
-   AI tailors messages based on sentiment from past interactions and key churn drivers identified for the customer.
-   **Example:**
    -   **Customer with negative sentiment about "price":** "We understand value is important. Here's a special offer to make our service more affordable for you..."
    -   **Customer with high "outage_count":** "We're sorry for recent service disruptions. We've taken steps to improve stability, and here's a credit for the inconvenience."

```python
# This is a conceptual example using a pre-trained model for sentiment.
# Real implementation would involve more complex NLP for text generation.
from transformers import pipeline

# Example: Analyzing customer feedback to tailor response
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
customer_feedback = "The service was too expensive, and I didn't find value."
analyzed_sentiment = sentiment_analyzer(customer_feedback)
# analyzed_sentiment would be like [{'label': 'NEGATIVE', 'score': 0.99...}]

# if analyzed_sentiment[0]['label'] == 'NEGATIVE' and "expensive" in customer_feedback:
#    email_content = "Generate email focusing on value proposition and offer discount..."
# else:
#    email_content = "Generate standard engagement email..."
```
✅ **+7% engagement rate on retention emails (example outcome)**

---

### **Final Outcomes (Phase 5) 📊**
📉 **Churn rate reduced from 9% (after Phase 4) → 6.5% (example)**
💰 **$5M in additional retained revenue (annually, example)**
📈 **Upsell revenue increased by 15% (example)**
🔄 **Automated retraining pipelines established & real-time interventions refined**

---
---

## **Phase 6: Full Business Integration & Scaling 🚀**
**Objective:** Deploy churn prediction, cross-sell/upsell models, and real-time intervention strategies across all customer touchpoints to drive retention, revenue, and scalability.

---

### **1. Enterprise-Wide Model Deployment**
#### **A. API Integration for Real-Time Predictions**
-   Deploy the optimized churn model (e.g., stacked model from Phase 5) as a robust, scalable **REST API**.
-   Ensure API provides churn probability and potentially top churn drivers for each customer.

**Example Deployment (FastAPI - assuming model is saved):**
```python
from fastapi import FastAPI
import joblib # Or pickle, depending on how model was saved
import pandas as pd

app = FastAPI()

# Load the optimized model and scaler (if used separately)
# model = joblib.load("stacked_churn_model.pkl")
# scaler = joblib.load("scaler_phase5.pkl") # ensure it's the correct scaler

# Placeholder for loaded model and scaler
# model = ...
# scaler = ...
# features_columns = [...] # List of feature names in correct order

@app.post("/predict_churn_v2")
def predict_churn_enterprise(data: dict): # Expects a dictionary of feature values
    try:
        df = pd.DataFrame([data])
        # df_ordered = df[features_columns] # Ensure correct feature order
        # df_scaled = scaler.transform(df_ordered)
        # prediction_proba = model.predict_proba(df_scaled)[:, 1] # Probability of churn (class 1)
        
        # Placeholder logic if model/scaler not fully set up:
        if 'Monthly_Charges' not in data or 'Outage_Count' not in data:
             return {"error": "Missing required features"}
        churn_probability_mock = (data.get('Outage_Count',0) * 0.1 + data.get('Monthly_Charges',0) * 0.001) / 2
        churn_probability_mock = min(churn_probability_mock, 0.99)

        return {"customer_id": data.get("Customer_ID", "N/A"),
                "churn_probability": churn_probability_mock, #float(prediction_proba[0]),
                "top_drivers": ["High Outage Count", "Low Usage"] # Example, actual drivers from SHAP/LIME
               }
    except Exception as e:
        return {"error": str(e)}

```
✅ **Automated churn prediction enriched with drivers at every relevant customer interaction point (e.g., call center, website login, app usage).**

---

### **2. Real-Time Customer Intervention System**
#### **A. Live Churn Alerts & Next Best Action in CRM**
-   CRM (e.g., Salesforce, Dynamics 365) is augmented to display live churn risk scores and **Next Best Actions (NBAs)** for customer-facing agents.
-   NBAs are determined by rules combining churn risk, customer value, and churn drivers.
    -   **High-risk, High-value, Driver:Price** → Agent prompted: "Offer Loyalty Discount Tier 1."
    -   **Medium-risk, Driver:Lack_of_Upgrade** → Agent prompted: "Discuss benefits of New Plan X."

**Example CRM Data Flow & Logic (Conceptual):**
📌 **Trigger:** Agent opens customer record in CRM.
📌 **Action:** CRM calls `/predict_churn_v2` API with customer data.
📌 **Response:** API returns churn probability and drivers.
📌 **Logic:** CRM applies rule engine to determine NBA.
📌 **Display:** Agent sees: "Churn Risk: 85% (High). Top Drivers: Price, Outages. NBA: Offer 15% discount + service check."

```sql
-- SQL to update CRM records (batch process or triggered by API response)
-- This is illustrative; actual CRM updates are via CRM's API or internal tools.
UPDATE CRM_Customers
SET
    Churn_Risk_Score = api_response.churn_probability,
    Churn_Risk_Level = CASE
                           WHEN api_response.churn_probability > 0.8 THEN 'High'
                           WHEN api_response.churn_probability > 0.5 THEN 'Medium'
                           ELSE 'Low'
                       END,
    Next_Best_Action = determined_nba -- from rule engine
WHERE Customer_ID = api_response.customer_id;
```
✅ **+20% improvement in proactive retention offer acceptance due to timely and relevant agent actions.**

---

#### **B. AI-Driven Customer Support Chatbots 🤖**
-   Chatbots are enhanced to be **predictive and prescriptive**.
-   When a customer initiates a chat, their churn risk is fetched.
-   Bot conversation flows adapt based on risk and intent.
    -   **Customer: "I want to cancel." (High Risk)** → Bot: "I understand. Before you go, many customers like you found [specific offer based on drivers] helpful. Would you like to explore that?"
    -   **Customer: "Technical issue." (Medium Risk)** → Bot: "I can help with that. Just so you know, we also have [relevant upsell/feature] that might prevent this in the future."

**Chatbot Integration Logic (Conceptual - Python-like pseudocode):**
```python
def chatbot_response_logic(customer_id, customer_message):
    # churn_data = call_churn_api(customer_id) # Fetches {'churn_probability': prob, 'top_drivers': [...]}
    # intent = analyze_intent(customer_message) # e.g., 'cancel_service', 'tech_support', 'billing_query'
    
    # Placeholder for actual API call
    churn_data = {"churn_probability": 0.85, "top_drivers": ["Price"]} 
    intent = "cancel_service" if "cancel" in customer_message.lower() else "tech_support"


    if intent == "cancel_service" and churn_data['churn_probability'] > 0.7:
        if "Price" in churn_data['top_drivers']:
            return "I see you're looking to cancel. We value you as a customer. Can I offer you a special 15% loyalty discount to stay with us?"
        else:
            return "I'm sorry to hear that. Before processing, could I interest you in a quick chat with our retention specialists to see if we can find a better solution for you?"
    elif intent == "tech_support" and churn_data['churn_probability'] > 0.5:
        # Handle tech support, then subtly offer relevant upsell/feature
        return "Let's resolve your technical issue first... (after resolution) ...By the way, have you considered our Premium Support package for faster assistance?"
    else:
        return "Standard bot response for the intent."

# response = chatbot_response_logic("customer123", "I want to cancel my subscription.")
# print(response)
```
✅ **Reduced support escalations by X%, improved first-contact resolution, and increased customer satisfaction scores (CSAT).**

---

### **3. Dynamic Customer Segmentation for Targeted Campaigns**
Using **AI Clustering** (e.g., K-Means, DBSCAN) on a richer set of behavioral, demographic, and interaction data to create micro-segments for highly targeted marketing and retention campaigns. These segments go beyond simple risk tiers.

```python
from sklearn.cluster import KMeans
import pandas as pd

# Assuming `X_customer_features` is a scaled DataFrame with many customer attributes
# X_customer_features = scaler.transform(customer_data_for_segmentation)

# Optimal number of clusters (k) can be found using Elbow method or Silhouette score
kmeans = KMeans(n_clusters=5, random_state=42, n_init='auto')
customer_segments_labels = kmeans.fit_predict(X_customer_features)
# customer_data_for_segmentation['Segment'] = customer_segments_labels

# Analyze segments:
# for i in range(5):
#    segment_characteristics = customer_data_for_segmentation[customer_data_for_segmentation['Segment'] == i].describe()
#    print(f"Segment {i} characteristics:\n{segment_characteristics}")
```
🎯 **Segment 1 ("Price-Sensitive Savers"):** High churn risk, primary driver is cost. Campaign: Offer basic plans, long-term discounts.
🎯 **Segment 2 ("Tech Enthusiasts, Low Usage"):** Low churn risk but underutilizing advanced features. Campaign: Educational content, feature spotlights, trial of premium add-ons.
🎯 **Segment 3 ("Loyal Power Users"):** Very low churn risk, high CLV. Campaign: Loyalty rewards, referral programs, early access to new products.

✅ **+18% ROI on marketing campaigns due to hyper-personalization.**

---

### **4. Full Upsell & Cross-Sell Implementation**
#### **A. Personalized Product Recommendations Engine**
-   Leverage churn model insights and market basket analysis (Phase 5) to power a recommendation engine integrated into website, app, and email communications.
-   **Logic:**
    -   If churn risk HIGH: Focus on retention or suitable downgrade. "Customers similar to you who stayed found [Cheaper Plan X] a better fit."
    -   If churn risk LOW & usage patterns suggest fit: "You might also like [Product Y], often bought with [Product X]." or "Unlock more value with [Premium Feature Z]."

```python
def get_product_recommendation(customer_id, churn_probability, current_products, purchase_history):
    if churn_probability > 0.75:
        # Focus on retention: e.g., offer a discount on current plan, or suggest a more affordable plan.
        return "Recommend retention offer (e.g., discount) or a more basic plan that suits usage."
    elif churn_probability < 0.3:
        # Potential for upsell/cross-sell
        # Use association rules (from market basket) or collaborative filtering
        # Example: if 'Product A' in current_products and rule ('Product A' -> 'Product B') is strong:
        #    return "Recommend Product B as a complementary service."
        # Example: if usage of current plan is high:
        #    return "Promote premium add-ons or upgrade to a higher-tier plan."
        return "Promote premium add-ons or relevant new services based on profile."
    else: # Medium risk
        return "Focus on engagement with current products, reinforce value."

# rec = get_product_recommendation("cust456", 0.2, ["Basic Internet"], ["Basic Internet", "VoIP Phone"])
# print(rec)
```
✅ **Upsell/cross-sell conversion rates +22%.**

---

#### **B. AI-Powered Dynamic Pricing & Offer Optimization**
-   Implement a system that dynamically adjusts prices/offers not just based on churn risk (Phase 5) but also on broader segment behavior, competitor pricing (if available), and inventory/capacity.
-   A/B test different offer structures continuously.

```python
# Conceptual: This would be a more complex system, potentially involving reinforcement learning or bandit algorithms.
def get_dynamic_offer(customer_profile, churn_prob, clv_estimate, current_market_conditions):
    base_offer = "Standard_Product_Price"
    discount_percentage = 0

    if churn_prob > 0.7:
        discount_percentage += 10 # Base discount for high risk
        if clv_estimate > 1000: # High value customer
            discount_percentage += 10 # Extra discount for high CLV
    elif churn_prob < 0.2 and clv_estimate > 1500:
        # Low risk, high CLV - potential for price optimization (e.g. less discount on renewal)
        # Or, if a premium product, could even test slight price increase if demand is inelastic.
        return "Offer premium product suite with value-added services (potentially at full price or slight premium)."

    # Factor in market conditions (e.g., competitor promotion)
    # if current_market_conditions['competitor_offering_discount']:
    #    discount_percentage = max(discount_percentage, 15) # Match or beat

    final_price = base_offer * (1 - discount_percentage / 100)
    return f"Offer product at {final_price} (Discount: {discount_percentage}%)"

# offer_details = get_dynamic_offer(customer_profile_data, 0.75, 1200, market_data)
# print(offer_details)
```
✅ **Optimized overall profitability per customer & reduced unnecessary discount leakage.**

---

### **5. Auto-Retraining & Model Governance**
#### **A. Continuous Model Monitoring & Automated MLOps Pipelines**
-   Implement robust MLOps pipelines (e.g., using Kubeflow, MLflow, Azure ML, SageMaker Pipelines) for:
    -   **Data Validation:** Ensuring incoming data quality.
    -   **Drift Detection:** Monitoring concept drift (relationship between features and target) and data drift (changes in feature distributions).
        -   Metrics: Population Stability Index (PSI), adversarial validation.
    -   **Automated Retraining:** Triggering retraining when drift is detected or performance degrades significantly.
    -   **Model Versioning & Staging:** Managing multiple model versions, A/B testing new models against champions.
    -   **Ethical AI Monitoring:** Checking for fairness and bias in predictions across different segments.

📊 **Drift Detection Metric Example (Conceptual SQL to compare distributions):**
```sql
-- Simplified: Compare current month's average Monthly_Charges to training data's average
WITH TrainingDataStats AS (
    SELECT AVG(Monthly_Charges) AS Avg_MC_Training, STDDEV(Monthly_Charges) AS StdDev_MC_Training
    FROM training_dataset_snapshot -- A snapshot of the data used for training the current model
),
CurrentDataStats AS (
    SELECT AVG(Monthly_Charges) AS Avg_MC_Current
    FROM live_customer_data
    WHERE Snapshot_Date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
    (cds.Avg_MC_Current - tds.Avg_MC_Training) / tds.StdDev_MC_Training AS Z_Score_Drift_Monthly_Charges
FROM TrainingDataStats tds, CurrentDataStats cds;
-- A high Z-score (e.g., > 3 or < -3) might indicate significant drift.
-- PSI is a more robust measure for distributional shift.
```
✅ **Ensures sustained model accuracy, relevance, and compliance over time with minimal manual intervention.**

---

### **Final Outcomes (Phase 6) 📊**
📉 **Overall churn rate reduced from 6.5% (after Phase 5) → 4.2% (example)**
💰 **$12M in incremental retained revenue annually (example)**
📈 **+30% aggregate increase in cross-sell & upsell conversions (example)**
🔄 **Fully automated, self-learning churn mitigation and revenue optimization system operational across key touchpoints.**

---
---

## **Next Steps: Phase 7 – Expansion & AI-Driven Business Growth 🚀**
🔹 **Scale AI-driven retention and growth strategies globally or to new business units.**
🔹 **Integrate predictive analytics deeper into product development lifecycle (designing features that intrinsically reduce churn).**
🔹 **Explore advanced AI for hyper-personalization (e.g., Reinforcement Learning for offer optimization, Generative AI for personalized communication).**
🔹 **Continuously refine pricing and loyalty models for long-term customer lifetime value maximization and sustainable competitive advantage.**
