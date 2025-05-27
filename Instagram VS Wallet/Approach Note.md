# **Approach Note: Phase 1 - Data Aggregation & Cleaning**

## **Objective**
To integrate and clean TikTok trend data with purchase and return logs, creating a structured dataset for predictive modeling.

## **Key Challenges & Considerations**
1. **Data Silos**: Trend data (TikTok API), transaction data (SQL), and resale data (scraping) exist in separate sources.
2. **Data Quality**: Missing return reasons (~15%) and inconsistent timestamps need imputation.
3. **Trend Alignment**: Purchases must be mapped to trend lifecycles (Peak, Decline, Death).

---

## **Approach**

### **Step 1: Extract & Preprocess Data**

#### **1.1 TikTok Trend Data (API Extraction)**
- Pull engagement metrics for viral products using TikTok API:
  - Hashtags: `#TikTokMadeMeBuyIt`, `#TrendingNow`
  - Engagement: `views`, `likes`, `shares`, `comments`
  - Video metadata: `upload_date`, `product_mentions`
- **Cleaning:**
  - Remove bot-driven anomalies using engagement ratio (`views/likes < 100`).
  ```sql
  DELETE FROM tiktok_data
  WHERE views / likes >= 100;
  ```
  - Normalize timestamps to match purchase records.

#### **1.2 Transaction Data (SQL Extraction)**
- Query purchase logs with key attributes:
  ```sql
  SELECT Order_ID, Product_ID, Purchase_Date, Return_Status, Customer_Age
  FROM transactions;
  ```
- **Cleaning:**
  - Standardize date formats.
  - Handle missing return reasons by inferring from trend lifecycles.

#### **1.3 Resale Data (Web Scraping)**
- Scrape eBay/Poshmark for resale pricing trends.
- **Key Variables:** Product_ID, Resale_Price, Days_Since_Trend_Peak.
- **Cleaning:** Convert price variations into % drop relative to original price.
  ```sql
  UPDATE resale_data
  SET price_drop_percent = ((original_price - resale_price) / original_price) * 100;
  ```

---

### **Step 2: Data Merging & Feature Engineering**

#### **2.1 Merging TikTok & Transaction Data**
- Join trend data with purchase logs using `trend_date ≈ purchase_date`:
  ```sql
  INSERT INTO merged_data (trend_id, product_id, trend_date, purchase_date)
  SELECT t.trend_id, t.product_id, t.trend_date, p.purchase_date
  FROM tiktok_data t
  JOIN purchase_data p ON t.trend_date = p.purchase_date;
  ```
- Create **Trend Lifecycle Stages**:
  - **Peak**: Max engagement date
  - **Decline**: Engagement drop >50%
  - **Death**: <5% of peak engagement

#### **2.2 Impute Return Reasons (SQL Update)**
- Assign missing return reasons based on trend stage:
  ```sql
  UPDATE returns
  SET reason = 'Regret'
  WHERE return_date BETWEEN (
      SELECT trend_peak_date + INTERVAL 7 DAY FROM tiktok_trends
      WHERE product_id = returns.product_id
  ) AND (
      SELECT trend_end_date FROM tiktok_trends
      WHERE product_id = returns.product_id
  );
  ```

#### **2.3 Feature Engineering**
- **Days Since Trend Peak**: Time gap between purchase and peak.
  ```sql
  UPDATE merged_data
  SET days_since_trend_peak = DATEDIFF(purchase_date, trend_peak_date);
  ```
- **Engagement Decay Rate**: Speed of trend decline.
  ```sql
  UPDATE tiktok_trends
  SET engagement_decay_rate = (peak_engagement - current_engagement) / DATEDIFF(current_date, peak_date);
  ```
- **Resale Price Drop %**: Indicator of regret likelihood.
  ```sql
  UPDATE resale_data
  SET price_drop_percent = ((original_price - resale_price) / original_price) * 100;
  ```

---

## **Deliverables**
- **Final Dataset** (500K+ rows): Integrated purchase, return, and trend data.
- **Data Dictionary**: Trend lifecycle definitions, engineered features.
- **SQL Scripts**: Extraction, cleaning, and merging processes.

---

## **Next Steps**
Proceed to **Phase 2: Exploratory Analysis** to identify key regret drivers.

# **Approach Note: Phase 2 - Exploratory Analysis**

## **Objective**
To analyze purchase behavior and regret drivers, identifying key trends and insights using SQL-based exploratory analysis.

---

## **Approach**

### **Step 1: Trend Longevity Analysis**

#### **1.1 Sales Velocity and Return Rate by Product Category**
- **Objective**: Identify product categories with high sales velocity and return rates to understand trends.
  ```sql
  SELECT
      product_category,
      AVG(sales_velocity) AS avg_sales_velocity,
      AVG(return_rate) AS avg_return_rate
  FROM product_data
  GROUP BY product_category;
  ```

#### **1.2 Percentage of Returns within 14 Days of Trend Peak**
- **Objective**: Determine the proportion of returns occurring shortly after the trend peak.
  ```sql
  SELECT
      COUNT(*) * 100.0 / (SELECT COUNT(*) FROM returns) AS percentage_returns_within_14_days
  FROM returns
  WHERE return_date <= trend_peak_date + INTERVAL 14 DAY;
  ```

#### **1.3 Average Time to Return by Product Category**
- **Objective**: Calculate the average time taken for returns in each product category.
  ```sql
  SELECT
      product_category,
      AVG(DATEDIFF(return_date, purchase_date)) AS avg_time_to_return
  FROM product_data
  WHERE returned = 1
  GROUP BY product_category;
  ```

#### **1.4 Correlation Between Engagement Metrics and Return Rates**
- **Objective**: Analyze the relationship between TikTok engagement metrics and product return rates.
  ```sql
  SELECT
      AVG(views) AS avg_views,
      AVG(likes) AS avg_likes,
      AVG(return_rate) AS avg_return_rate
  FROM tiktok_engagement_data
  GROUP BY product_id;
  ```

---

### **Step 2: Sentiment & Quality Analysis**

#### **2.1 Negative Sentiment Correlation with Return Probability**
- **Objective**: Analyze the relationship between negative customer sentiment and product returns.
  ```sql
  SELECT
      AVG(CASE WHEN sentiment < 0 THEN 1 ELSE 0 END) AS negative_sentiment_rate,
      AVG(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS return_rate
  FROM review_data;
  ```

#### **2.2 Products Reselling for <40% of Original Price**
- **Objective**: Identify products with significant price drops in the resale market.
  ```sql
  SELECT
      product_id,
      AVG(resale_price / original_price) AS price_drop_ratio
  FROM resale_data
  GROUP BY product_id
  HAVING AVG(resale_price / original_price) < 0.4;
  ```

#### **2.3 Customer Age Distribution and Return Rates**
- **Objective**: Analyze the impact of customer age on return rates.
  ```sql
  SELECT
      customer_age_group,
      AVG(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS return_rate
  FROM customer_data
  GROUP BY customer_age_group;
  ```

#### **2.4 Impact of Product Mentions in TikTok Videos on Sales**
- **Objective**: Determine how product mentions in TikTok videos affect sales.
  ```sql
  SELECT
      product_id,
      COUNT(*) AS mention_count,
      AVG(sales_volume) AS avg_sales_volume
  FROM tiktok_mentions
  GROUP BY product_id;
  ```

---

### **Step 3: Visualizing Insights**

#### **3.1 Top 5 Regret Drivers**
- **Objective**: Identify the most common drivers of product returns.
  ```sql
  SELECT
      regret_driver,
      COUNT(*) AS frequency
  FROM regret_drivers
  GROUP BY regret_driver
  ORDER BY frequency DESC
  LIMIT 5;
  ```

#### **3.2 Heatmap of Regret Rates by Product Category**
- **Objective**: Visualize regret rates across different product categories.
  ```sql
  SELECT
      product_category,
      AVG(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS regret_rate
  FROM product_data
  GROUP BY product_category;
  ```

#### **3.3 Sales and Return Trends Over Time**
- **Objective**: Analyze sales and return trends over a specific time period.
  ```sql
  SELECT
      DATE_TRUNC('month', purchase_date) AS month,
      SUM(sales_volume) AS total_sales,
      SUM(CASE WHEN returned = 1 THEN 1 ELSE 0 END) AS total_returns
  FROM product_data
  GROUP BY DATE_TRUNC('month', purchase_date);
  ```

#### **3.4 Customer Demographics and Purchase Behavior**
- **Objective**: Understand the relationship between customer demographics and purchase behavior.
  ```sql
  SELECT
      customer_age_group,
      AVG(purchase_frequency) AS avg_purchase_frequency,
      AVG(avg_purchase_value) AS avg_purchase_value
  FROM customer_data
  GROUP BY customer_age_group;
  ```

---

## **Deliverables**
- **SQL Queries**: Trend longevity and sentiment analysis.
- **Executive Summary**: Regret trends and actionable insights.

---

## **Next Steps**
Proceed to **Phase 3: Predictive Modeling** to develop a predictive model for identifying high-regret products.

# **Approach Note: Phase 3 - Predictive Modeling**

## **Objective**
To develop a predictive model for identifying high-regret products using machine learning techniques.

---

## **Approach**

### **Step 1: Data Preparation**

#### **1.1 Feature Selection**
- **Situation**: We have a dataset with various features related to product trends, customer behavior, and engagement metrics.
- **Task**: Select the most relevant features for building the predictive model.
- **Action**: Use domain knowledge and exploratory analysis to select features such as sales velocity, return rate, sentiment score, engagement metrics, and customer demographics.
- **Result**: A refined dataset with the most impactful features for modeling.

```python
import pandas as pd

# Load the dataset
data = pd.read_csv('product_data.csv')

# Select relevant features
features = ['sales_velocity', 'return_rate', 'sentiment_score', 'views', 'likes', 'customer_age_group']
target = 'high_regret'

# Create feature matrix and target vector
X = data[features]
y = data[target]
```

#### **1.2 Data Splitting**
- **Situation**: We need to split the data into training and testing sets to evaluate the model's performance.
- **Task**: Split the dataset into training and testing sets.
- **Action**: Use the `train_test_split` function from `sklearn.model_selection`.
- **Result**: Training and testing datasets ready for model training and evaluation.

```python
from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

---

### **Step 2: Model Training**

#### **2.1 Model Selection**
- **Situation**: We need to choose an appropriate machine learning algorithm for classification.
- **Task**: Select a suitable algorithm for predicting high-regret products.
- **Action**: Use a Random Forest Classifier due to its robustness and ability to handle various types of data.
- **Result**: A selected model ready for training.

```python
from sklearn.ensemble import RandomForestClassifier

# Initialize the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
```

#### **2.2 Model Training**
- **Situation**: We have the training data and a selected model.
- **Task**: Train the model on the training data.
- **Action**: Use the `fit` method of the Random Forest Classifier.
- **Result**: A trained model ready for evaluation.

```python
# Train the model
model.fit(X_train, y_train)
```

---

### **Step 3: Model Evaluation**

#### **3.1 Model Prediction**
- **Situation**: We have a trained model and testing data.
- **Task**: Make predictions on the testing data.
- **Action**: Use the `predict` method of the trained model.
- **Result**: Predictions for the testing data.

```python
# Make predictions on the testing data
y_pred = model.predict(X_test)
```

#### **3.2 Model Evaluation**
- **Situation**: We have predictions for the testing data.
- **Task**: Evaluate the model's performance.
- **Action**: Use metrics such as accuracy, precision, recall, and F1-score.
- **Result**: Evaluation metrics to assess the model's performance.

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1-Score: {f1:.2f}')
```

---

### **Step 4: Model Interpretation**

#### **4.1 Feature Importance**
- **Situation**: We need to understand which features are most important for the model's predictions.
- **Task**: Extract and visualize feature importances.
- **Action**: Use the `feature_importances_` attribute of the Random Forest Classifier.
- **Result**: Insights into the most impactful features.

```python
import matplotlib.pyplot as plt

# Get feature importances
importances = model.feature_importances_

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel('Feature Importance')
plt.ylabel('Feature')
plt.title('Feature Importances')
plt.show()
```

#### **4.2 Model Interpretation**
- **Situation**: We have feature importances and evaluation metrics.
- **Task**: Interpret the model's performance and feature importances.
- **Action**: Analyze the feature importances and evaluation metrics to understand the model's behavior.
- **Result**: Insights into the model's strengths and weaknesses, and areas for improvement.

---

## **Deliverables**
- **Trained Model**: A predictive model for identifying high-regret products.
- **Evaluation Metrics**: Performance metrics for the trained model.
- **Feature Importances**: Insights into the most impactful features.

---

## **Next Steps**
- **Model Deployment**: Deploy the trained model for real-time predictions.
- **Continuous Monitoring**: Monitor the model's performance and update it as needed.
- **Further Analysis**: Conduct further analysis to improve the model's accuracy and interpretability.
