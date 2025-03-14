
---

# **Approach Note: Phase 2 – Redistribution Engine Development**  
**Project**: FreshPlate Food Waste Reduction Initiative  
**Owner**: [Intern Name] | **Date**: [Insert Date] | **Tools**: SQL, Power BI  

---

## **Objective**  
Design a scalable SQL-driven system to automate surplus food matching with nonprofits, ensuring 40% of FreshPlate’s excess inventory is donated or recycled within 8 months.  

---

## **Scope**  
- **Data**:  
  - Real-time inventory tables (item, quantity, expiry date, location).  
  - Nonprofit profiles (needs, pickup capacity, cold storage availability).  
- **Focus Areas**:  
  - Daily matching of perishable/non-perishable surplus to nonprofits.  
  - Weekly donation performance tracking.  
  - Integration with Power BI for real-time reporting.  
- **Exclusions**: Handling logistics (e.g., transportation coordination).  

---

## **Data Sources**  
1. **Inventory Table**: Updated hourly from POS systems.  
   - Columns: `item_id, item_name, category, quantity_kg, expiry_date, location`.  
2. **Nonprofits Database**:  
   - Columns: `org_id, org_name, needs, pickup_capacity_kg, refrigeration_required`.  
3. **Donation Logs**: Historical data on past donations (success/failure reasons).  

---

## **Methodology**  

### **Step 1: Database Design & Optimization**  
**Schema**:  
```sql  
-- Inventory Table  
CREATE TABLE inventory (  
  item_id INT PRIMARY KEY,  
  item_name VARCHAR(50) NOT NULL,  
  category VARCHAR(20) CHECK (category IN ('Perishable', 'Non-Perishable')),  
  quantity_kg DECIMAL(10,2) NOT NULL,  
  expiry_date DATE NOT NULL,  
  location VARCHAR(20) NOT NULL  
);  

-- Nonprofits Table  
CREATE TABLE nonprofits (  
  org_id INT PRIMARY KEY,  
  org_name VARCHAR(50) NOT NULL,  
  needs VARCHAR(100),  -- e.g., 'Perishable, Dairy, Frozen'  
  pickup_capacity_kg DECIMAL(10,2) NOT NULL,  
  refrigeration_required BOOLEAN DEFAULT FALSE  
);  
```  

**Optimizations**:  
- Add indexes on `expiry_date` and `location` for faster querying.  
- Use `CHECK constraints` to enforce category validity.  

---

### **Step 2: Surplus Matching Logic**  
**Key SQL Queries**:  
1. **Daily Perishable Matching**:  
   ```sql  
   -- Match items expiring in 24 hours with nonprofits needing perishables  
   SELECT  
     i.item_name,  
     i.quantity_kg,  
     i.location,  
     n.org_name,  
     n.pickup_capacity_kg  
   FROM inventory i  
   JOIN nonprofits n  
     ON i.category = 'Perishable'  
     AND n.needs LIKE '%Perishable%'  
     AND n.refrigeration_required = TRUE  
   WHERE i.expiry_date = CURDATE() + INTERVAL 1 DAY  
     AND i.quantity_kg <= n.pickup_capacity_kg  
   ORDER BY i.location;  
   ```  

2. **Weekly Capacity Utilization**:  
   ```sql  
   -- Track how much of a nonprofit’s capacity is used  
   SELECT  
     org_id,  
     org_name,  
     SUM(quantity_kg) AS total_donated,  
     (SUM(quantity_kg) / pickup_capacity_kg) * 100 AS utilization_rate  
   FROM donations  
   GROUP BY org_id;  
   ```  

**Edge Cases**:  
- If no nonprofit claims an item, flag it for recycling partners.  
- Split large surpluses (>100kg) across multiple nonprofits.  

---

### **Step 3: Integration with Power BI**  
**Automated Workflow**:  
1. Use **SQL Server Agent** to run matching queries daily at 8 AM.  
2. Export results to a CSV, then load into Power BI.  
3. Build a **Donation Dashboard** with:  
   - Map of nonprofits served by location.  
   - Utilization rates (actual vs. capacity).  
   - Alerts for unclaimed surpluses (e.g., "50kg unclaimed in Chicago").  

**Sample DAX Measure**:  
```  
Donation Success Rate =   
DIVIDE(  
    SUM(donations[quantity_kg]),  
    SUM(inventory[quantity_kg]),  
    0  
)  
```  

---

## **Deliverables**  
1. **SQL Scripts**:  
   - `daily_matching.sql`: Automated surplus-to-nonprofit matching.  
   - `weekly_utilization_report.sql`: Capacity tracking.  
2. **Power BI Dashboard**:  
   - Real-time donation tracking with drilldowns.  
   - Exportable PDF reports for stakeholder meetings.  
3. **Data Validation Checklist**:  
   - Steps to audit `pickup_capacity_kg` vs. actual pickups.  
   - Flagging expired donations in transit (e.g., "Spinach expired mid-transit").  

---

## **Timeline**  
| Task                          | Duration | Owner       |  
|-------------------------------|----------|-------------|  
| Database Schema Finalization  | 2 days   | Intern      |  
| Query Development & Testing   | 4 days   | Intern      |  
| Power BI Dashboard Build      | 3 days   | Intern      |  
| Stakeholder Review            | 1 day    | Intern + Manager |  

---

## **Risks & Mitigation**  
| Risk                                  | Mitigation                                  |  
|---------------------------------------|---------------------------------------------|  
| Nonprofits reject last-minute surpluses | Add a backup recycler partner list.        |  
| Incorrect expiry dates in inventory   | Validate dates against supplier invoices.  |  
| Overloaded SQL server performance     | Schedule resource-heavy queries off-peak.  |  

---

## **Next Steps**  
1. Pilot the system in 5 locations for 2 weeks.  
2. Train restaurant managers on updating inventory tables.  
3. Transition to Phase 3: Profit conversion modeling for upcycled products.  

---

**Approved By**: [Manager Name]  
**Signature**: ___________________________  
**Date**: _______________________________  

---

### **Appendix: Real-World Testing Scenario**  
**Mock Data Challenge**:  
- **Problem**: A nonprofit’s `pickup_capacity_kg` is listed as 100kg, but they only collect 70kg.  
- **Intern Task**:  
  1. Use SQL to identify mismatches:  
  ```sql  
  SELECT *  
  FROM donations  
  WHERE org_id = 203  
    AND quantity_kg > pickup_capacity_kg;  
  ```  
  2. Update the matching logic to cap donations at 80% of capacity.  

---

This note equips the intern to tackle technical and operational challenges, ensuring the redistribution engine is both data-driven and adaptable to real-world constraints.
