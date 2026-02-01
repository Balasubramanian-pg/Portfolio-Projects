## The Transit Gap - Between-Stops Economy Analyzer

**Tools**: Python, SQL, GIS (QGIS/ArcGIS), Power BI | **Duration**: 12-week Internship  
**Business Context**: *MetroCity Transit Authority* seeks to boost ridership and local economic activity by targeting underutilized zones between subway stops. Despite 1.2M daily riders, 30% of commuters bypass "dead zones" with no amenities, costing the city $15M/year in lost revenue.  

---

## **Problem Statement**  
*MetroCity* needs to:  
1. **Identify 10 high-potential transit gaps** with low commercial activity but high foot traffic.  
2. **Recommend 3-5 interventions** (e.g., pop-up retail, micro-mobility hubs) to activate these zones.  
3. **Increase ridership by 8%** in targeted areas within 12 months.  

---

## **Your Role as an Intern**  
Analyze spatial, transit, and economic data to prioritize gaps and model interventions.  

---

### **Phase 1: Data Aggregation & Cleaning**  
**Objective**: Merge messy transit, business, and foot traffic data.  

#### **Data Sources**  
1. **Transit Data** (GTFS Feeds, SQL):  
   - `stop_id, latitude, longitude, daily_ridership`.  
   - Issues: Missing coordinates for 12% of bus stops.  
2. **Business Registry** (CSV, 50K+ rows):  
   - `Business_Name, NAICS_Code, Revenue, Address`.  
   - Challenges: 20% of addresses geocode inaccurately.  
3. **Mobile Location Data** (JSON):  
   - Anonymous foot traffic heatmaps (cell tower pings).  

#### **Tasks**  
1. **Geocode Missing Stops** (Python):  
   ```python  
   from geopy.geocoders import Nominatim  

   def geocode_stops(df):  
       geolocator = Nominatim(user_agent="metro_transit")  
       for index, row in df[df['latitude'].isna()].iterrows():  
           location = geolocator.geocode(row['Address'])  
           df.at[index, 'latitude'] = location.latitude  
           df.at[index, 'longitude'] = location.longitude  
       return df  
   ```  

2. **Clean Business Data** (SQL):  
   ```sql  
   -- Fix NAICS code mismatches (e.g., "Food Services" = 722511)  
   UPDATE businesses  
   SET NAICS_Code = CASE  
       WHEN Business_Name LIKE '%Cafe%' THEN 722511  
       WHEN Business_Name LIKE '%Pharmacy%' THEN 446110  
   END  
   WHERE NAICS_Code IS NULL;  
   ```  

**Deliverable**:  
- Cleaned geospatial dataset with 98% accuracy.  
- Data dictionary explaining NAICS code mappings.  

---

### **Phase 2: Spatial Gap Analysis**  
**Objective**: Find zones with high ridership but low amenities.  

#### **Methodology**  
1. **Buffer Analysis** (QGIS):  
   - Create 500m buffers around subway stops.  
   - Identify overlapping buffers as "high foot traffic corridors."  
2. **Commercial Density Scoring**:  
   ```python  
   # Calculate businesses per sq km in buffer zones  
   def density_score(buffers, businesses_gdf):  
       buffers['business_count'] = buffers.apply(  
           lambda row: businesses_gdf.within(row.geometry).sum(), axis=1  
       )  
       buffers['density'] = buffers['business_count'] / (buffers.area / 1e6)  
       return buffers  
   ```  
   - Gaps defined as zones with density < 10 businesses/sq km but foot traffic > 1K/day.  

#### **Deliverable**:  
- Interactive QGIS map highlighting 15 priority gaps.  
- Tableau dashboard showing density vs. foot traffic scatterplots.  

---

### **Phase 3: Intervention Modeling**  
**Objective**: Simulate ROI for pop-ups, micro-hubs, and new stops.  

#### **Intervention Ideas**  
1. **Pop-Up Retail Pods**: Modular kiosks selling coffee/snacks.  
2. **E-Bike Stations**: Last-mile connectivity to nearby offices.  
3. **Night Market Pilot**: Activate gaps after 6 PM.  

#### **Financial Model** (Excel):  
| Metric                | Pop-Up Pod       | E-Bike Hub      |  
|-----------------------|------------------|-----------------|  
| Setup Cost            | $25,000         | $50,000         |  
| Monthly Revenue       | $8,000          | $12,000         |  
| Payback Period        | 3.1 months      | 4.2 months      |  

**Sensitivity Analysis**:  
- If foot traffic drops 20%, pop-up pod revenue falls to $6,400/month.  

#### **Deliverable**:  
- Excel model with scenario planning (optimistic/pessimistic forecasts).  

---

### **Phase 4: Stakeholder Playbook & Dashboard**  
**Objective**: Empower MetroCity to implement solutions.  

#### **Power BI Dashboard**  
- **Home Tab**:  
  - Top 5 gaps ranked by potential ROI.  
  - Before/after heatmaps of foot traffic.  
- **Intervention Tracker**:  
  - Real-time revenue vs. projections.  
  - Break-even countdown: "E-Bike Hub needs $18K more to break even."  

#### **Playbook Components**  
1. **Zoning Cheat Sheet**: Streamlined permits for pop-ups in Gap #3.  
2. **Partner Pitch Deck**: Pre-designed slides to attract retailers.  

---

## **Business Impact**  
| Metric               | Before  | After (12 Months) |  
|----------------------|---------|--------------------|  
| Ridership in Gaps    | 150K/mo | 195K/mo (+30%)    |  
| New Businesses       | 0       | 42                 |  
| Commuter Satisfaction| 58%     | 82%                |  

---

## **Real-World Challenges**  
1. **Data Bias**: Mobile data underrepresented low-income neighborhoods (adjusted with on-ground surveys).  
2. **Stakeholder Resistance**: Local businesses feared pop-ups would cannibalize sales (resolved with revenue-sharing agreements).  
3. **Regulatory Hurdles**: Zoning laws blocked night markets (lobbied for temporary event permits).  

---

## **Deliverables**  
1. **Technical**:  
   - Python scripts for geocoding and density scoring.  
   - QGIS project files with buffer layers.  
2. **Business**:  
   - Power BI dashboard with intervention tracking.  
   - Excel ROI models + 15-page stakeholder playbook.  

---

## **Executive Summary**  
*By transforming transit gaps into vibrant hubs, MetroCity can unlock $8M/year in new economic activity while cutting commute times by 12%. The intern’s work bridges urban planning and data science, proving that "dead zones" are goldmines in disguise.*  

---

This case study mirrors real-world complexity, requiring the intern to navigate spatial analytics, financial modeling, and stakeholder politics—all while delivering measurable impact.
