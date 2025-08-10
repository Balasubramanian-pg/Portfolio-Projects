# Consolidated Python Code for Churn Prediction Case Study (Phases 1-6)

#-------------------------------------------------------------------------------
# PRELIMINARIES & IMPORTS
#-------------------------------------------------------------------------------
print("--- Initializing: Importing Libraries ---")
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib # For saving/loading models and scalers
import json # For JSON operations if needed directly

# Phase 1 specific (already covered by pandas for loading)

# Phase 3 specific
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

# SHAP
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    print("SHAP library not found. SHAP visualizations will be skipped.")
    SHAP_AVAILABLE = False


# Phase 4 specific
# from fastapi import FastAPI # Will be defined in its section
# import uvicorn # For running FastAPI app, not directly used in script

# Phase 5 specific
try:
    from skopt import BayesSearchCV
    from skopt.space import Real, Categorical, Integer
    SKOPT_AVAILABLE = True
except ImportError:
    print("scikit-optimize (skopt) not found. Bayesian Optimization will be skipped.")
    SKOPT_AVAILABLE = False

from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
try:
    from lightgbm import LGBMClassifier
    LGBM_AVAILABLE = True
except ImportError:
    print("LightGBM not found. Stacking with LightGBM meta-model will be skipped.")
    LGBM_AVAILABLE = False

try:
    from mlxtend.frequent_patterns import apriori, association_rules
    from mlxtend.preprocessing import TransactionEncoder
    MLXTEND_AVAILABLE = True
except ImportError:
    print("mlxtend not found. Market Basket Analysis will be skipped.")
    MLXTEND_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Transformers library not found. NLP-based sentiment analysis will be skipped.")
    TRANSFORMERS_AVAILABLE = False


# Phase 6 specific
from sklearn.cluster import KMeans

# Suppress warnings for cleaner output (optional)
import warnings
warnings.filterwarnings('ignore')

#-------------------------------------------------------------------------------
# MOCK DATA GENERATION
#-------------------------------------------------------------------------------
print("\n--- Generating Mock Data ---")

def generate_mock_data(num_customers=2000, num_usage_logs_per_customer=5, num_support_tickets=500):
    customer_ids = [f"CUST{i:04d}" for i in range(1, num_customers + 1)]

    # CRM Data
    crm_data = {
        'Customer_ID': customer_ids,
        'Plan_Type': np.random.choice(['Basic', 'Premium', 'Enterprise'], num_customers),
        'Tenure': np.random.randint(-12, 60, num_customers), # Include some negatives for cleaning
        'Monthly_Charges': np.random.uniform(20, 200, num_customers),
        'Upgrade_History': np.random.choice(['Upgraded', 'Downgraded', None, 'Initial'], num_customers, p=[0.2, 0.1, 0.15, 0.55])
    }
    crm_df = pd.DataFrame(crm_data)

    # Usage Logs (more than 2M rows simulated by customer count and logs per customer)
    usage_data_list = []
    log_id_counter = 0
    for cid in customer_ids:
        for _ in range(np.random.randint(1, num_usage_logs_per_customer + 1)): # Simulating 2M+ rows would be large here
            log_id_counter +=1
            usage_data_list.append({
                'Log_ID': f"LOG{log_id_counter:05d}",
                'Customer_ID': cid,
                'Usage_Timestamp': pd.Timestamp('now') - pd.Timedelta(days=np.random.randint(0, 30)),
                'Data_Used_GB': np.random.uniform(0.1, 50),
                'Call_Duration_Mins': np.random.uniform(0, 120) if np.random.rand() > 0.3 else 0,
                'Outage_Count_Month': np.random.choice([0,1,2,3,4,5], p=[0.5,0.2,0.1,0.1,0.05,0.05]) # Used later
            })
    usage_df = pd.DataFrame(usage_data_list)
    # Aggregate usage for features
    usage_agg = usage_df.groupby('Customer_ID').agg(
        Total_Data_Used_GB=('Data_Used_GB', 'sum'),
        Avg_Call_Duration_Mins=('Call_Duration_Mins', 'mean'),
        Outage_Count=('Outage_Count_Month', 'max') # Simplified, take max outages reported in logs
    ).reset_index()


    # Support Tickets
    support_data_list = []
    ticket_id_counter = 0
    for _ in range(num_support_tickets):
        ticket_id_counter += 1
        support_data_list.append({
            'Ticket_ID': f"TKT{ticket_id_counter:04d}",
            'Customer_ID': np.random.choice(customer_ids),
            'Ticket_Date': pd.Timestamp('now') - pd.Timedelta(days=np.random.randint(0, 90)),
            'Sentiment_Text': np.random.choice(['frustrated', 'neutral', 'satisfied', 'very frustrated', 'very satisfied']),
            'Issue_Type': np.random.choice(['Billing', 'Technical', 'Service', 'Other'])
        })
    support_df = pd.DataFrame(support_data_list)

    # Churn Target Variable (add to CRM for simplicity)
    # Simulate churn based on some mock factors
    churn_probabilities = (crm_df['Monthly_Charges'] / 200) - (crm_df['Tenure'].clip(lower=0) / 60) + np.random.normal(0, 0.2, num_customers)
    crm_df['Churned'] = (churn_probabilities > np.percentile(churn_probabilities, 80)).astype(int) # Approx 20% churn rate

    # Transaction data for Market Basket Analysis (Phase 5)
    products = ['ProductA', 'ProductB', 'ProductC', 'ProductD', 'ServiceX', 'ServiceY']
    transactions_list = []
    for cid in customer_ids:
        num_prods = np.random.randint(1, 4)
        for prod in np.random.choice(products, num_prods, replace=False):
            transactions_list.append({'Customer_ID': cid, 'Product': prod})
    transaction_data_df = pd.DataFrame(transactions_list)

    # Feature for 'Months_Since_Upgrade' (used in Phase 2 & 3)
    crm_df['Months_Since_Upgrade'] = np.random.randint(0, 24, num_customers)
    crm_df.loc[crm_df['Upgrade_History'].isnull(), 'Months_Since_Upgrade'] = crm_df['Tenure'].clip(lower=0) # If no upgrade history, use tenure

    print("Mock CRM Data Head:\n", crm_df.head())
    print("Mock Usage Aggregated Data Head:\n", usage_agg.head())
    print("Mock Support Tickets Data Head:\n", support_df.head())
    print("Mock Transaction Data Head:\n", transaction_data_df.head())

    return crm_df, usage_agg, support_df, transaction_data_df

crm_mock, usage_agg_mock, support_mock, transaction_mock = generate_mock_data(num_customers=500) # Smaller for faster demo

# Save to mock CSV/JSON for Phase 1 loading example
crm_mock.to_csv("customers_mock.csv", index=False) # Simulating SQL source by saving then loading
usage_agg_mock.to_csv("usage_logs_agg_mock.csv", index=False) # Using aggregated for simplicity
support_mock.to_json("support_tickets_mock.json", orient='records', lines=True)


#-------------------------------------------------------------------------------
# PHASE 1: Data Aggregation & Cleaning
#-------------------------------------------------------------------------------
print("\n--- PHASE 1: Data Aggregation & Cleaning ---")

# Step 1: Extract & Load Data (using mock files)
# SQL Query for CRM Data Extraction (simulation)
# ```sql
# SELECT Customer_ID, Plan_Type, Tenure, Monthly_Charges, Upgrade_History
# FROM customers;
# ```
crm_data_loaded = pd.read_csv("customers_mock.csv") # Loaded from mock CSV
print("\nLoaded CRM Data (mock):\n", crm_data_loaded.head())

# Load CSV (Usage Logs) & JSON (Support Tickets) into Pandas
usage_data_loaded = pd.read_csv("usage_logs_agg_mock.csv") # Using aggregated mock
support_data_loaded = pd.read_json("support_tickets_mock.json", orient='records', lines=True)
print("\nLoaded Usage Data (mock):\n", usage_data_loaded.head())
print("\nLoaded Support Tickets (mock):\n", support_data_loaded.head())

# Step 2: Data Cleaning & Transformation
# Fix Tenure Inconsistencies (Negative Values)
# ```sql
# UPDATE customers
# SET Tenure = ABS(Tenure)
# WHERE Tenure < 0;
# ```
# Python equivalent:
print(f"\nTenure before cleaning: Min={crm_data_loaded['Tenure'].min()}, Max={crm_data_loaded['Tenure'].max()}")
crm_data_loaded['Tenure'] = crm_data_loaded['Tenure'].abs()
print(f"Tenure after cleaning: Min={crm_data_loaded['Tenure'].min()}, Max={crm_data_loaded['Tenure'].max()}")


# Convert Sentiment Text to Numerical Scores (on support_data_loaded)
sentiment_mapping = {'frustrated': -1, 'neutral': 0, 'satisfied': 1,
                     'very frustrated': -2, 'very satisfied': 2} # Extended mapping
support_data_loaded['Sentiment_Score_Raw'] = support_data_loaded['Sentiment_Text'].map(sentiment_mapping)

# Aggregate sentiment score per customer (e.g., average or most recent)
support_agg = support_data_loaded.groupby('Customer_ID').agg(
    Sentiment_Score=('Sentiment_Score_Raw', 'mean'),
    Num_Support_Tickets=('Ticket_ID', 'count')
).reset_index()
print("\nAggregated Support Data with Sentiment Score:\n", support_agg.head())


# Step 3: Data Integration & Quality Check
# Merge Datasets on Customer_ID
# `final_data = usage.merge(support, on="Customer_ID", how="left").merge(crm, on="Customer_ID", how="left")`
merged_data = crm_data_loaded.merge(usage_data_loaded, on="Customer_ID", how="left")
merged_data = merged_data.merge(support_agg, on="Customer_ID", how="left")
print("\nMerged Data (preview):\n", merged_data.head())

# Handle Missing Values (after merge)
# `merged_data['Upgrade_History'].fillna("No Upgrade", inplace=True)`
# `merged_data['Sentiment_Score'].fillna(0, inplace=True) # Assume neutral sentiment if no ticket`
merged_data['Upgrade_History'].fillna("No Upgrade", inplace=True)
merged_data['Sentiment_Score'].fillna(0, inplace=True) # If no support ticket, assume neutral
merged_data['Num_Support_Tickets'].fillna(0, inplace=True)
# For other numeric columns from merges
for col in ['Total_Data_Used_GB', 'Avg_Call_Duration_Mins', 'Outage_Count']:
    if col in merged_data.columns:
         merged_data[col].fillna(merged_data[col].median(), inplace=True) # Impute with median

# Validate Data Completeness
missing_values_percentage = merged_data.isnull().sum() * 100 / len(merged_data)
print("\nMissing Values Percentage after cleaning & merging:\n", missing_values_percentage)
# Ensure all relevant columns are >95% complete (ideally 100% after imputation)

# Final dataset from Phase 1
final_data_phase1 = merged_data.copy()
print("\nFinal Data after Phase 1 (Head):\n", final_data_phase1.head())
print("\nFinal Data after Phase 1 (Shape):", final_data_phase1.shape)


#-------------------------------------------------------------------------------
# PHASE 2: Exploratory Data Analysis (EDA)
#-------------------------------------------------------------------------------
print("\n\n--- PHASE 2: Exploratory Data Analysis (EDA) ---")
# Using final_data_phase1 as 'merged_data' for this phase

# 1. Data Profiling
# Missing values (already checked, but good practice to re-verify)
print("\nMissing values in EDA dataset:\n", final_data_phase1.isnull().sum())

# Outliers detection for 'Monthly_Charges'
plt.figure(figsize=(6,4))
sns.boxplot(x=final_data_phase1['Monthly_Charges'])
plt.title("Boxplot of Monthly Charges (Before Winsorizing)")
plt.show()

# Fix: Winsorized extreme values (>99th percentile)
# from scipy.stats.mstats import winsorize # Not used here for simplicity, but this is how
# final_data_phase1['Monthly_Charges_Winsorized'] = winsorize(final_data_phase1['Monthly_Charges'], limits=[0.0, 0.01])
# Using clipping as a simpler alternative for demonstration
q99 = final_data_phase1['Monthly_Charges'].quantile(0.99)
final_data_phase1['Monthly_Charges_Clipped'] = final_data_phase1['Monthly_Charges'].clip(upper=q99)

plt.figure(figsize=(6,4))
sns.boxplot(x=final_data_phase1['Monthly_Charges_Clipped'])
plt.title("Boxplot of Monthly Charges (After Clipping at 99th Percentile)")
plt.show()

# 2. Churn Triggers Analysis
# A. Outage Frequency & Churn
# SQL Query to Extract Insights: (Conceptual, Python equivalent below)
# ```sql
# SELECT Outage_Count, COUNT(*) AS Customer_Count,
#        SUM(CASE WHEN Churned = 1 THEN 1 ELSE 0 END) AS Churners
# FROM merged_data
# GROUP BY Outage_Count
# ORDER BY Outage_Count DESC;
# ```
if 'Outage_Count' in final_data_phase1.columns:
    outage_churn_analysis = final_data_phase1.groupby('Outage_Count')['Churned'].agg(['count', 'sum']).rename(
        columns={'count': 'Customer_Count', 'sum': 'Churners'}
    ).sort_values(by='Outage_Count', ascending=False)
    outage_churn_analysis['Churn_Rate'] = outage_churn_analysis['Churners'] / outage_churn_analysis['Customer_Count']
    print("\nOutage Count vs. Churn:\n", outage_churn_analysis)

    # Power BI Visualization: Heatmap (Simulated with Seaborn)
    plt.figure(figsize=(8, 6))
    if not outage_churn_analysis.empty:
        # Pivot for heatmap
        outage_pivot = final_data_phase1.groupby(['Outage_Count', 'Churned']).size().unstack(fill_value=0)
        sns.heatmap(outage_pivot, annot=True, fmt="d", cmap="viridis")
        plt.title("Heatmap of Churn vs. Outage Count")
        plt.ylabel("Outage Count")
        plt.xlabel("Churned (0=No, 1=Yes)")
        plt.show()
else:
    print("\n'Outage_Count' not available for analysis.")


# B. Plan Age & Churn (using 'Months_Since_Upgrade' as proxy for plan age related feature)
# Python Correlation Check:
if 'Months_Since_Upgrade' in final_data_phase1.columns:
    correlation_plan_age_churn = final_data_phase1[['Months_Since_Upgrade', 'Churned']].corr()
    print("\nCorrelation between 'Months_Since_Upgrade' and 'Churned':\n", correlation_plan_age_churn)

    # Power BI Visualization: Line chart (Simulated with Matplotlib/Seaborn)
    if 'Months_Since_Upgrade' in final_data_phase1.columns:
        plan_age_churn_rate = final_data_phase1.groupby('Months_Since_Upgrade')['Churned'].mean()
        plt.figure(figsize=(10, 6))
        plan_age_churn_rate.plot(kind='line', marker='o')
        plt.title("Churn Rate by Months Since Last Upgrade")
        plt.xlabel("Months Since Last Upgrade")
        plt.ylabel("Churn Rate")
        plt.grid(True)
        plt.show()
else:
    print("\n'Months_Since_Upgrade' not available for analysis.")


# C. Sentiment Analysis & Churn
# Python Correlation Check (Sentiment_Score vs Churned):
correlation_sentiment_churn = final_data_phase1[['Sentiment_Score', 'Churned']].corr()
print("\nCorrelation between 'Sentiment_Score' and 'Churned':\n", correlation_sentiment_churn)

# Python Code Snippet for Scatter Plot:
plt.figure(figsize=(8, 6))
plt.scatter(final_data_phase1['Sentiment_Score'], final_data_phase1['Churned'], alpha=0.1) # Alpha for density
# Add jitter for better visualization of binary outcome
sns.stripplot(x='Sentiment_Score', y='Churned', data=final_data_phase1, jitter=True, alpha=0.5, orient='h')
plt.xlabel('Sentiment Score')
plt.ylabel('Churned (0 or 1)')
plt.title('Sentiment Score vs. Churn (with Jitter)')
plt.show()

# 3. Customer Segmentation (Conceptual - based on findings)
# This would typically involve creating flags based on the criteria
# Example:
# final_data_phase1['Risk_Segment'] = 'Low Risk'
# final_data_phase1.loc[(final_data_phase1['Outage_Count'] > 3) & (final_data_phase1['Sentiment_Score'] < 0), 'Risk_Segment'] = 'High Risk'
# final_data_phase1.loc[(final_data_phase1['Months_Since_Upgrade'] > 12) & (final_data_phase1['Risk_Segment'] == 'Low Risk'), 'Risk_Segment'] = 'Moderate Risk' # Avoid overwriting High Risk
# print("\nCustomer Segmentation example:\n", final_data_phase1['Risk_Segment'].value_counts())

# Prepare data for Phase 3 (select features, handle categoricals)
data_for_modeling = final_data_phase1.copy()
# Drop highly correlated or redundant, or non-numeric for now
# For simplicity, ensure features used in modeling part exist and are numeric
# Let's one-hot encode 'Plan_Type' and 'Upgrade_History'
data_for_modeling = pd.get_dummies(data_for_modeling, columns=['Plan_Type', 'Upgrade_History'], drop_first=True)

# Select features for modeling (example set)
# Ensure all these columns exist after dummification.
potential_features = ['Tenure', 'Monthly_Charges_Clipped', 'Months_Since_Upgrade', 'Outage_Count',
                      'Sentiment_Score', 'Num_Support_Tickets', 'Total_Data_Used_GB', 'Avg_Call_Duration_Mins']
# Add dummy variable columns
dummy_cols = [col for col in data_for_modeling.columns if 'Plan_Type_' in col or 'Upgrade_History_' in col]
potential_features.extend(dummy_cols)

# Keep only existing features
features_for_model = [f for f in potential_features if f in data_for_modeling.columns]
target_variable = 'Churned'

# Check for NaN in selected features and target before modeling
data_for_modeling = data_for_modeling[features_for_model + [target_variable]].dropna()

X = data_for_modeling[features_for_model]
y = data_for_modeling[target_variable]

print("\nShape of X for modeling:", X.shape)
print("Shape of y for modeling:", y.shape)
print("\nFeatures selected for modeling:\n", X.columns.tolist())


#-------------------------------------------------------------------------------
# PHASE 3: Predictive Modeling & Churn Prevention Strategies
#-------------------------------------------------------------------------------
print("\n\n--- PHASE 3: Predictive Modeling & Churn Prevention Strategies ---")

if X.empty or y.empty:
    print("Skipping Phase 3 due to empty feature set or target.")
else:
    # 1. Model Selection & Training
    # A. Feature Engineering (largely done above, now splitting and scaling)
    # Splitting data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if y.nunique() > 1 else None)

    # Standardizing
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, "scaler_phase3.pkl") # Save scaler
    print("Scaler saved as scaler_phase3.pkl")


    # B. Model Comparison (We will train XGBoost as it was the best performer)
    # Training XGBoost:
    print("\nTraining XGBoost Model...")
    xgb_model = XGBClassifier(n_estimators=100, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb_model.fit(X_train_scaled, y_train)
    joblib.dump(xgb_model, "xgboost_churn_model_phase3.pkl") # Save model
    print("XGBoost model saved as xgboost_churn_model_phase3.pkl")


    # Predictions
    y_pred_xgb = xgb_model.predict(X_test_scaled)
    y_pred_proba_xgb = xgb_model.predict_proba(X_test_scaled)[:, 1]

    print("\nXGBoost Classification Report:\n", classification_report(y_test, y_pred_xgb))
    print("XGBoost ROC AUC Score:", roc_auc_score(y_test, y_pred_proba_xgb))


    # 2. Model Interpretability & Risk Scoring
    # SHAP (Explainability) Implementation:
    if SHAP_AVAILABLE:
        print("\nGenerating SHAP values for XGBoost model...")
        try:
            explainer = shap.Explainer(xgb_model, X_train_scaled) # Use TreeExplainer for XGBoost
            shap_values = explainer(X_test_scaled) # Pass the test data

            # For summary_plot, shap_values object itself can often be used directly if it's the right type.
            # Or, if shap_values.values is needed:
            shap_values_for_plot = shap_values.values if hasattr(shap_values, 'values') else shap_values

            # Convert X_test_scaled to DataFrame with feature names for plot
            X_test_df_for_shap = pd.DataFrame(X_test_scaled, columns=X.columns)

            plt.figure() # Create a new figure to avoid overlap
            shap.summary_plot(shap_values_for_plot, X_test_df_for_shap, show=False)
            plt.title("SHAP Summary Plot for XGBoost Model")
            plt.show()
        except Exception as e:
            print(f"Error during SHAP value generation or plotting: {e}")
            print("Attempting KernelExplainer as fallback (slower)...")
            try:
                # Fallback to KernelExplainer if TreeExplainer fails or for non-tree models
                # KernelExplainer needs a background dataset (a sample of X_train_scaled)
                X_train_sample_shap = shap.sample(X_train_scaled, 100) # Sample 100 instances
                kernel_explainer = shap.KernelExplainer(xgb_model.predict_proba, X_train_sample_shap)
                shap_values_kernel = kernel_explainer.shap_values(X_test_scaled) # This will be a list [shap_class0, shap_class1]

                plt.figure()
                shap.summary_plot(shap_values_kernel[1], X_test_df_for_shap, show=False) # Plot for positive class
                plt.title("SHAP Summary Plot (KernelExplainer) for XGBoost Model - Positive Class")
                plt.show()
            except Exception as e_kernel:
                 print(f"Error during SHAP KernelExplainer: {e_kernel}")

    # 3. Churn Prevention Strategy (Conceptual - based on model outputs)
    # SQL Query for High-Risk Customers (Conceptual)
    # ```sql
    # SELECT Customer_ID, Outage_Count, Churn_Probability
    # FROM churn_predictions
    # WHERE Churn_Probability > 0.85;
    # ```
    # Python equivalent: Create a DataFrame with predictions
    churn_predictions_df = pd.DataFrame({
        'Customer_ID': X_test.index, # Assuming index holds Customer_ID or use a specific column
        'Churn_Probability': y_pred_proba_xgb
    })
    # Merge with original features if needed, e.g., Outage_Count
    # For demo, let's assume Customer_ID is in the index of X_test.
    # If X_test.index is not Customer_ID, you'd need to map it.
    # For now, we'll just show high-risk probabilities.
    high_risk_customers = churn_predictions_df[churn_predictions_df['Churn_Probability'] > 0.85]
    print("\nHigh-Risk Customers (Predicted Proba > 0.85):\n", high_risk_customers.head())

#-------------------------------------------------------------------------------
# PHASE 4: Deployment & Continuous Monitoring
#-------------------------------------------------------------------------------
print("\n\n--- PHASE 4: Deployment & Continuous Monitoring ---")

# 1. Model Deployment Strategy
# A. API Deployment (FastAPI Endpoint Definition)
# This code would typically be in a separate file (e.g., main_api_phase4.py)
# and run with `uvicorn main_api_phase4:app --reload`

# Placeholder features_df_columns, assuming it's the columns of X from Phase 3
# Global scope or loaded/defined here for the API.
# For this script, it's X.columns
API_FEATURE_COLUMNS = X.columns.tolist() if 'X' in locals() else []


def define_fastapi_app_phase4():
    from fastapi import FastAPI # Local import for this definition block
    import pandas as pd
    import joblib

    app_ph4 = FastAPI()

    # Load trained model and scaler
    try:
        model_ph4 = joblib.load("xgboost_churn_model_phase3.pkl")
        scaler_ph4 = joblib.load("scaler_phase3.pkl")
    except FileNotFoundError:
        print("API Error: Model or scaler file not found. Ensure they are saved from Phase 3.")
        model_ph4 = None
        scaler_ph4 = None

    @app_ph4.post("/predict_phase4/")
    def predict_churn_phase4(data: dict): # Expects a dict like {'Feature1': val1, ...}
        if not model_ph4 or not scaler_ph4:
            return {"error": "Model or scaler not loaded."}
        try:
            df = pd.DataFrame([data])
            # Ensure columns are in the same order as during training
            df_ordered = df[API_FEATURE_COLUMNS] # Use the saved feature order
            df_scaled = scaler_ph4.transform(df_ordered)
            prediction_proba = model_ph4.predict_proba(df_scaled)
            # Return probability of churn (class 1)
            return {"Churn_Probability": float(prediction_proba[0][1])}
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}

    print("\nFastAPI app for Phase 4 defined (app_ph4).")
    print("To run: save this FastAPI block to a file 'main_api_phase4.py' and run 'uvicorn main_api_phase4:app_ph4 --reload'")
    return app_ph4

app_phase4 = define_fastapi_app_phase4() # Define it, but won't run server in this script


# B. Power BI Dashboard Integration (Conceptual - SQL for data feed)
# ```sql
# SELECT Customer_ID, Churn_Probability, Last_Interaction_Date, Plan_Type
# FROM churn_predictions
# WHERE Last_Interaction_Date > CURRENT_DATE - INTERVAL '30 days';
# ```

# 2. Automated Alerts & Intervention Triggers (Conceptual)
# Power Automate flow described, not Python code.

# 3. A/B Testing for Retention Strategies (Conceptual - SQL for tracking)
# ```sql
# SELECT Strategy, COUNT(Customer_ID) AS Customers, AVG(Churn_Probability) AS Avg_Risk, Retention_Rate
# FROM retention_tests
# GROUP BY Strategy;
# ```

#-------------------------------------------------------------------------------
# PHASE 5: Model Optimization & Expansion
#-------------------------------------------------------------------------------
print("\n\n--- PHASE 5: Model Optimization & Expansion ---")

if 'X_train_scaled' not in locals() or 'y_train' not in locals():
    print("Skipping Phase 5 as training data from Phase 3 is not available.")
else:
    # 1. Model Optimization
    # A. Hyperparameter Tuning (Bayesian Optimization)
    if SKOPT_AVAILABLE:
        print("\nPerforming Bayesian Optimization for XGBoost...")
        param_space_xgb = {
            'n_estimators': Integer(50, 300),
            'max_depth': Integer(3, 10),
            'learning_rate': Real(0.01, 0.3, 'log-uniform'),
            'subsample': Real(0.6, 1.0, 'uniform'),
            'colsample_bytree': Real(0.6, 1.0, 'uniform')
        }
        xgb_for_bayes = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

        opt_bayes_xgb = BayesSearchCV(
            estimator=xgb_for_bayes,
            search_spaces=param_space_xgb,
            n_iter=10,  # Reduced iterations for faster demo
            cv=3,       # Reduced CV folds for faster demo
            scoring='roc_auc',
            n_jobs=-1,
            random_state=42
        )
        try:
            opt_bayes_xgb.fit(X_train_scaled, y_train)
            print(f"Best parameters found by BayesSearchCV: {opt_bayes_xgb.best_params_}")
            print(f"Best ROC AUC score from BayesSearchCV: {opt_bayes_xgb.best_score_}")
            optimized_xgb_model = opt_bayes_xgb.best_estimator_
            joblib.dump(optimized_xgb_model, "xgboost_optimized_phase5.pkl")
            print("Optimized XGBoost model saved as xgboost_optimized_phase5.pkl")
        except Exception as e:
            print(f"Bayesian Optimization failed: {e}")
            optimized_xgb_model = xgb_model # Fallback to previous model
    else:
        print("Skipping Bayesian Optimization as skopt is not available.")
        optimized_xgb_model = xgb_model # Fallback


    # B. Model Stacking (Ensemble Learning)
    if LGBM_AVAILABLE and 'optimized_xgb_model' in locals():
        print("\nBuilding and training Stacking Classifier...")
        # Base Models
        clf1_stack = optimized_xgb_model # Use the (potentially) optimized XGBoost
        clf2_stack = RandomForestClassifier(n_estimators=50, random_state=42) # Simpler RF for speed
        clf3_stack = LogisticRegression(solver='liblinear', random_state=42)

        # Meta-Model
        meta_learner_stack = LGBMClassifier(random_state=42)

        stacking_clf = StackingClassifier(
            estimators=[
                ('xgb', clf1_stack),
                ('rf', clf2_stack),
                ('lr', clf3_stack)
            ],
            final_estimator=meta_learner_stack,
            cv=3 # Reduced CV for speed
        )
        try:
            stacking_clf.fit(X_train_scaled, y_train) # Fit on scaled data
            joblib.dump(stacking_clf, "stacking_model_phase5.pkl")
            print("Stacking model saved as stacking_model_phase5.pkl")

            # Evaluate stacking_clf
            y_pred_stack = stacking_clf.predict(X_test_scaled)
            y_pred_proba_stack = stacking_clf.predict_proba(X_test_scaled)[:, 1]
            print("\nStacking Classifier Report:\n", classification_report(y_test, y_pred_stack))
            print("Stacking Classifier ROC AUC Score:", roc_auc_score(y_test, y_pred_proba_stack))
        except Exception as e:
            print(f"Stacking model training failed: {e}")
    else:
        print("Skipping Stacking model as LightGBM or optimized XGBoost is not available.")


    # C. Drift Detection & Auto-Retraining (Conceptual SQL shown in case study)
    print("\nDrift Detection: Conceptual. Monitoring would be set up in MLOps.")


    # 2. Expanding Beyond Churn: Cross-Sell & Upsell Predictions
    # A. Market Basket Analysis (Apriori Algorithm)
    if MLXTEND_AVAILABLE:
        print("\nPerforming Market Basket Analysis...")
        # Using transaction_mock DataFrame
        if not transaction_mock.empty:
            # Convert transactional data into binary format
            # One-hot encode items
            te = TransactionEncoder()
            te_ary = te.fit(transaction_mock.groupby('Customer_ID')['Product'].apply(list)).transform(transaction_mock.groupby('Customer_ID')['Product'].apply(list))
            market_basket_df = pd.DataFrame(te_ary, columns=te.columns_)

            if not market_basket_df.empty:
                # Generate frequent itemsets
                frequent_itemsets = apriori(market_basket_df, min_support=0.01, use_colnames=True) # Adjusted min_support for small mock data
                if not frequent_itemsets.empty:
                    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0) # Adjusted min_threshold
                    print("\nAssociation Rules (Top 5 by lift):\n", rules.sort_values('lift', ascending=False).head())
                else:
                    print("No frequent itemsets found with current support threshold.")
            else:
                print("Market basket DataFrame is empty after encoding.")
        else:
            print("Transaction data for Market Basket Analysis is empty.")
    else:
        print("Skipping Market Basket Analysis as mlxtend is not available.")


    # B. Dynamic Pricing Model (Conceptual Python function)
    def dynamic_pricing_offer_phase5(churn_probability, customer_lifetime_value):
        if churn_probability > 0.8:
            if customer_lifetime_value > 1000:
                 return "Offer premium retention package (e.g., 20% off + free add-on)"
            else:
                 return "Offer standard retention discount (e.g., 10% off) or plan downgrade option"
        elif churn_probability > 0.5:
            return "Offer personalized bundle or small incentive for early renewal"
        else:
            if customer_lifetime_value > 500:
                return "Recommend premium plan upgrade or complementary service"
            else:
                return "Nurture with loyalty rewards, no immediate pricing action"
        return "Default Offer" # Fallback

    # Example usage:
    example_churn_prob_dp = 0.85
    example_clv_dp = 1200
    offer = dynamic_pricing_offer_phase5(example_churn_prob_dp, example_clv_dp)
    print(f"\nDynamic Pricing Example (Churn Prob: {example_churn_prob_dp}, CLV: {example_clv_dp}): {offer}")


    # 3. AI-Driven Retention Strategies
    # A. Personalized Retention Emails (NLP-Based Sentiment Analysis)
    if TRANSFORMERS_AVAILABLE:
        print("\nPerforming NLP-based Sentiment Analysis for personalized emails...")
        try:
            sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            customer_feedback_example = "The service was too expensive, and I didn't find value."
            analyzed_sentiment = sentiment_analyzer(customer_feedback_example)
            print(f"Sentiment for feedback '{customer_feedback_example}': {analyzed_sentiment}")

            # Based on sentiment, tailor email (conceptual)
            if analyzed_sentiment[0]['label'] == 'NEGATIVE' and "expensive" in customer_feedback_example.lower():
               email_content_idea = "Focus on value proposition, offer a discount or a more suitable plan."
            else:
               email_content_idea = "Standard engagement or positive reinforcement email."
            print(f"Email idea: {email_content_idea}")
        except Exception as e:
            print(f"Error during Transformers sentiment analysis: {e}. Ensure model is downloaded or internet is available.")
    else:
        print("Skipping NLP Sentiment Analysis as Transformers library is not available.")


#-------------------------------------------------------------------------------
# PHASE 6: Full Business Integration & Scaling
#-------------------------------------------------------------------------------
print("\n\n--- PHASE 6: Full Business Integration & Scaling ---")

# 1. Enterprise-Wide Model Deployment
# A. API Integration for Real-Time Predictions (Refined FastAPI Endpoint)
# This would use the best model from Phase 5 (e.g., stacking_model_phase5.pkl or xgboost_optimized_phase5.pkl)

# Global scope or loaded/defined here for the API.
# For this script, it's X.columns
API_FEATURE_COLUMNS_PH6 = X.columns.tolist() if 'X' in locals() else []


def define_fastapi_app_phase6():
    from fastapi import FastAPI # Local import for this definition block
    import pandas as pd
    import joblib

    app_ph6 = FastAPI()

    # Load the best model and corresponding scaler
    try:
        # Try loading stacking model first, fallback to optimized XGBoost, then original XGBoost
        if Path("stacking_model_phase5.pkl").exists():
            model_ph6 = joblib.load("stacking_model_phase5.pkl")
            print("API (Phase 6) using: stacking_model_phase5.pkl")
        elif Path("xgboost_optimized_phase5.pkl").exists():
            model_ph6 = joblib.load("xgboost_optimized_phase5.pkl")
            print("API (Phase 6) using: xgboost_optimized_phase5.pkl")
        elif Path("xgboost_churn_model_phase3.pkl").exists():
            model_ph6 = joblib.load("xgboost_churn_model_phase3.pkl")
            print("API (Phase 6) using: xgboost_churn_model_phase3.pkl")
        else:
            raise FileNotFoundError("No suitable model file found for Phase 6 API.")

        scaler_ph6 = joblib.load("scaler_phase3.pkl") # Assuming same scaler is used
    except FileNotFoundError as e:
        print(f"API Error (Phase 6): {e}")
        model_ph6 = None
        scaler_ph6 = None
    except Exception as e: # Catch other joblib/loading errors
        print(f"API Error (Phase 6) during model/scaler loading: {e}")
        model_ph6 = None
        scaler_ph6 = None


    @app_ph6.post("/predict_churn_v2_phase6")
    def predict_churn_enterprise_phase6(data: dict):
        if not model_ph6 or not scaler_ph6:
            return {"error": "Model or scaler not loaded for Phase 6 API."}
        try:
            # Basic input validation
            if not all(feature in data for feature in API_FEATURE_COLUMNS_PH6):
                 missing_feats = [f for f in API_FEATURE_COLUMNS_PH6 if f not in data]
                 return {"error": f"Missing required features: {missing_feats}"}

            df = pd.DataFrame([data])
            df_ordered = df[API_FEATURE_COLUMNS_PH6]
            df_scaled = scaler_ph6.transform(df_ordered)
            prediction_proba = model_ph6.predict_proba(df_scaled)[:, 1]

            # Get top drivers (conceptual, SHAP would be more involved for real-time API)
            # For a simple proxy, one could use feature importances from the model if available
            # or a simplified rule based on input values for demo
            top_drivers_mock = []
            if data.get('Outage_Count', 0) > 3: top_drivers_mock.append("High Outage Count")
            if data.get('Sentiment_Score', 0) < -0.5: top_drivers_mock.append("Negative Sentiment")
            if data.get('Months_Since_Upgrade', 0) > 12: top_drivers_mock.append("Outdated Plan")


            return {
                "customer_id": data.get("Customer_ID", "N/A"), # Assuming Customer_ID might be passed
                "churn_probability": float(prediction_proba[0]),
                "top_drivers": top_drivers_mock if top_drivers_mock else ["General Risk Factors"]
            }
        except KeyError as e: # Specifically catch missing keys if API_FEATURE_COLUMNS_PH6 is not perfectly aligned
            return {"error": f"Missing feature in input data for API: {str(e)}"}
        except Exception as e:
            return {"error": f"Prediction error in Phase 6 API: {str(e)}"}

    print("\nFastAPI app for Phase 6 defined (app_ph6).")
    print("To run: save this FastAPI block to 'main_api_phase6.py' and run 'uvicorn main_api_phase6:app_ph6 --reload'")
    return app_ph6

# Define the app, but don't run the server
from pathlib import Path # Used in define_fastapi_app_phase6
app_phase6 = define_fastapi_app_phase6()


# 2. Real-Time Customer Intervention System
# B. AI-Driven Customer Support Chatbots (Conceptual Python Logic)
def chatbot_response_logic_phase6(customer_id, customer_message, churn_data_from_api):
    # churn_data_from_api = {'churn_probability': prob, 'top_drivers': [...]}
    # intent = analyze_intent(customer_message) # Assume intent analysis is done

    intent = "cancel_service" if "cancel" in customer_message.lower() else "tech_support" # Simplified intent

    if intent == "cancel_service" and churn_data_from_api['churn_probability'] > 0.7:
        if "Price" in churn_data_from_api.get('top_drivers', []): # Check if top_drivers exists
            return "I see you're looking to cancel. We value you as a customer. Can I offer you a special 15% loyalty discount to stay with us?"
        else:
            return "I'm sorry to hear that. Before processing, could I interest you in a quick chat with our retention specialists to see if we can find a better solution for you?"
    elif intent == "tech_support" and churn_data_from_api['churn_probability'] > 0.5:
        return "Let's resolve your technical issue... (After resolution) ...By the way, have you considered our Premium Support package for faster assistance?"
    else:
        return "Standard bot response for the intent."

# Example usage:
example_churn_api_response = {"churn_probability": 0.85, "top_drivers": ["Price", "High Outage Count"]}
chat_response = chatbot_response_logic_phase6("customer123", "I want to cancel my subscription.", example_churn_api_response)
print(f"\nChatbot example response: {chat_response}")


# 3. Dynamic Customer Segmentation for Targeted Campaigns (K-Means)
print("\nPerforming K-Means Clustering for Dynamic Customer Segmentation...")
# Using X_scaled (all available customers after scaling) if available, otherwise X_train_scaled for demo
if 'X_scaled' in locals() and not X_scaled.empty: # If full dataset was scaled
    data_for_clustering = X_scaled
elif 'X_train_scaled' in locals() and not X_train_scaled.empty:
    data_for_clustering = X_train_scaled # Use training data as proxy
    print("Using X_train_scaled for K-Means clustering demo.")
else:
    data_for_clustering = None
    print("Skipping K-Means clustering as no suitable scaled data is available.")

if data_for_clustering is not None:
    try:
        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto') # e.g., High, Medium, Loyal segments
        customer_segments_labels = kmeans.fit_predict(data_for_clustering)
        print(f"K-Means clustering complete. Example segment labels (first 10): {customer_segments_labels[:10]}")
        # In a real scenario, you'd map these labels back to Customer_IDs and analyze segment characteristics.
        # Example: pd.Series(customer_segments_labels).value_counts()
    except Exception as e:
        print(f"Error during K-Means clustering: {e}")


# 4. Full Upsell & Cross-Sell Implementation
# A. Personalized Product Recommendations (Conceptual Python function)
def get_product_recommendation_phase6(customer_id, churn_probability, current_products_list, purchase_history_list):
    if churn_probability > 0.75:
        return "Recommend retention offer (e.g., discount on current plan) or suggest a more basic/affordable plan."
    elif churn_probability < 0.3:
        # This would integrate with Market Basket rules or collaborative filtering outputs
        if "ProductA" in current_products_list and "ServiceX" not in current_products_list: # Example rule
            return "Recommend ServiceX as a complementary service to ProductA."
        else:
            return "Promote premium add-ons or upgrade to a higher-tier plan based on usage profile."
    else: # Medium risk
        return "Focus on engagement with current products, reinforce value proposition."

# Example usage:
rec_ph6 = get_product_recommendation_phase6("cust789", 0.2, ["ProductA"], ["ProductA", "OldService"])
print(f"\nProduct Recommendation example: {rec_ph6}")


# B. AI-Powered Dynamic Pricing Model (Conceptual Python function)
def get_dynamic_offer_phase6(customer_profile_dict, churn_prob, clv_estimate, market_conditions_dict):
    base_product_price = customer_profile_dict.get('current_plan_price', 100) # Example
    discount_percentage = 0

    if churn_prob > 0.7:
        discount_percentage += 10
        if clv_estimate > 1000:
            discount_percentage += 10
    elif churn_prob < 0.2 and clv_estimate > 1500:
        return f"Offer premium product suite at {base_product_price * 1.2} (Value-added services)." # Upsell

    if market_conditions_dict.get('competitor_offering_discount', False):
       discount_percentage = max(discount_percentage, 15)

    final_price = base_product_price * (1 - discount_percentage / 100)
    return f"Offer product at {final_price:.2f} (Original: {base_product_price}, Discount: {discount_percentage}%)"

# Example usage:
example_profile = {'current_plan_price': 50}
example_market_conditions = {'competitor_offering_discount': True}
dynamic_offer_ph6 = get_dynamic_offer_phase6(example_profile, 0.75, 1200, example_market_conditions)
print(f"\nDynamic Offer example: {dynamic_offer_ph6}")


# 5. Auto-Retraining & Model Governance (Conceptual - MLOps pipelines would handle this)
# SQL for drift detection example:
# ```sql
# SELECT AVG(predicted_probability) - AVG(actual_churn)
# FROM churn_predictions
# WHERE date >= CURRENT_DATE - INTERVAL '30 days';
# ```
print("\nAuto-Retraining & Model Governance: MLOps pipelines would be implemented here.")


print("\n\n--- ALL PHASES COMPLETED (Python Code Execution) ---")
