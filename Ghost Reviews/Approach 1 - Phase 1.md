### **Phase 1: Data Aggregation & Cleaning – Approach Note**  

#### **Objective**  
To integrate and clean fragmented customer data from multiple sources (CRM, billing, usage logs, and support tickets) to create a high-quality dataset for churn prediction.  

#### **Key Challenges & Considerations**  
1. **Data Completeness** – Missing values in `Upgrade_History` (15%) and inconsistent tenure data.  
2. **Data Volume & Performance** – Handling 2M+ rows of usage logs efficiently.  
3. **Data Standardization** – Merging SQL, CSV, and JSON formats into a unified structure.  

---

### **Step 1: Extract & Load Data**  
- **SQL Query for CRM Data Extraction**  
  ```sql
  SELECT Customer_ID, Plan_Type, Tenure, Monthly_Charges, Upgrade_History  
  FROM customers;
  ```
- **Load CSV (Usage Logs) & JSON (Support Tickets) into Pandas**  
  ```python
  import pandas as pd  
  usage = pd.read_csv("usage_logs.csv")  
  support = pd.read_json("support_tickets.json")  
  ```

---

### **Step 2: Data Cleaning & Transformation**  
- **Fix Tenure Inconsistencies** (Negative Values)  
  ```sql
  UPDATE customers  
  SET Tenure = ABS(Tenure)  
  WHERE Tenure < 0;
  ```
- **Handle Missing Values**  
  ```python
  merged_data['Upgrade_History'].fillna("No Upgrade", inplace=True)
  merged_data['Sentiment_Score'].fillna(0, inplace=True)  # Assume neutral sentiment if no ticket
  ```
- **Convert Sentiment Text to Numerical Scores**  
  ```python
  sentiment_mapping = {'frustrated': -1, 'neutral': 0, 'satisfied': 1}
  support['Sentiment_Score'] = support['Sentiment_Text'].map(sentiment_mapping)
  ```

---

### **Step 3: Data Integration & Quality Check**  
- **Merge Datasets on `Customer_ID`**  
  ```python
  final_data = usage.merge(support, on="Customer_ID", how="left").merge(crm, on="Customer_ID", how="left")
  ```
- **Validate Data Completeness**  
  ```python
  missing_values = final_data.isnull().sum() / len(final_data) * 100
  print(missing_values)  # Ensure completeness >95%
  ```

---

### **Deliverables**  
1. **Cleaned Dataset** – Ensuring >95% data completeness.  
2. **Data Dictionary** – Mapping sentiment scores to risk levels.  
3. **Quality Report** – Summary of missing values handled, transformations applied, and integration status.  

This structured approach ensures reliable input data for predictive modeling in Phase 2.
