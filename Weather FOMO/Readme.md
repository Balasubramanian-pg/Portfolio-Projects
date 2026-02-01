
---

# **Hyper-Realistic Case Study: Weather FOMO - Lost Revenue Weather Tracker**  
**Tools**: Python, SQL, Power BI, Excel | **Duration**: 10-week Internship  
**Business Context**: *SunnyDays Resorts*, a chain of 15 beachfront properties, loses 12% of annual revenue ($8M) due to unplanned weather disruptions (rain, hurricanes). They need to:  
1. Predict weather-driven cancellations with 85% accuracy.  
2. Deploy real-time mitigation strategies (e.g., dynamic pricing, promotions).  
3. Reduce weather-related revenue loss by 30% in 6 months.  

---

## **Problem Statement**  
*SunnyDays* struggles with last-minute cancellations during rainy weekends and misses upsell opportunities during sunny spikes. Manual weather monitoring is reactive and error-prone.  

---

## **Your Role as an Intern**  
Build a weather-revenue correlation model, design a real-time alert system, and create mitigation playbooks.  

---

### **Phase 1: Historical Weather-Revenue Analysis**  
**Objective**: Correlate 5 years of weather data with booking/revenue trends.  

#### **Data Sources**  
1. **Resort Data** (SQL):  
   - `Booking_ID, Check-in_Date, Revenue, Cancellation_Reason`.  
   - Issues: 20% of cancellations lack reasons; inconsistent date formats.  
2. **Weather API** (Python):  
   - Historical hourly data (temperature, precipitation, wind) for each resort.  
3. **Event Calendar** (Excel):  
   - Local festivals, marathons, and holidays affecting demand.  

#### **Tasks**  
1. **Clean Data** (Python):  
   ```python  
   def fix_cancellations(df):  
       # Impute missing cancellation reasons using weather  
       df.loc[(df['Cancellation_Reason'].isna()) & (df['Precipitation'] > 10), 'Cancellation_Reason'] = "Weather"  
       return df  

   # Merge weather and booking data  
   merged_data = pd.merge(bookings, weather, on=['Resort_ID', 'Date'])  
   ```  

2. **Identify Key Drivers** (Excel):  
   - Pivot table showing 63% of cancellations occur when rainfall > 0.5" on check-in day.  
   - Scatterplot revealing 22% revenue spike when temperature is 75-80°F.  

#### **Deliverable**:  
- Excel report: "Rainfall > 0.5" reduces occupancy by 40% at Miami resorts."  

---

### **Phase 2: Predictive Modeling**  
**Objective**: Forecast cancellations and demand surges.  

#### **Model Selection**  
1. **Cancellation Risk** (Logistic Regression):  
   - Features: 3-day rainfall forecast, day-of-week, resort capacity.  
   - Outcome: Probability of cancellation (AUC-ROC: 0.89).  
2. **Revenue Surge** (Time-Series LSTM):  
   - Predict 15% demand spike when sunny weekends coincide with festivals.  

#### **Code Snippet** (Python):  
```python  
from sklearn.linear_model import LogisticRegression  

# Train cancellation model  
X = df[['Rainfall_Forecast', 'Day_of_Week', 'Capacity']]  
y = df['Cancelled']  
model = LogisticRegression()  
model.fit(X, y)  

# Predict next weekend's risk  
forecast_data = [[2.3, 6, 80]]  # 2.3" rain, Saturday, 80% capacity  
risk = model.predict_proba(forecast_data)[0][1]  # Output: 72% risk  
```  

#### **Validation Challenge**:  
- Hurricane false alarms caused over-pessimistic predictions (fixed by adding "forecast certainty" weights).  

---

### **Phase 3: Real-Time Alert System**  
**Objective**: Notify managers of risks/opportunities 72 hours in advance.  

#### **Power BI Dashboard**:  
1. **Risk Alerts**:  
   - Red/Amber/Green flags for cancellations.  
   - "Miami: 70% cancellation risk Saturday – offer 20% discount to retain bookings."  
2. **Upsell Opportunities**:  
   - "San Diego: Sunny + Music Festival – upgrade poolside cabanas to Premium."  

#### **Integration**:  
- Auto-send alerts via Microsoft Teams using Power Automate.  

---

### **Phase 4: Mitigation Playbooks**  
**Objective**: Turn insights into action.  

#### **Strategies Tested**  
1. **Dynamic Pricing**:  
   - Offer 15% discount if guests keep bookings during high-risk periods.  
   - **Result**: Reduced cancellations by 25% in pilot resorts.  
2. **Weather-Driven Promotions**:  
   - "Rainy Day Spa Package" increased ancillary revenue by 18%.  

#### **Financial Model** (Excel):  
| Strategy              | Cost      | Revenue Impact | ROI  |  
|-----------------------|-----------|----------------|------|  
| Dynamic Pricing       | $12K/resort | $12K/resort   | 8.3x |  
| Spa Promotions        | $5K/resort | $19K/resort   | 3.8x |  

---

## **Business Impact**  
| Metric               | Before   | After (6 Months) |  
|----------------------|----------|-------------------|  
| Weather Cancellations| 22%      | 15% (-32%)        |  
| Ancillary Revenue    | $1.2M/mo | $1.6M/mo (+33%)   |  
| Guest Satisfaction   | 4.1/5    | 4.6/5             |  

---

## **Real-World Challenges**  
1. **Data Bias**:  
   - Rainy-day spa promotions failed in family resorts (fixed by segmenting by guest type).  
2. **Stakeholder Pushback**:  
   - Managers resisted dynamic pricing (resolved with A/B test results).  
3. **API Limitations**:  
   - Weather API rate limits caused gaps (switched to AWS Weather).  

---

## **Deliverables**  
1. **Technical**:  
   - Python scripts for predictive models.  
   - SQL queries linking bookings to weather.  
2. **Business**:  
   - Power BI dashboard with real-time alerts.  
   - Excel playbook: "5 Weather Mitigation Strategies with ROI."  
   - Stakeholder training video (Loom).  

---

## **Executive Summary**  
*By treating weather as a lever, not a liability, SunnyDays Resorts turned a $8M problem into a $2.4M opportunity. The intern’s work showcases how data transforms "bad weather" into "upsell weather."*  

---

This case study simulates real-world chaos, requiring the intern to blend meteorology, data science, and hospitality ops under tight deadlines.
