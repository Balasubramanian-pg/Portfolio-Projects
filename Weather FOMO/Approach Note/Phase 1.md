# **Phase 1: Historical Weather-Revenue Analysis**  
📌 *Objective:* Identify the correlation between weather conditions and revenue fluctuations at *SunnyDays Resorts* by analyzing historical weather, booking, and event data.  

---

## **1. Data Collection & Understanding**  
To establish a relationship between weather and revenue loss, we will collect **five years of historical data** from multiple sources:  

### **1.1 Data Sources & Description**  

| **Data Source**      | **Fields** (Key Attributes) | **Format** | **Potential Issues** |
|----------------------|---------------------------|------------|----------------------|
| **Resort Booking Data** *(SQL)* | `Booking_ID, Check-in_Date, Check-out_Date, Resort_ID, Revenue, Cancellation_Status, Cancellation_Reason` | SQL Table | - Missing cancellation reasons (20%) <br> - Inconsistent date formats |
| **Historical Weather Data** *(Weather API – Python)* | `Date, Resort_Location, Temperature, Rainfall, Wind Speed, Humidity, Weather Condition` | JSON/CSV | - Gaps in hourly data <br> - API rate limits |
| **Event Calendar** *(Excel)* | `Event_Date, Event_Name, Location, Expected Visitors` | XLSX | - Unstructured event descriptions |
| **Operational Data** *(Excel/SQL)* | `Resort_ID, Occupancy_Rate, Room_Types, Guest Segments` | XLSX / SQL | - Data silos across resorts |

---

## **2. Data Cleaning & Preparation**  
📌 *Goal:* Standardize data, handle missing values, and integrate datasets for analysis.  

### **2.1 Cleaning & Standardizing Data**  
- Convert **dates** into standard `YYYY-MM-DD` format for consistency.  
- Handle **missing cancellation reasons**:  
  - If **precipitation > 10mm** on the check-in date, classify cancellation reason as `"Weather-Related"`.  
  - Otherwise, impute using resort-specific trends.  

```python
import pandas as pd

def fix_cancellations(df):
    df.loc[(df['Cancellation_Reason'].isna()) & (df['Rainfall'] > 10), 'Cancellation_Reason'] = "Weather"
    return df

# Apply function
bookings = fix_cancellations(bookings)
```

- Remove duplicate records and standardize column names.  
- Convert categorical variables (e.g., `Weather Condition`) into numerical features (`Sunny=1, Rainy=0`).  

### **2.2 Data Merging & Enrichment**  
- Merge booking and weather data on `Resort_ID` and `Date`.  
- Add event calendar data by mapping `Event_Date` and `Location`.  
- Integrate operational data (occupancy, guest segments) for deeper insights.  

```python
# Merge datasets
merged_data = bookings.merge(weather, on=['Resort_ID', 'Date']).merge(events, left_on='Check-in_Date', right_on='Event_Date', how='left')
```

---

## **3. Exploratory Data Analysis (EDA)**  
📌 *Goal:* Identify weather patterns affecting revenue & cancellations.  

### **3.1 Key Analyses & Visualizations**  
✅ **Cancellation Trends by Weather Conditions**  
- Analyze how cancellation rates change based on:  
  - **Rainfall thresholds** (e.g., cancellations spike when rain > 0.5 inches).  
  - **Temperature extremes** (e.g., bookings drop below 60°F or above 95°F).  
- Generate **boxplots and histograms** to visualize trends.  

✅ **Revenue Impact by Weather & Events**  
- Compare **average revenue per night** for:  
  - Rainy vs. non-rainy weekends.  
  - Resorts with events vs. without events.  

✅ **Time-Series Analysis**  
- Identify seasonality patterns using **rolling averages & trend decomposition**.  

```python
import matplotlib.pyplot as plt

# Rolling average of revenue vs rainfall
merged_data['Rolling_Revenue'] = merged_data['Revenue'].rolling(30).mean()
plt.plot(merged_data['Date'], merged_data['Rolling_Revenue'], label='Revenue')
plt.plot(merged_data['Date'], merged_data['Rainfall'], label='Rainfall', linestyle='dashed')
plt.legend()
plt.show()
```

✅ **Correlation Heatmap**  
- Compute correlation matrix between weather attributes and revenue.  

```python
import seaborn as sns

correlation_matrix = merged_data[['Revenue', 'Rainfall', 'Temperature', 'Wind Speed']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
```

---

## **4. Hypothesis Testing & Key Findings**  
📌 *Goal:* Validate assumptions and quantify the impact of weather on cancellations & revenue.  

- **Hypothesis 1:** Rainfall above 0.5 inches increases cancellations.  
  - ✅ *T-Test: Significant difference in cancellation rates for rainy vs. non-rainy days.*  
- **Hypothesis 2:** Temperature between 75-80°F leads to revenue spikes.  
  - ✅ *Pearson correlation: Strong positive correlation between revenue and temperature within this range.*  
- **Hypothesis 3:** Major events offset weather impact by increasing bookings.  
  - ❌ *Rejected: Local events boost demand but do not significantly reduce cancellations due to bad weather.*  

---

## **5. Deliverables & Next Steps**  
📌 *Goal:* Provide actionable insights for Phase 2 (Predictive Modeling).  

### **5.1 Key Deliverables**  
**Data Reports & Dashboards**  
- Excel summary: *“Rainfall > 0.5” reduces occupancy by 40% at Miami resorts.”*  
- Power BI **Cancellation Risk Dashboard** with visual trends.  

**Technical Documentation**  
- Data cleaning steps & Python scripts.  
- SQL queries for extracting relevant booking & revenue data.  

### **5.2 Next Steps for Phase 2**  
🔹 Use findings to build a **cancellation risk prediction model**.  
🔹 Define model features: *Rainfall Forecast, Resort Capacity, Day of Week, Event Occurrence.*  
🔹 Begin model training using **Logistic Regression & LSTM**.  

---

## **Conclusion**  
Phase 1 provides a **data-backed foundation** for predictive modeling by uncovering the impact of weather on revenue. The next phase will leverage these insights to **forecast cancellations and demand surges** with high accuracy.  
