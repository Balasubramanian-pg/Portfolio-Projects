# **Data Aggregation & Cleaning**  
**Project**: The Transit Gap - Between-Stops Economy Analyzer  
**Objective**: Establish a clean, structured dataset integrating transit, business, and foot traffic data to identify high-potential transit gaps.  

---

## **Scope of Work**  
Phase 1 focuses on collecting, cleaning, and integrating diverse data sources to form a reliable foundation for spatial and economic analysis. The primary tasks include:  
- **Geocoding & Validating Transit Data**  
- **Cleaning & Standardizing Business Registry Data**  
- **Processing Foot Traffic Heatmaps**  
- **Building a Centralized Data Repository**  

---

## **Key Challenges & Mitigation Strategies**  

### **1. Missing Coordinates in Transit Data (12% of stops)**  
- **Challenge**: Some subway and bus stop locations lack GPS coordinates, making spatial analysis inaccurate.  
- **Approach**:  
  - Use Python’s **Geopy** library with OpenStreetMap’s **Nominatim API** to geocode missing locations.  
  - Cross-validate with existing city transit maps and manual corrections.  

**Implementation:**  
```python  
from geopy.geocoders import Nominatim  
import pandas as pd  

def geocode_stops(df):  
    geolocator = Nominatim(user_agent="metro_transit")  
    for index, row in df[df['latitude'].isna()].iterrows():  
        location = geolocator.geocode(row['Address'])  
        if location:  
            df.at[index, 'latitude'] = location.latitude  
            df.at[index, 'longitude'] = location.longitude  
    return df  
```  
- **Deliverable**: A transit dataset with **98%+ geolocation accuracy**.  

---

### **2. Inaccurate Business Addresses (20% Geocode Failure Rate)**  
- **Challenge**: Business registry data has inconsistencies, causing location mismatches.  
- **Approach**:  
  - Use **SQL fuzzy matching** to clean and standardize address formats.  
  - Implement **NAICS code corrections** for business categories.  

**Implementation:**  
```sql  
UPDATE businesses  
SET NAICS_Code = CASE  
    WHEN Business_Name LIKE '%Cafe%' THEN 722511  
    WHEN Business_Name LIKE '%Pharmacy%' THEN 446110  
END  
WHERE NAICS_Code IS NULL;  
```  
- **Deliverable**: A cleaned business registry dataset, mapped to correct geographic zones.  

---

### **3. Integrating Foot Traffic Heatmaps (JSON Format)**  
- **Challenge**: Mobile location data is noisy and requires filtering.  
- **Approach**:  
  - Apply **Python Pandas** for JSON parsing and data normalization.  
  - Filter only data points within **500m of transit stops**.  

**Implementation:**  
```python  
import json  

def parse_foot_traffic(file):  
    with open(file, 'r') as f:  
        data = json.load(f)  
    df = pd.json_normalize(data, 'location_pings')  
    df = df[df['distance_to_stop'] <= 500]  
    return df  
```  
- **Deliverable**: A structured foot traffic dataset aligned with transit locations.  

---

### **4. Creating a Unified Data Repository**  
- **Challenge**: Multiple datasets in different formats (CSV, JSON, SQL).  
- **Approach**:  
  - Store cleaned datasets in a **PostgreSQL** database with **spatial indexing**.  
  - Use **QGIS** to visualize data layers.  

**Deliverable**:  
✅ Cleaned and integrated transit, business, and foot traffic datasets.  
✅ A **data dictionary** documenting transformations and assumptions.  

---

## **Next Steps**  
🚀 Once Phase 1 is complete, we will move to **Phase 2: Spatial Gap Analysis**, where we identify high-potential transit gaps based on foot traffic and commercial density.  

---

Would you like any refinements or additional details?
