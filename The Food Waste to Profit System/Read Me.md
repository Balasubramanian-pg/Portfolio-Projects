# **Case Study: Food Waste Optimization for "FreshPlate" Restaurant Group**  
**Tools**: SQL, Excel, Power BI | **Duration**: 6-week Internship  
**Business Context**: FreshPlate operates 35 restaurants across 4 cities, wasting 18% of inventory ($220K/month). Their goals:  
1. Reduce food waste by 35% in 8 months.  
2. Donate 40% of surplus to nonprofits.  
3. Launch 3 upcycled product lines by Q4.  

---

## **Phase 1: Waste Audit & Root Cause Analysis (Excel)**  
**Task**: Analyze 6 months of waste data (200K+ rows) to identify patterns.  

### **Mock Dataset (Excel)**  
| Date       | Location | Food_Category | Item          | Waste_Reason     | Quantity_kg | Cost  | Supplier |  
|------------|----------|---------------|---------------|------------------|-------------|-------|----------|  
| 2023-03-15 | Chicago  | Bakery        | Sourdough     | Overproduction   | 12.5        | $45   | Supplier A |  
| 2023-03-15 | Houston  | Produce       | Spinach       | Spoilage         | 8.2         | $28   | Supplier B |  
| ...        | ...      | ...           | ...           | ...              | ...         | ...   | ...      |  

**Real-World Complexity**:  
- Inconsistent date formats (MM/DD vs. DD-MM-YYYY).  
- 15% of entries missing `Waste_Reason` or `Supplier`.  
- Outliers (e.g., a single entry showing 500kg of "beef waste" due to data entry error).  

**Deliverables**:  
1. **Cleaned Dataset**:  
   - Use `TEXT-TO-COLUMNS`, `TRIM`, and `IFERROR` to standardize dates.  
   - Apply `VLOOKUP` to fill missing `Supplier` data from a master list.  
2. **Pivot Analysis**:  
   - Top 5 wasteful items by cost: `=SUMIFS(Cost, Item, "Sourdough")`.  
   - Waste reason trends: 62% of bakery waste is from "overproduction" on weekends.  
3. **Recommendations**:  
   - Negotiate with Supplier B (spoilage rate 22% vs. Supplier A’s 9%).  
   - Adjust weekend bakery production by 30%.  

---

## **Phase 2: Redistribution Engine (SQL)**  
**Task**: Build a system to match surplus food with nonprofits.  

### **Database Schema**  
```sql  
CREATE TABLE inventory (  
  item_id INT PRIMARY KEY,  
  item_name VARCHAR(50),  
  category VARCHAR(20),  
  quantity_kg DECIMAL,  
  expiry_date DATE,  
  location VARCHAR(20)  
);  

CREATE TABLE nonprofits (  
  org_id INT PRIMARY KEY,  
  org_name VARCHAR(50),  
  needs VARCHAR(100),  -- e.g., "perishables, frozen"  
  pickup_capacity_kg DECIMAL  
);  
```  

**Complex Queries**:  
1. **Daily Surplus Matching**:  
```sql  
SELECT   
  i.location,  
  i.item_name,  
  i.quantity_kg,  
  n.org_name  
FROM inventory i  
JOIN nonprofits n  
  ON i.category = CASE  
    WHEN n.needs LIKE '%perishable%' THEN 'Produce'  
    WHEN n.needs LIKE '%frozen%' THEN 'Meat'  
  END  
WHERE i.expiry_date = CURDATE() + INTERVAL 1 DAY  
  AND i.quantity_kg <= n.pickup_capacity_kg;  
```  

2. **Weekly Donation Report**:  
```sql  
SELECT   
  WEEK(expiry_date) AS week_number,  
  location,  
  SUM(quantity_kg) AS total_donated,  
  COUNT(DISTINCT org_id) AS nonprofits_served  
FROM inventory  
GROUP BY week_number, location;  
```  

**Real-World Hurdles**:  
- Nonprofit "City Harvest" can only accept 50kg/day but surplus averages 80kg.  
- 20% of donations go unclaimed due to last-minute cancellations.  

---

## **Phase 3: Profitability Modeling (Excel + Power BI)**  
**Task**: Build a financial model for upcycled products.  

### **Upcycled Product Analysis (Excel)**  
| Product      | Input_Waste | Input_Cost/kg | Labor_Cost | Packaging | Selling_Price | Monthly_Volume |  
|--------------|-------------|---------------|------------|-----------|---------------|----------------|  
| Veggie Broth | 300kg       | $0.50         | $1.20      | $0.80     | $4.50         | 500 units      |  
| Fruit Jam    | 150kg       | $0.30         | $2.00      | $1.50     | $6.00         | 300 units      |  

**Formulas**:  
- **COGS/Unit**: `=(Input_Cost*Input_Waste + Labor_Cost + Packaging)/Monthly_Volume`  
- **Profit Margin**: `=(Selling_Price - COGS)/Selling_Price`  

**Sensitivity Analysis**:  
- What-if table for 10-15% increases in labor costs.  
- Break-even point using `GOAL SEEK`: Jam needs 275 units/month to break even.  

---

## **Phase 4: Executive Dashboard (Power BI)**  
**Requirements**:  
1. **Live Waste Tracker**:  
   - Map overlay showing waste by location.  
   - Trend line comparing current vs. target waste (e.g., 35% reduction goal).  
2. **Donation Metrics**:  
   - Donation fulfillment rate (actual vs. potential).  
   - Top nonprofits by volume received.  
3. **Revenue Engine**:  
   - Actual vs. projected revenue from upcycled products.  
   - ROI timeline for new product lines.  

**Advanced Features**:  
- **Drillthrough Page**: Click a location to see item-level waste details.  
- **DAX Measures**:  
  ```  
  Waste Cost Savings = SUMX(Inventory, [Quantity_kg] * [Avg_Cost/kg] * 0.35)  
  ```  
- **Data Alerts**: Email managers if a location exceeds daily waste thresholds.  

---

## **Phase 5: Stakeholder Presentation**  
**Mock Scenario**: Present findings to CFO and Head of Sustainability.  

**Slide 1: Problem & Insights**  
- "Bakery waste costs $12K/month, 80% from weekend overproduction."  
- "20% of donations fail due to capacity mismatches."  

**Slide 2: Financial Impact**  
- **Cost Savings**: $220K/month waste → $143K/month after fixes (35% reduction).  
- **New Revenue**: $8K/month from broth/jam sales (scaling to $25K/month by Q4).  

**Slide 3: Proposed Actions**  
1. Redesign weekend bakery menu to use 30% less dough.  
2. Partner with "WasteNot" logistics for donation pickups.  
3. Pilot veggie broth in 5 locations by November.  

---

## **Realistic Deliverables**  
1. **Excel Files**:  
   - `FreshPlate_Waste_Audit.xlsx` (cleaned data + pivot tables).  
   - `Upcycled_Financial_Model.xlsx` (dynamic what-if scenarios).  
2. **SQL Scripts**:  
   - `daily_donation_matching.sql` (automated surplus matching).  
   - `weekly_impact_report.sql`.  
3. **Power BI File**:  
   - `FreshPlate_Dashboard.pbix` with drilldowns and mobile view.  
4. **Documentation**:  
   - 10-page playbook: "How to Scale Upcycled Products."  
   - 5-minute Loom video demoing the dashboard.  

---

## **Added Complexity (Real-World Touches)**  
- **Data Privacy**: Mask nonprofit names as "Nonprofit A", "Nonprofit B" in deliverables.  
- **Change Resistance**: Mock email from a restaurant manager: *"Reducing bakery portions will hurt customer satisfaction!"* (Intern must propose solutions).  
- **Supply Chain Constraints**: Supplier B refuses to negotiate – pivot to alternative suppliers.  

---

## **Business Impact Metrics**  
| Metric                | Before | After 6 Months |  
|-----------------------|--------|----------------|  
| Monthly Waste Cost    | $220K  | $143K (-35%)   |  
| Donations Fulfilled   | 15%    | 48%            |  
| Upcycled Revenue      | $0     | $8K            |  
| CO2 Emissions (tons)  | 45     | 29 (-36%)      |  

---

This structure forces the intern to:  
1. Work with messy, real-world data.  
2. Balance idealism (zero waste goals) with practicality (profitability).  
3. Communicate technical findings to non-technical stakeholders.  

Want to add even more depth? We could include mock email threads, a Gantt chart for the project, or a Python script for data cleaning (though you specified SQL/Excel/PBI). Let me know!
