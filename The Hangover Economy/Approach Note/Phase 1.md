### **Phase 1: Data Collection & Cleaning**  

#### **Objective**  
To aggregate, clean, and structure raw data from multiple sources into a unified dataset with high accuracy and completeness.  

---

#### **Data Sources & Issues**  
| **Source**              | **Format** | **Key Columns**                              | **Issues Identified** |
|-------------------------|-----------|---------------------------------------------|------------------------|
| **Transaction Logs**    | CSV       | `Timestamp, Store_ID, Product_ID, Price`   | Missing `Product_ID` (8%), inconsistent timestamps (12AM vs. 00:00), duplicates |
| **Loyalty Program Data** | SQL       | `User_ID, Age, Gender, Purchase_History`   | Some users lack purchase history (5%) |
| **Third-Party Surveys** | Excel     | `User_ID, Hangover_Frequency, Top_Purchase` | Self-reported bias, inconsistent categorizations |

---

#### **Key Tasks & Methodology**  

##### **1. Data Cleaning (Python & SQL)**
- **Handling Missing Values**:  
  - Drop rows where `Product_ID` is missing.  
  - Fill missing `Age` values in loyalty data using median imputation.  
- **Fixing Inconsistencies**:  
  - Convert timestamps into a uniform format.  
  - Standardize product categories and purchase labels.  
- **Removing Duplicates**:  
  - Deduplicate transactions using `Transaction_ID` and `Timestamp`.  

**Python Implementation Example:**  
```python
import pandas as pd  

# Load transaction data  
transactions = pd.read_csv('transactions.csv')  

# Convert timestamp format  
transactions['Timestamp'] = pd.to_datetime(transactions['Timestamp'], errors='coerce')  

# Remove duplicates  
transactions = transactions.drop_duplicates()  

# Drop missing Product_ID entries  
transactions = transactions.dropna(subset=['Product_ID'])  
```

---

##### **2. Data Merging & Transformation**
- **SQL Joins**: Combine transaction logs, loyalty data, and survey responses.  
- **Creating a Master Dataset**: Generate a unified table with customer demographics, purchase patterns, and product preferences.  

**SQL Query Example:**  
```sql
SELECT t.Store_ID, t.Product_ID, t.Timestamp, l.Age, l.Gender, s.Hangover_Frequency  
FROM transactions t  
LEFT JOIN loyalty_data l ON t.User_ID = l.User_ID  
LEFT JOIN survey_data s ON l.User_ID = s.User_ID;
```

---

#### **Deliverables**  
✅ **Cleaned dataset** with at least **95% completeness**.  
✅ **Data dictionary** defining key variables and transformations.  
✅ **Exploratory summary** (missing data report, key statistics).  

---

This phase ensures that the data is structured, consistent, and ready for trend analysis in **Phase 2**. Let me know if you need refinements!
