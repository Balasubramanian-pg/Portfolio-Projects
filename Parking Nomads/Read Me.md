
---
# **Hyper-Realistic Case Study: Urban Parking Optimization System**  
**Tools**: Python, SQL, GIS (ArcGIS), Power BI, IoT | **Duration**: 14-week Internship  
**Business Context**: *MetroCity* (population 2.4M) loses $28M/year to parking inefficiencies: 22% of downtown traffic is drivers circling for parking, while 40% of off-peak garage spaces sit empty. Their goals:  
1. Reduce parking search time by 35% in 6 months.  
2. Increase parking revenue by 20% through dynamic pricing.  
3. Cut downtown CO2 emissions by 15% via reduced idling.  

---

## **Problem Statement**  
*MetroCity*’s legacy parking system relies on coin meters and static signs. Drivers waste 18 minutes/search on average, while prime spots underprice event-day demand by 300%.  

---

## **Your Role as an Intern**  
Design a data-driven parking system balancing driver convenience, city revenue, and sustainability.  

---

### **Phase 1: IoT Sensor Deployment & Data Chaos**  
**Objective**: Capture real-time parking availability across 10,000 spaces.  

#### **Challenges**  
1. **Sensor Failures**: 12% of IoT devices malfunctioned in initial rollout (fixed with redundant ultrasonic + camera verification).  
2. **Legacy Integration**: 30% of garages used 1990s-era systems requiring manual data entry (built Python OCR scripts for analog gauge photos).  

#### **Code Snippet** (Python):  
```python  
# OCR for legacy garage counters  
import pytesseract  
from PIL import Image  

def read_analog_gauge(image_path):  
    img = Image.open(image_path)  
    text = pytesseract.image_to_string(img, config='--psm 6')  
    return int(text) if text.isdigit() else None  

# Usage: Nightly scrape of garage CCTV  
available_spots = read_analog_gauge('garage3.jpg')  
```  

**Deliverable**:  
- Unified parking API with 95% uptime across street/garage spots.  

---

### **Phase 2: Predictive Modeling & Edge Cases**  
**Objective**: Forecast demand for World Series games, protests, and flash floods.  

#### **Model Development**  
1. **Algorithm**: Prophet time-series + computer vision (event crowd detection).  
2. **Features**:  
   - `Event_Attendance` (Ticketmaster API + stadium camera headcounts).  
   - `Weather_Impact` (NEXRAD rainfall radar integration).  
3. **Validation**:  
   - Predicted 97% occupancy during NBA finals (actual: 94%).  
   - False alarm: Mistook marathon runners for parking surge (added sport_gear CV filter).  

#### **Code Snippet** (Python):  
```python  
from fbprophet import Prophet  

def forecast_event_demand(event_date, attendee_count):  
    model = Prophet(holidays=event_holidays_df)  
    model.fit(historical_demand_df)  
    future = model.make_future_dataframe(periods=24, freq='H')  
    future['attendees'] = attendee_count  
    return model.predict(future)  

# World Series Game 7: 45K attendees  
forecast = forecast_event_demand('2023-10-30', 45000)  
```  

---

### **Phase 3: Dynamic Pricing Engine**  
**Objective**: Balance accessibility and revenue without public backlash.  

#### **Strategy**  
1. **Surge Pricing**:  
   - Up to 4x base rate during events (capped by city ordinance).  
2. **Equity Rules**:  
   - Low-income zones max 1.5x surge.  
   - Free first 30 minutes for ADA spots.  

#### **SQL Implementation**:  
```sql  
UPDATE parking_rates  
SET price =   
    CASE  
        WHEN demand_score > 0.8 AND income_tier != 'Low' THEN base_price * 3.5  
        WHEN demand_score > 0.8 THEN base_price * 1.5  
        WHEN demand_score < 0.3 THEN base_price * 0.7  
    END  
WHERE effective_date = CURDATE();  
```  

**Backlash Mitigation**:  
- Partnered with Uber to offer "Park & Ride" discounts during 4x surges.  

---

### **Phase 4: Driver App & Behavioral Nudges**  
**Objective**: Shift behavior via real-time incentives.  

#### **Mobile App Features**  
1. **Personalized Routing**:  
   - "Your downtown meeting at 2 PM – reserve garage spot for $12 (vs $35 drive-around cost)."  
2. **Gamification**:  
   - "Earn 50 points parking in underutilized zones – redeem for free EV charging."  

#### **A/B Test Results**:  
| Nudge Type           | Adoption | Search Time Reduction |  
|----------------------|----------|-----------------------|  
| Reservation Discount | 28%      | 41%                   |  
| Eco Points           | 12%      | 18%                   |  

---

### **Phase 5: Stakeholder Dashboards**  
**Objective**: Align city staff, businesses, and residents.  

#### **Power BI Dashboard**  
1. **Mayor View**:  
   - CO2 reduction vs. revenue gains.  
   - Public sentiment analysis (Reddit/Twitter).  
2. **Parking Enforcement**:  
   - Predictive illegal parking hotspots.  
3. **Business View**:  
   - Foot traffic correlation with garage availability.  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Avg. Search Time     | 18 min  | 11 min (-39%)     |  
| Parking Revenue      | $42M    | $51M (+21%)       |  
| Downtown Emissions   | 12K tons| 10.2K (-15%)      |  

---

## **Real-World Challenges**  
1. **Sensor Vandalism**: 5% of street sensors stolen (replaced with tamper-proof units).  
2. **PR Crisis**: "Surge pricing during parade" headlines – added charity event exemptions.  
3. **Data Bias**: Model underpredicted demand in gentrifying areas (added Zillow home price data).  

---

## **Deliverables**  
1. **Technical**:  
   - Python demand models + OCR pipeline.  
   - IoT anomaly detection system (Grafana).  
2. **Business**:  
   - Driver app prototype (Figma).  
   - Stakeholder playbook: "Crisis Communication for Pricing Changes."  

---

## **Executive Summary**  
*By treating parking as perishable inventory, MetroCity turned a congestion nightmare into a $9M revenue stream while making streets cleaner and quieter. The intern’s work showcases how cities can balance tech innovation with social equity.*  

---

This case study immerses the intern in the messy reality of smart cities – technical debt, public backlash, and sensor gremlins – while delivering measurable impact through relentless iteration.
