

### **Phase 1: Legacy Data Scraping & Manual Audits**  
**Objective**: *Estimate parking availability across 10,000 spaces without IoT.*  

#### **Challenges**  
1. **No Real-Time Data**: Legacy systems only log garage entry/exit timestamps (no live occupancy).  
2. **Analog Chaos**: 30% of garages use paper logs for monthly permits and visitor counts.  


### **Tool-Centric Approach**  
#### **1. SQL: Reverse-Engineer Occupancy**  
**Problem**: Garages have entry/exit timestamps but no live counts.  
**Solution**: Use **time-stamped ticket data** to model occupancy.  

```sql  
-- Calculate hourly garage occupancy  
WITH entries AS (  
  SELECT garage_id, DATE_TRUNC('hour', entry_time) AS hour, COUNT(*) AS entries  
  FROM garage_transactions  
  GROUP BY 1, 2  
),  
exits AS (  
  SELECT garage_id, DATE_TRUNC('hour', exit_time) AS hour, COUNT(*) AS exits  
  FROM garage_transactions  
  GROUP BY 1, 2  
)  
SELECT  
  e.garage_id,  
  e.hour,  
  SUM(e.entries - COALESCE(ex.exits, 0)) OVER (PARTITION BY e.garage_id ORDER BY e.hour) AS occupancy  
FROM entries e  
LEFT JOIN exits ex ON e.garage_id = ex.garage_id AND e.hour = ex.hour;  
```  
**Insight**: This assumes drivers don’t stay longer than 24 hours – validated against permit data.  


#### **2. Excel: Manual Data Reconciliation**  
**Problem**: Paper logs for permits and ad-hoc visitors.  
**Solution**:  
- Created a **shared Excel template** for garage attendants:  
  - *Daily*: Log total visitors, permits used, and "manual overrides" (e.g., construction closures).  
  - *Data Validation*: Use Excel formulas to flag outliers (e.g., `=IF(Visitors > Garage_Capacity, "ERROR", "")`).  

**Process**:  
- Collected 40+ Excel files weekly via email.  
- Used Power Query to merge files into a **master SQL table**.  


#### **3. Power BI: "Pseudo-Real-Time" Dashboard**  
**Problem**: Data is lagged by 24–48 hours.  
**Workaround**:  
- Built a **probabilistic occupancy model** in Power BI:  
  - *Baseline*: Historical occupancy patterns (e.g., "Garage 3 averages 60% full on Mondays").  
  - *Adjustments*: Manual inputs (e.g., "Today’s baseball game adds +1,200 cars").  

**Dashboard Logic**:  
```  
Estimated_Spots =   
Garage_Capacity * (1 - BASELINE_OCCUPANCY[%])   
- MANUAL_ADJUSTMENTS[Event_Demand]  
+ MANUAL_ADJUSTMENTS[Closures]  
```  
**Output**:  
- A "live-ish" map of parking availability, refreshed daily.  
- Confidence intervals shown as **data bars** (e.g., "Garage 5: 120–180 spots free").  


### **Deliverables**  
1. **SQL Pipeline**: Hourly occupancy trends from ticket data.  
2. **Excel Governance**: Standardized templates reduced manual errors by 65%.  
3. **Power BI Dashboard**:  
   - Filter by time/garage/event.  
   - "Worst-Case Scenario" toggle for planners.  


### **Trade-Offs & Hacks**  
- **Accuracy**: Model error rate was ±18% (vs. IoT’s ±5%), but still beat the old system’s "guessing."  
- **Speed**: Daily updates instead of real-time – mitigated by emphasizing *trends* over live counts.  
- **Buy-In**: Framed the dashboard as a "temporary upgrade" to secure funding for future IoT projects.  


### **Why This Works for Non-IOT Teams**  
1. **Leverages existing data** (tickets, permits) instead of new hardware.  
2. **Excel skills** bridge the gap between analog processes and digital analytics.  
3. **Power BI** creates urgency with visuals, even if the data is imperfect.  

Would you like to dig deeper into the SQL logic or Power BI DAX formulas?