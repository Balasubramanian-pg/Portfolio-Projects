# TrendBuy: From Viral Sales to Sustainable Growth"

Objective: As a data-driven intern at TrendBuy, a fast-fashion retailer, your mission is to tackle the $10 million annual loss due to returns on TikTok-driven purchases. Your goal is to build a predictive model that identifies high-regret-risk purchases and develop an intervention engine to reduce returns by 25% in 6 months.

#### Project Overview:
In this guided project, you'll work through the following phases:

- Data Aggregation & Cleaning: Merge TikTok trend data with purchase and return logs to create a comprehensive dataset.
- Exploratory Analysis: Identify regret drivers and trends using Power BI and Python.
- Predictive Modeling: Develop an XGBoost model to flag high-regret-risk purchases in real-time.
- Intervention Engine: Design a system to nudge customers with personalized offers and messages.
- Consumer App & Dashboard: Create a prototype of the "TrendGuard" app and a Power BI dashboard for managers.

#### Key Deliverables:

- A predictive model with 85% accuracy in identifying high-regret-risk purchases
- A fully functional intervention engine that reduces returns by 25% in 6 months
- A prototype of the "TrendGuard" consumer app
- A Power BI dashboard with regret risk analytics and ROI tracking

### Technical Requirements:

- Python scripting for data cleaning, feature engineering, and modeling
- SQL pipelines for data aggregation and intervention triggers
- Power BI for data visualization and dashboard creation
- XGBoost for predictive modeling

### Business Impact:
By completing this project, you'll help TrendBuy:

- Reduce return rates by 25% in 6 months
= Increase customer satisfaction ratings by 28%
- Recover $2.1 million in resale revenue

Let's Get Started!
In the following sections, we'll guide you through each phase of the project, providing code snippets, technical requirements, and business insights to help you succeed.

### Phase 1: Data Aggregation & Cleaning
Your first task is to merge TikTok trend data with purchase and return logs. You'll use Python to clean and preprocess the data, and SQL to create a comprehensive dataset.

```Python

import pandas as pd

# Load TikTok trend data
trends = pd.read_csv('tiktok_trends.csv')

# Load purchase and return logs
purchases = pd.read_csv('purchases.csv')
returns = pd.read_csv('returns.csv')

# Merge datasets
merged_data = pd.merge(trends, purchases, on='product_id')
```

What's Next?
In the next section, you'll perform exploratory analysis to identify regret drivers and trends. You'll use Power BI to visualize the data and Python to perform sentiment analysis.
Let's get started!
