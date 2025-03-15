
---
# **Hyper-Realistic Case Study: Menu Price Evolution Tracker**  
**Tools**: Python, SQL, Power BI, Tesseract OCR, AWS | **Duration**: 10-week Internship  
**Business Context**: *UrbanEats Diner Chain* (12 locations) faces shrinking margins due to inconsistent pricing. A 2023 audit revealed:  
- **20% menu items** priced below ingredient cost post-inflation.  
- **15% price disparity** for identical dishes across locations.  
- **30% customer complaints** on "overpriced" seasonal specials.  

**Goals**:  
1. Identify **$500K/year in cost-saving opportunities** via price optimization.  
2. Align prices with local competitor benchmarks.  
3. Reduce customer price complaints by 25% in 6 months.  

---

## **Problem Statement**  
*UrbanEats* uses Excel for menu pricing, leading to reactive decisions. Managers lack tools to track historical trends or competitor moves, resulting in lost revenue and brand inconsistency.  

---

## **Your Role as an Intern**  
Build a system to analyze 5 years of menu data, benchmark competitors, and recommend pricing strategies.  

---

### **Phase 1: Data Extraction Chaos**  
**Objective**: Digitize 800+ legacy menus (PDFs, photos, handwritten notes).  

#### **Challenges**  
1. **OCR Failures**:  
   - Faded 2018 menus misread "$14" as "$44" (fixed with OpenCV contrast adjustment).  
   - Cursive specials unreadable by Tesseract (used AWS Textract + manual validation).  

#### **Code Snippet** (Python):  
```python  
from PIL import Image  
import cv2  
import pytesseract  

def preprocess_image(img_path):  
    img = cv2.imread(img_path)  
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))  
    enhanced = clahe.apply(gray)  
    return enhanced  

menu_text = pytesseract.image_to_string(preprocess_image('old_menu.jpg'))  
```  

**Deliverable**:  
- Clean SQL database of 25K+ menu items with 98% accuracy.  

---

### **Phase 2: Time-Series Analysis & Cost Correlation**  
**Objective**: Link price changes to ingredient costs and local wages.  

#### **Data Sources**  
1. **USDA API**: Historical beef/poultry prices.  
2. **BLS Data**: City-specific minimum wage changes.  

#### **Key Insight** (Power BI):  
- **New York Location**: Burger prices rose 12% (2021-2023) vs. 34% beef cost increase → **$2.50/loss per burger**.  
- **Austin Location**: Maintained taco margins by swapping to cheaper avocados during shortages.  

#### **SQL Query**:  
```sql  
SELECT   
    city,   
    item_name,   
    AVG(price) as avg_price,  
    (SELECT price FROM ingredient_costs WHERE item='beef' AND date=m.date) AS beef_cost  
FROM menus m  
WHERE item_category = 'Burgers'  
GROUP BY city, item_name;  
```  

---

### **Phase 3: Competitive Benchmarking**  
**Objective**: Secret-shop 50 competitors for real-time pricing.  

#### **Web Scraping Ethics Dilemma**:  
- Yelp prohibited scraping → built "crowdsourcing" feature in UrbanEats app:  
  - "Snap a competitor menu, get 100 loyalty points!"  
  - 1,200 user submissions in 2 weeks.  

#### **Price Positioning Map** (Python):  
```python  
import matplotlib.pyplot as plt  

def plot_price_quality(competitors):  
    plt.scatter(competitors['price'], competitors['yelp_rating'])  
    plt.xlabel('Price')  
    plt.ylabel('Yelp Rating')  
    plt.title('Value-for-Money Analysis')  
    plt.show()  

# Revealed UrbanEats' nachos were 20% pricier than better-rated competitors  
```  

---

### **Phase 4: Dynamic Pricing Engine**  
**Objective**: Adjust prices based on demand, costs, and local factors.  

#### **Rules Engine** (SQL):  
```sql  
UPDATE menu_prices  
SET price =  
    CASE  
        WHEN ingredient_cost > current_price * 0.4 THEN current_price * 1.1  
        WHEN competitor_price < current_price * 0.9 THEN current_price * 0.95  
        ELSE current_price  
    END  
WHERE location = 'Chicago';  
```  

#### **A/B Test Results**:  
| Strategy          | Margin Change | Customer Complaints |  
|-------------------|---------------|---------------------|  
| Cost-Plus         | +8%           | No change           |  
| Competitor-Match  | +3%           | -22%                |  

---

### **Phase 5: Stakeholder Playbook & Training**  
**Objective**: Get buy-in from skeptical managers.  

#### **Playbook Components**:  
1. **"Red Zone" Alerts**: Items priced below cost (urgent fixes).  
2. **Localized Price Ceilings**: "Never charge >$18 for salads in Dallas (avg. competitor: $14)."  
3. **Promotion Calendar**: Discount overpiked items during off-peak hours.  

#### **Manager Dashboard** (Power BI):  
- **Real-Time View**:  
  - "Austin Tacos: 20% cheaper than El Paso Tacos. Recommend +$1.50."  
- **Customer Sentiment**:  
  - "Nacho complaints ↓ 40% after $2 price drop."  

---

## **Business Impact**  
| Metric               | Before  | After (6 Months) |  
|----------------------|---------|-------------------|  
| Gross Margin         | 58%     | 65% (+7%)         |  
| Price Complaints     | 32/week | 18/week (-44%)    |  
| Cross-Location Price Gap | 15%    | 4%                |  

---

## **Real-World Challenges**  
1. **Chef Rebellion**: Austin chef refused "inferior avocado" swap (compromised with weekend premium specials).  
2. **Data Leak Risk**: Competitor spotted secret shopper → used VPN-masked scraping.  
3. **Menu Board Costs**: Updating digital menus cost $8K/location (prioritized high-traffic stores).  

---

## **Deliverables**  
1. **Technical**:  
   - Python OCR pipeline with OpenCV enhancement.  
   - AWS DynamoDB for real-time competitor prices.  
2. **Business**:  
   - Power BI dashboard with pricing KPIs.  
   - "Price Optimization Playbook" for managers.  

---

## **Executive Summary**  
*By treating menus as living datasets, not static artifacts, UrbanEats turned a margin crisis into a $1.2M/year opportunity. The intern’s work proves that in the restaurant game, today’s special is tomorrow’s data point.*  

---

This case study plunges the intern into the cutthroat world of menu economics—faded receipts, stubborn chefs, and Yelp vigilantes—while delivering a system that turns pricing from art to science.
