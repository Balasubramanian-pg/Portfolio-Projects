
---

# **The Hangover Economy - Post-Party Purchase Analyzer**  
**Tools**: Python, SQL, Excel, Power BI | **Duration**: 8-week Internship  
**Business Context**: A national convenience store chain, *QuickStop*, wants to capitalize on the $50B "hangover economy" by optimizing product placement, promotions, and partnerships for hungover consumers.  

---

## **Problem Statement**  
*QuickStop* loses 15% of post-party sales to competitors due to inefficient inventory and marketing. They need to:  
1. **Increase post-party sales** by 25% in 6 months.  
2. **Identify top-selling products** by time, location, and demographic.  
3. **Launch targeted promotions** (e.g., "Hangover Recovery Bundles").  

---

## **Your Role as an Intern**  
Analyze transaction data, segment consumers, and design a dashboard to drive data-driven decisions.  

---

### **Phase 1: Data Collection & Cleaning**  
**Objective**: Aggregate messy, multi-source data into a unified dataset.  

#### **Data Sources**  
1. **Transaction Logs** (CSV, 500K+ rows):  
   - Columns: `Timestamp, Store_ID, Product_ID, Price, Payment_Method`.  
   - Issues: Missing `Product_ID` (8% of rows), inconsistent timestamps (12AM vs. 00:00).  
2. **Loyalty Program Data** (SQL):  
   - `User_ID, Age, Gender, Purchase_History`.  
3. **Third-Party Surveys** (Excel):  
   - Self-reported hangover spending habits (1,200 responses).  

#### **Tasks**  
1. **Clean Transaction Data** (Python):  
   ```python  
   import pandas as pd  

   # Fix timestamps and drop duplicates  
   def clean_transactions(df):  
       df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')  
       df = df.dropna(subset=['Product_ID'])  
       df = df.drop_duplicates()  
       return df  

   # Example  
   transactions = pd.read_csv('transactions.csv')  
   cleaned_data = clean_transactions(transactions)  
   ```  

2. **Merge SQL + Survey Data** (SQL Join):  
   ```sql  
   SELECT l.User_ID, l.Age, s.Hangover_Frequency, s.Top_Purchase  
   FROM loyalty_data l  
   JOIN survey_data s ON l.User_ID = s.User_ID;  
   ```  

**Deliverable**:  
- Cleaned dataset with 95% completeness.  
- Data dictionary explaining `Hangover_Frequency` codes (e.g., 1 = "Weekly").  

---

### **Phase 2: Trend Analysis**  
**Objective**: Uncover when, where, and what hungover consumers buy.  

#### **Key Analysis**  
1. **Peak Purchase Hours** (Power BI):  
   - 65% of electrolyte drinks sell between 8-11 AM on weekends.  
2. **Demographic Trends** (Excel Pivot):  
   - Men aged 21-30 buy 3x more spicy snacks post-party than women.  
3. **Product Affinity** (Python):  
   ```python  
   # Identify frequently bought-together items  
   from mlxtend.frequent_patterns import apriori  

   basket = pd.pivot_table(data, index='Transaction_ID', columns='Product_ID', aggfunc='size', fill_value=0)  
   frequent_items = apriori(basket, min_support=0.05, use_colnames=True)  
   ```  
   - Top pairs: Energy drinks + breakfast sandwiches, pain relievers + water.  

#### **Deliverable**:  
- Report highlighting "Prime Time Windows" and product recommendations.  

---

### **Phase 3: Consumer Segmentation**  
**Objective**: Group buyers into actionable personas.  

#### **Clustering** (Python):  
```python  
from sklearn.cluster import KMeans  

# Features: Purchase time, basket composition, spend  
X = df[['Hour', 'Energy_Drink_Count', 'Total_Spend']]  
kmeans = KMeans(n_clusters=4)  
df['Segment'] = kmeans.fit_predict(X)  
```  

#### **Personas**  
1. **Breakfast Rescuers**: Buy sandwiches + coffee at 9 AM.  
2. **Late-Night Cravers**: Purchase snacks + alcohol post-midnight.  
3. **Wellness Rehabilitators**: Electrolytes + painkillers at 8 AM.  

#### **Deliverable**:  
- Power BI visual of segments with filters for age/gender.  

---

### **Phase 4: Marketing Strategy & Simulation**  
**Objective**: Design and predict promo success.  

#### **Promo Ideas**  
1. **Early Bird Bundle**: 20% off breakfast sandwich + energy drink (8-11 AM).  
2. **Night Owl Deal**: Free chips with alcohol purchase (10 PM-2 AM).  

#### **Impact Simulation** (Python):  
```python  
# Predict sales lift using historical elasticity  
def simulate_promo(base_sales, discount, elasticity=1.2):  
    price_change = -discount  # 20% discount = -20% price  
    sales_lift = elasticity * price_change  
    return base_sales * (1 + sales_lift/100)  

base_sales = 1000  # Weekly sandwich sales  
discount = 20  
new_sales = simulate_promo(base_sales, discount)  # Output: 1,240 units  
```  

#### **Deliverable**:  
- Financial model in Excel showing 12-week ROI for each promo.  

---

### **Phase 5: Dashboard & Stakeholder Playbook**  
**Objective**: Empower managers to act on insights.  

#### **Power BI Dashboard**  
- **Home Tab**:  
  - Real-time sales by segment.  
  - Map of top-performing stores.  
- **Promo Tab**:  
  - Actual vs. projected sales for campaigns.  
  - Break-even countdown (e.g., "100 units left to hit target").  

#### **Stakeholder Playbook**  
1. **Inventory Cheat Sheet**: Stock 20% more energy drinks on weekends.  
2. **Staff Training**: Upsell "Hangover Kits" during peak hours.  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Post-Party Sales     | $1.2M/mo | $1.5M/mo (+25%)  |  
| Customer Retention   | 55%     | 68%               |  
| Avg. Basket Size     | $8.50   | $10.20            |  

---

## **Real-World Challenges**  
1. **Data Bias**: Survey respondents skewed toward tech-savvy millennials (fixed by weighting).  
2. **Inventory Pushback**: Store managers resisted stocking "unhealthy" items (resolved with profit-sharing incentives).  
3. **Privacy Concerns**: Masked `User_ID` in dashboards to comply with GDPR.  

---

## **Deliverables**  
1. **Technical**:  
   - Python scripts for clustering and simulations.  
   - SQL queries for merging loyalty/survey data.  
2. **Business**:  
   - Power BI dashboard with drill-down capabilities.  
   - Excel promo models + 10-slide stakeholder deck.  

---

This case study mimics real-world chaos and complexity, forcing the intern to balance analytics with human behavior and operational constraints.
