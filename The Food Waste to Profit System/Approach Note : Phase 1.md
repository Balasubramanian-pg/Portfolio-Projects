---

# **Approach Note: Phase 1 – Waste Audit & Root Cause Analysis**  
**Project**: FreshPlate Food Waste Reduction Initiative  
**Owner**: [Intern Name] | **Date**: [Insert Date] | **Tools**: Excel  

---

## **Objective**  
Identify patterns, root causes, and cost-saving opportunities in FreshPlate’s food waste data across 35 locations to reduce waste by 35% in 8 months.  

---

## **Scope**  
- **Data**: 6 months of historical waste logs (200K+ rows) from POS systems and manual entries.  
- **Focus Areas**:  
  - Top wasteful items by cost and volume.  
  - Supplier performance (spoilage rates).  
  - Temporal trends (peak waste days/meals).  
- **Exclusions**: Beverage waste (handled separately by the bar team).  

---

## **Data Sources**  
1. **Waste Logs**: Raw CSV exports from restaurant POS systems.  
   - Columns: `Date, Location, Food_Category, Item, Waste_Reason, Quantity_kg, Cost, Supplier`.  
2. **Supplier Master List**: Excel sheet with supplier reliability ratings.  
3. **Menu Sales Data**: To cross-reference waste with low-selling dishes.  

---

## **Methodology**  

### **Step 1: Data Cleaning & Standardization**  
**Issues Identified**:  
- Inconsistent date formats (MM/DD/YYYY vs. DD-MM-YYYY).  
- Missing `Waste_Reason` (15% of entries) and `Supplier` (10% of entries).  
- Outliers (e.g., 500kg of "beef waste" due to typo).  

**Actions**:  
1. **Standardize Dates**:  
   - Use `TEXT-TO-COLUMNS` to split malformed dates.  
   - Apply `DATEVALUE` to convert text to Excel date format.  
2. **Fill Missing Data**:  
   - Use `VLOOKUP` to populate `Supplier` names from the master list.  
   - Flag rows with missing `Waste_Reason` for manual review.  
3. **Remove Outliers**:  
   - Filter entries where `Quantity_kg > 50` and validate with location managers.  

---

### **Step 2: Exploratory Analysis**  
**Key Excel Functions & Tools**:  
- **Pivot Tables**: Aggregate waste by item, location, and reason.  
- **Conditional Formatting**: Highlight high-cost waste items in red.  
- **SUMIFS/AVERAGEIFS**: Compare spoilage rates by supplier.  

**Sample Analysis**:  
| Food_Category | Total_Waste_kg | Total_Cost | Primary_Waste_Reason |  
|---------------|----------------|------------|----------------------|  
| Bakery        | 1,200          | $4,200     | Overproduction (62%) |  
| Produce       | 980            | $3,800     | Spoilage (48%)       |  

**Visualizations**:  
1. **Waste by Day of Week**: Line chart showing bakery waste spikes on Sundays.  
2. **Supplier Comparison**: Bar chart comparing spoilage rates (Supplier B: 22% vs. Supplier A: 9%).  

---

### **Step 3: Root Cause Identification**  
**Guiding Questions**:  
1. Why does "sourdough bread" account for 18% of bakery waste?  
   - *Finding*: Overproduced on weekends due to outdated demand forecasts.  
2. Why does Supplier B have higher spoilage rates?  
   - *Finding*: Deliveries occur 2 days later than Supplier A.  

**Prioritization Matrix**:  
| Issue                  | Cost Impact | Ease of Fix |  
|------------------------|-------------|-------------|  
| Weekend bakery overproduction | High       | Medium      |  
| Supplier B delays      | High        | High        |  
| Inconsistent portion sizes | Medium    | Low         |  

---

## **Deliverables**  
1. **Cleaned Dataset**:  
   - Standardized dates, filled suppliers, outliers removed.  
2. **Pivot Table Report**:  
   - Top 10 wasteful items by cost.  
   - Waste reason breakdown by category.  
3. **Visual Summary**:  
   - Excel charts embedded in a 1-pager for stakeholders.  
4. **Root Cause Summary**:  
   - 3-5 actionable insights (e.g., "Renegotiate Supplier B contracts").  

---

## **Timeline**  
| Task                  | Duration | Owner       |  
|-----------------------|----------|-------------|  
| Data Cleaning         | 3 days   | Intern      |  
| Pivot Table Analysis  | 2 days   | Intern      |  
| Root Cause Workshop   | 1 day    | Intern + Manager |  
| Final Report          | 1 day    | Intern      |  

---

## **Risks & Mitigation**  
| Risk                          | Mitigation |  
|-------------------------------|------------|  
| Incomplete data for 4 locations | Exclude and note in report |  
| Stakeholder pushback on findings | Prep backup data samples |  

---

## **Next Steps**  
1. Present findings to the ops team for buy-in.  
2. Begin Phase 2: Build SQL-driven redistribution logic for surplus food.  

---

**Approved By**: [Manager Name]  
**Signature**: ___________________________  
**Date**: _______________________________  

--- 

This note balances technical rigor with stakeholder clarity, ensuring the intern stays focused on high-impact actions while navigating real-world data chaos.
