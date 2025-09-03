### **Project Scenario: "Project Phoenix" for SavoryBites Restaurant Chain**

**Company:** SavoryBites, a chain of 15 casual dining restaurants.
<br>**Current Situation:** Managers intuitively know food waste is a problem, costing money and impacting sustainability goals. 
<br>However, they have no standardized way to measure it, understand its causes, or address it systematically. Their current tools are limited to their Point-of-Sale (POS) system, Excel, and manual processes.

**Project Goal:** To reduce food waste by 25% within 12 months and identify at least one viable avenue to convert waste into a revenue stream or cost savings.

### **Phase 1: The Manual Audit & Baseline Establishment (Months 1-2)**

**Tool:** Excel
**Goal:** Move from intuition to data.

- **Action:** Introduce a simple "Waste Log" spreadsheet in every kitchen. For one full month, every time food is thrown away, staff must log:
    1. **Date & Time**
    2. **Item:** (e.g., prepped onions, day-old bread, spoiled chicken, customer plate waste)
    3. **Category:** Raw Ingredient / Prepared but Unsold / Plate Waste / Spoiled
    4. **Quantity:** (in weight - kg/lbs or volume - units)
    5. **Reason:** (e.g., over-preparation, spoilage, cosmetic, customer didn't like it)
    6. **Estimated Cost:** (from ingredient cost sheet)
- **Realistic Challenge:** Staff pushback ("this is extra work"). Solution: Train managers to lead by example, emphasize the "why," and maybe run a small incentive for the most consistent kitchen.
- **Outcome:** After one month, you have a powerful, messy Excel dataset from all 15 locations. You can now establish a baseline total waste cost.

### **Phase 2: Centralized Analysis & Insight Generation (Months 3-4)**

**Tool:** SQL (or Power Query in Excel)
**Goal:** Find the biggest sources of waste and their root causes.

- **Action:**
    1. Consolidate all restaurant Excel files into a single database.
    2. Use SQL to query this data and find key insights:
        - `SELECT Reason, SUM(Estimated_Cost) FROM waste_log GROUP BY Reason ORDER BY SUM(Estimated_Cost) DESC;`
        - `SELECT Item, SUM(Quantity) FROM waste_log WHERE Category = 'Prepared but Unsold' GROUP BY Item;` (What are we consistently making too much of?)
        - `SELECT Restaurant_ID, SUM(Estimated_Cost) FROM waste_log GROUP BY Restaurant_ID;` (Is one location an outlier? A best performer?)
        - Compare waste logs against sales data (from the POS) to see if waste for an item spikes on slow days.
- **Realistic Outcome:** You discover that **40% of waste cost comes from over-preparation of french fries and coleslaw during weekday lunches**. Another **25% comes from bread spoilage** because the delivered loaves are too large.

### **Phase 3: Implement Low-Tech Solutions & Pilot Redistribution (Months 5-8)**

**Goal:** Act on the data to reduce waste and test a redistribution channel.

- **Action 1 (Process Change):**
    - **For Fries/Slaw:** Adjust prep recipes and par-levels for weekdays vs. weekends. Implement "batch prep" throughout the lunch rush instead of pre-making everything upfront.
    - **For Bread:** Negotiate with the supplier for smaller loaves or implement a rule to freeze half the delivery upon arrival.
- **Action 2 (Redistribution Pilot - Tool: Excel/Phone):**
    - Identify 3 restaurants near local farms or animal shelters.
    - Instead of throwing away certain food scraps (vegetable peels, eggshells, old bread), staff place them in designated "farm buckets."
    - A local pig farmer agrees to pick up the buckets twice a week for free. This **saves on waste disposal costs** (tipping fees), which is an indirect revenue gain.
- **Measure:** Continue the waste log for these pilot locations to measure the impact of the changes.

### **Phase 4: Reporting, Scaling, and Premium Redistribution (Months 9-12)**

**Tool:** Power BI
**Goal:** Create a culture of accountability and explore partnerships for higher-value waste.

- **Action:**
    1. Build a **"Circular Economy Dashboard"** in Power BI that connects to the central waste database.
    2. **Dashboard includes:**
        - Key Metrics: Total waste cost (vs. last month, vs. baseline), waste by category, waste by reason.
        - A map showing which locations are participating in the farm animal program and the weight of waste diverted.
        - A leaderboard of locations based on waste reduction percentage. (Gamification!).
    3. Share this dashboard with regional managers in weekly reviews to drive accountability.
    4. **Pilot a "Non-Profit Partnership":** For one location near a homeless shelter, package unsold, safe-to-eat meals (e.g., day-old pastries, unserved soups) at the end of the night. A volunteer from the shelter picks it up. Use Power BI to track this donation (potential for tax benefits).
- **Revenue Conversion Idea:** The data shows a consistent surplus of citrus peels (from bar drinks). Partner with a local craft distillery or marmalade maker to **sell them these peels** as raw ingredients. This becomes a direct, albeit small, revenue stream.

### **Final Deliverable to Stakeholders:**

A Power BI report showcasing:

- **A 30% reduction in food waste costs,** exceeding the goal.
- **$X saved in reduced disposal fees** from the animal feed program.
- **Y tons of food diverted** from landfills.
- **A roadmap for Year 2:** Including a business case for a smaller IoT scale (e.g., smart scales for the waste bins in the top 3 locations to automate logging) and expanding the non-profit and upcycling partnerships.

This approach is realistic because it starts small, uses tools the company likely already has, proves value quickly with manual data, and uses that value to justify more sophisticated steps later. It turns a cost center into a story of efficiency, sustainability, and community engagement.
