Here’s Phase 2 of the case study in detail:  

---

## **Phase 2: Exploratory Data Analysis (EDA)**  
**Objective**: Identify key churn drivers and customer risk patterns.  

### **1. Data Profiling**  
Before diving into insights, an initial check on data quality:  
- **Missing values**:  
  ```python
  print(merged_data.isnull().sum())
  ```
  - *Fix*: Imputed missing values using median for numeric fields and "Unknown" for categorical ones.  

- **Outliers detection**:  
  ```python
  import seaborn as sns  
  sns.boxplot(x=merged_data['Monthly_Charges'])  
  ```
  - *Fix*: Winsorized extreme values (>99th percentile).  

---

### **2. Churn Triggers Analysis**  
#### **A. Outage Frequency & Churn**  
**Hypothesis**: Customers with frequent network outages are more likely to leave.  

- **Finding**:  
  - 62% of churners experienced **>3 outages/month**.  
  - Non-churners averaged **0.8 outages/month**.  

- **Power BI Visualization**:  
  - A **heatmap** of churn risk vs. outage count.  

- **SQL Query to Extract Insights**:  
  ```sql  
  SELECT Outage_Count, COUNT(*) AS Customer_Count,  
         SUM(CASE WHEN Churned = 1 THEN 1 ELSE 0 END) AS Churners  
  FROM merged_data  
  GROUP BY Outage_Count  
  ORDER BY Outage_Count DESC;  
  ```

---

#### **B. Plan Age & Churn**  
**Hypothesis**: Customers on older plans with no upgrades are likelier to churn.  

- **Finding**:  
  - Customers **without upgrades in 12+ months** churn **3x faster**.  
  - Legacy plan users had an **18% higher churn rate**.  

- **Python Correlation Check**:  
  ```python  
  print(merged_data[['Months_Since_Upgrade', 'Churned']].corr())  
  ```
  - Correlation: **0.63 (positive)** → Strong link between outdated plans and churn.  

- **Power BI Visualization**:  
  - A **line chart** showing churn % by months since last upgrade.  

---

#### **C. Sentiment Analysis & Churn**  
**Hypothesis**: Customers with negative support interactions are more at risk.  

- **Finding**:  
  - 78% of customers with >3 frustrated tickets churned within 90 days.  
  - **Negative sentiment had a -0.71 correlation** with retention.  

- **Python Code Snippet**:  
  ```python  
  import matplotlib.pyplot as plt  

  plt.scatter(merged_data['Sentiment_Score'], merged_data['Churned'])  
  plt.xlabel('Sentiment Score')  
  plt.ylabel('Churn Probability')  
  plt.show()  
  ```
  - Clear inverse relationship between sentiment and churn.  

---

### **3. Customer Segmentation**  
Based on insights, segmented customers into risk tiers:  
| **Segment**          | **Criteria**                        | **Churn Risk** |  
|----------------------|------------------------------------|---------------|  
| **High Risk**        | >3 outages + negative sentiment   | 85%+          |  
| **Moderate Risk**    | No upgrade in 12 months          | 50%-85%       |  
| **Low Risk**         | Stable usage, positive sentiment | <30%          |  

---

### **Deliverables**  
✅ **Power BI Report**: "Top 5 Churn Drivers – Outages, Plan Age, Sentiment, Usage Drops, Billing Complaints"  
✅ **SQL Queries**: Data extraction for churn trends  
✅ **Python Insights**: Churn correlation matrix  

---

With these insights, the next step is **Phase 3: Predictive Modeling** 🚀.
