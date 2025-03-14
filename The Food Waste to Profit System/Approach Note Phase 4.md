---

# **Approach Note: Phase 4 – Circular Economy Dashboard Development**  
**Project**: FreshPlate Food Waste Reduction Initiative  
**Owner**: [Intern Name] | **Date**: [Insert Date] | **Tools**: Power BI, SQL, Excel  

---

## **Objective**  
Develop an interactive Power BI dashboard to consolidate waste reduction, redistribution, and revenue metrics, enabling stakeholders to monitor progress toward circular economy goals and drive data-driven decisions.  

---

## **Scope**  
- **Data Integration**: Aggregate data from Phases 1-3 (waste audits, donations, upcycled revenue).  
- **Key Metrics**:  
  - **Operational**: Total waste reduced (kg), donation fulfillment rate, revenue from upcycled products.  
  - **Environmental**: CO2 emissions avoided, water saved, landfill diversion.  
  - **Financial**: Cost savings vs. disposal costs, ROI of upcycled products.  
- **Exclusions**: Real-time IoT sensor integration (future phase).  

---

## **Data Sources**  
1. **SQL Databases**:  
   - `Waste_Audit` (Phase 1): Daily waste logs by location/category.  
   - `Donations` (Phase 2): Nonprofit pickup records.  
   - `Revenue` (Phase 3): Upcycled product sales and bio-energy contracts.  
2. **Excel Files**:  
   - Environmental conversion factors (e.g., 1kg food waste = 2.5kg CO2 avoided).  
   - Supplier and nonprofit metadata.  

---

## **Methodology**  

### **Step 1: Data Model Design**  
**Power BI Dataflows**:  
1. **Connect to SQL**: Direct query for real-time donation and inventory data.  
2. **Import Excel**: Static tables for conversion factors and KPIs.  
3. **Relationships**: Link tables via `Location`, `Date`, and `Product_ID`.  

**Key DAX Measures**:  
```  
CO2 Avoided = SUM(Waste_Audit[Quantity_kg]) * RELATED(Conversion_Factors[CO2_per_kg])  
Revenue per kg = DIVIDE(SUM(Revenue[Sales]), SUM(Upcycled[Input_kg]))  
```  

---

### **Step 2: Dashboard Design**  
**Home Page (Overview)**:  
- **Summary Cards**: Total waste reduced, donations fulfilled, revenue generated.  
- **Trend Lines**: Monthly progress vs. targets (e.g., "35% waste reduction by Q2").  
- **Map**: Waste hotspots and donation distribution by location.  

**Drill-Down Pages**:  
1. **Waste Analysis**:  
   - Top 5 wasteful items by cost.  
   - Supplier spoilage rates (bar chart).  
2. **Redistribution**:  
   - Nonprofit utilization rates (actual vs. capacity).  
   - Unclaimed surplus alerts (table with expiry dates).  
3. **Revenue Engine**:  
   - Upcycled product performance (revenue vs. COGS).  
   - Bio-energy contribution (biogas/compost revenue).  
4. **Environmental Impact**:  
   - CO2, water, and landfill savings (vs. industry benchmarks).  

**Mobile View**:  
- Simplified layout with key metrics and filters.  

---

### **Step 3: Automation & Security**  
**Automation**:  
- Schedule daily SQL data refresh via **Power BI Gateway**.  
- Use **Power Automate** to email weekly PDF reports to stakeholders.  

**Security**:  
- Role-based access (e.g., managers see financials, nonprofits view donation data).  
- Row-level security in SQL to restrict location-specific data.  

---

## **Deliverables**  
1. **Power BI File**:  
   - `FreshPlate_Circular_Dashboard.pbix` with drillable visuals and tooltips.  
2. **Data Validation Report**:  
   - Cross-check dashboard metrics against source systems (e.g., SQL vs. Excel).  
3. **User Guide**:  
   - 5-page manual: "How to navigate filters, export data, and set alerts."  

---

## **Timeline**  
| Task                          | Duration | Owner       |  
|-------------------------------|----------|-------------|  
| Data Model Build              | 5 days   | Intern      |  
| Dashboard UI/UX Design        | 5 days   | Intern      |  
| Security & Automation Setup   | 3 days   | Intern      |  
| UAT & Stakeholder Training    | 2 days   | Intern + IT |  

---

## **Risks & Mitigation**  
| Risk                                  | Mitigation                                  |  
|---------------------------------------|---------------------------------------------|  
| Data latency from SQL                 | Use import mode (not direct query) for large tables. |  
| Conflicting environmental metrics     | Align conversion factors with industry standards (e.g., EPA). |  
| Stakeholder resistance to new tools   | Host a 30-minute training workshop.        |  

---

## **Next Steps**  
1. Pilot the dashboard with 5 power users for feedback.  
2. Integrate IoT sensor data (Phase 5) for real-time waste tracking.  
3. Develop executive summary slides for board presentations.  

---

**Approved By**: [Manager Name]  
**Signature**: ___________________________  
**Date**: _______________________________  

---

### **Appendix: Mock Dashboard Wireframe**  
![Dashboard Wireframe](https://i.imgur.com/AbC1234.png)  
*Visual includes: (1) Summary cards, (2) Waste trends, (3) Donation map, (4) Revenue vs. targets bar chart.*  

---

This note ensures the intern balances technical rigor with stakeholder needs, delivering a dashboard that turns data into actionable insights for a circular economy.
