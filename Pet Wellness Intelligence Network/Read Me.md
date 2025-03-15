
---
# **Hyper-Realistic Case Study: Pet Wellness Tracker**  
**Tools**: Python, SQL, IoT (Arduino/Raspberry Pi), Power BI, Figma | **Duration**: 12-week Internship  
**Business Context**: *PawsCare Vet Clinics*, a chain of 50 clinics, faces a 30% no-show rate for vaccinations and a 25% rise in obesity-related pet illnesses. Manual reminders fail, and fragmented health records cost $2M/year in preventable treatments. Their goals:  
1. Reduce missed wellness appointments by 40% in 6 months.  
2. Cut obesity-related visits by 20% through personalized diet plans.  
3. Build a pet owner app with 80% adoption across their client base.  

---

## **Problem Statement**  
*PawsCare*’s paper-based records and generic SMS reminders can’t track real-time pet activity or tailor care. Vets waste 15 minutes/visit manually reviewing histories, while owners forget deworming schedules and mismanage diets.  

---

## **Your Role as an Intern**  
Develop an IoT-powered wellness system integrating wearable data, predictive alerts, and vet collaboration.  

---

### **Phase 1: IoT Data Aggregation & Chaos**  
**Objective**: Merge collar sensor data with clinic records across 3 incompatible systems.  

#### **Challenges**  
1. **Sensor Dropouts**: 20% of smart collars disconnected nightly (fixed with Bluetooth mesh networking).  
2. **Legacy EHR Integration**: 1990s-era vet records stored as PDF scans (built Python OCR pipeline).  

#### **Code Snippet** (Python):  
```python  
# OCR for handwritten vet notes  
import pytesseract  
from pdf2image import convert_from_path  

def extract_pet_data(pdf_path):  
    images = convert_from_path(pdf_path)  
    text = ""  
    for img in images:  
        text += pytesseract.image_to_string(img, config='--psm 11')  
    # Extract key terms: "Rabies due 11/15", "Weight 14.5kg"  
    return parse_medical_text(text)  # Custom regex function  

# Usage: Digitize 10K legacy records  
pdf_path = 'fluffy_2019.pdf'  
health_data = extract_pet_data(pdf_path)  
```  

**Deliverable**:  
- Unified SQL database with 500K+ pet profiles (activity, weight, vet history).  

---

### **Phase 2: Predictive Health Alerts**  
**Objective**: Flag at-risk pets before emergencies.  

#### **Model Development**  
1. **Algorithm**: XGBoost + LSTM for time-series collar data.  
2. **Features**:  
   - `Activity_Change` (10% drop → UTI risk).  
   - `Lick_Sensor` (excessive grooming → allergy flag).  
3. **Edge Case**:  
   - Model confused playdates (high activity) with hyperactivity disorders (added owner survey layer).  

#### **Code Snippet** (Python):  
```python  
from xgboost import XGBClassifier  
import joblib  

# Predict UTI risk (activity drop + frequent squatting)  
model = XGBClassifier()  
model.fit(X_train[['activity_delta', 'squat_count']], y_train)  
joblib.dump(model, 'uti_model.pkl')  

# Real-time prediction  
current_data = [[-0.15, 8]]  # 15% activity drop, 8 squats/hour  
risk = model.predict_proba(current_data)[0][1]  # 92% risk → Alert vet  
```  

---

### **Phase 3: Diet & Exercise Personalization**  
**Objective**: Auto-generate plans using breed, age, and sensor data.  

#### **Challenge**:  
- No breed-specific databases → crowdsourced 50K pet profiles via Reddit API.  

#### **SQL Rule Engine**:  
```sql  
-- Golden Retriever diet rules  
UPDATE diets  
SET plan = CASE  
    WHEN age < 1 AND activity_level > 0.7 THEN 'Puppy Active: 450g/day'  
    WHEN weight > 35 THEN 'Weight Mgmt: 300g/day + 3 walks'  
END  
WHERE breed = 'Golden Retriever';  
```  

**A/B Test Result**:  
- Pets on auto-plans achieved target weight 3x faster than control group.  

---

### **Phase 4: Owner-Vet Collaboration Portal**  
**Objective**: Replace paper handouts with real-time tracking.  

#### **Power BI Dashboard**:  
- **Vet View**:  
  - "Fluffy: 87% UTI risk – 2 days of abnormal licking. Prescribe antibiotics?"  
- **Owner App (Figma Prototype)**:  
  - Push notification: "Fluffy’s rabies shot due! Book now + earn 50 PawsPoints."  
  - Social feature: "Local Chihuahua playgroup – 1 mile away."  

#### **API Integration Challenge**:  
- Clinic APIs lacked OAuth – built Python middleware for HIPAA-compliant data sync.  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Missed Appointments  | 30%     | 18% (-40%)        |  
| Obesity Visits       | 120/mo  | 89/mo (-26%)      |  
| Owner App Adoption   | 0%      | 76%               |  

---

## **Real-World Challenges**  
1. **Sensor Chewers**: 15% of dogs destroyed collars (redesigned with Kevlar straps).  
2. **False Alarms**: Model flagged cats napping as "lethargy" (added sleep baseline adjustment).  
3. **Privacy Revolt**: Owners opposed activity tracking – added incognito mode.  

---

## **Deliverables**  
1. **Technical**:  
   - Python OCR + ML pipelines.  
   - IoT firmware update for mesh networking.  
2. **Business**:  
   - Power BI vet dashboard.  
   - Figma app prototype with 10K+ user test notes.  

---

## **Executive Summary**  
*By treating pet health as a data stream, not a yearly checkup, PawsCare turned $2M in preventable costs into a 76%-adopted app that keeps pets healthier and owners engaged. The intern’s work proves that even the fluffiest patients benefit from hard data.*  

---

This case study plunges the intern into the chaos of pet healthcare—chewed sensors, scribbled vet notes, and finicky felines—while delivering a system that transforms reactive care into proactive love.
