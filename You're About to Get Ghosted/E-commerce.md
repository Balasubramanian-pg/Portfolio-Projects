Okay, here is the complete Jupyter Notebook structure as a single runnable script. Remember to have the `2019-Oct.csv` file in the same directory as your notebook, or update the path accordingly.

```python
# %%
"""
# 📊 Advanced Customer Analytics: Statistical Analysis of E-Commerce Behavior
### A Data Science Portfolio Project

![Analytics Banner](https://img.shields.io/badge/Portfolio-E--Commerce%20Analytics-blue?style=for-the-badge&logo=jupyter)

**Author:** [Your Name]  
**LinkedIn:** [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/yourprofile)  
**GitHub:** [![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/yourusername)  
**Last Updated:** May 2025
"""

# %%
"""
## 🎯 Problem Statement

In today's competitive e-commerce landscape, understanding customer behavior patterns is critical for business success. This project applies advanced statistical methods to analyze customer interactions, predict churn, identify behavioral segments, and optimize business strategies.

### Key Objectives:
1. 📉 Predict customer churn using survival analysis techniques
2. 🗓️ Decompose time series data to understand seasonal purchasing patterns
3. 👥 Segment customers using advanced clustering methods (Note: Clustering itself is not explicitly in the provided code, but PCA sets up for it)
4. 📊 Apply Bayesian methods to quantify uncertainty in A/B testing results

### Dataset Overview:
The dataset contains over 7.5 million records of e-commerce transactions for October 2019 across multiple product categories. Each record represents a customer event (view, cart, purchase) with associated metadata. (Adjusted based on filename)

Dataset Source: [E-commerce Behavior Data from Multi Category Store](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store) (Using 2019-Oct.csv from this source)
"""

# %%
"""
## 🛠️ Setup and Environment Configuration
"""

# Standard data manipulation and visualization libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical libraries
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
import statsmodels.formula.api as smf
from statsmodels.stats.power import TTestIndPower
import pymc as pm  # For Bayesian analysis

# Survival analysis
from lifelines import KaplanMeierFitter, CoxPHFitter

# Machine learning (PCA is used, clustering libraries imported but not used in provided snippets)
from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans, DBSCAN  # Imported but not used in provided snippets
# from sklearn.mixture import GaussianMixture # Imported but not used in provided snippets
from sklearn.decomposition import PCA
# from sklearn.pipeline import Pipeline # Imported but not used in provided snippets

# Advanced visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Notebook styling
from IPython.display import HTML, display
import warnings
warnings.filterwarnings('ignore')

# Custom styling for plots
plt.style.use('seaborn-v0_8-whitegrid')
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="whitegrid", rc=custom_params)

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# Custom color palette
palette = sns.color_palette("viridis", 10)
sns.set_palette(palette)

# Add custom theme styling
display(HTML("""
<style>
    div.cell {
        margin-bottom: 20px;
    }
    div.text_cell_render h1 {
        font-size: 35px;
        color: #447AAB;
    }
    div.text_cell_render h2 {
        font-size: 30px;
        color: #447AAB;
    }
    div.text_cell_render h3 {
        font-size: 25px;
        font-style: italic;
        color: #447AAB;
    }
    .rendered_html table {
        font-size: 14px;
    }
</style>
"""))

# %%
"""
## 📥 Data Loading and Preparation
This section handles the import, cleaning, and transformation of the raw e-commerce event data.
"""

# %%
def load_ecommerce_data(filepath):
    """
    Load the e-commerce events dataset and perform initial processing.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV data file
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataframe
    """
    # Load the data
    # For demonstration, we might use a sample if the full dataset is too large for quick iteration
    # df = pd.read_csv(filepath, nrows=1000000) # Example: load first 1M rows
    df = pd.read_csv(filepath)
    
    # Display basic information
    print(f"Dataset dimensions: {df.shape}")
    print(f"Memory usage: {df.memory_usage().sum() / 1e6:.2f} MB")
    
    return df

# Load the dataset - replace '2019-Oct.csv' with your actual file path if different
# Ensure the CSV file is in the same directory as this notebook or provide the full path.
try:
    df = load_ecommerce_data('2019-Oct.csv')
except FileNotFoundError:
    print("Error: '2019-Oct.csv' not found. Please ensure the file is in the correct directory or update the path.")
    # Create a dummy dataframe for the rest of the notebook to run without error, if desired
    # For now, we'll let it error out if file not found.
    # df = pd.DataFrame() # Or exit
    raise

# %%
# Display the first few rows and basic information
display(df.head())
df.info(show_counts=True) # show_counts=True to show non-null counts explicitly

# %%
"""
### 🧹 Data Cleaning
"""

# %%
def clean_data(df_raw):
    """
    Clean the e-commerce dataset by handling missing values,
    converting data types, and creating derived features.
    
    Parameters:
    -----------
    df_raw : pd.DataFrame
        Raw dataframe
        
    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe with derived features
    """
    # Make a copy to avoid modifying the original
    df_clean = df_raw.copy()
    
    # Convert timestamp to datetime
    df_clean['event_time'] = pd.to_datetime(df_clean['event_time'])
    
    # Extract date components
    df_clean['date'] = df_clean['event_time'].dt.date
    df_clean['hour'] = df_clean['event_time'].dt.hour
    df_clean['day_of_week'] = df_clean['event_time'].dt.dayofweek # Monday=0, Sunday=6
    df_clean['is_weekend'] = df_clean['day_of_week'].isin([5, 6]).astype(int)
    
    # Handle missing values
    print("Missing values before cleaning:")
    for col in df_clean.columns:
        if df_clean[col].isna().sum() > 0:
            print(f"Column '{col}' has {df_clean[col].isna().sum()} missing values ({df_clean[col].isna().mean()*100:.2f}%).")
    
    # Drop rows with missing values in critical columns (user_id, product_id, event_type)
    # These are essential for almost all analyses.
    critical_cols = ['user_id', 'product_id', 'event_type']
    df_clean = df_clean.dropna(subset=critical_cols)
    print(f"\nShape after dropping NaNs in critical columns: {df_clean.shape}")

    # Impute 'brand' and 'category_code' with 'Unknown' if they are objects/strings
    # If they are numerical, other strategies might be needed. Let's check types.
    if 'brand' in df_clean.columns and df_clean['brand'].dtype == 'object':
        df_clean['brand'] = df_clean['brand'].fillna('Unknown')
    if 'category_code' in df_clean.columns and df_clean['category_code'].dtype == 'object':
        df_clean['category_code'] = df_clean['category_code'].fillna('Unknown')

    # For 'price', negative values are likely errors.
    # If present, decide on a strategy (e.g., remove, impute with median of product/category)
    # For now, we'll assume positive prices. If not, this is a point for further EDA.
    if (df_clean['price'] <= 0).any():
        print(f"Warning: Found {(df_clean['price'] <= 0).sum()} non-positive prices.")
        # df_clean = df_clean[df_clean['price'] > 0] # Option: remove them

    # Create price buckets (handle potential errors with qcut if price has low variance or many NaNs)
    # Ensure price has no NaNs before qcut, or qcut will fail.
    # We'll only bucket non-NaN prices for products involved in view, cart, or purchase events.
    if df_clean['price'].notna().sum() > 0: # Check if there are any non-NaN prices
        try:
            # Create a temporary series for qcut without NaNs to avoid errors
            valid_prices = df_clean.loc[df_clean['price'].notna(), 'price']
            if len(valid_prices.unique()) >= 5: # qcut needs enough unique values for quantiles
                 df_clean['price_bucket'] = pd.qcut(df_clean['price'], q=5, 
                                                   labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                                                   duplicates='drop') # Drop duplicate bin edges
            else:
                df_clean['price_bucket'] = pd.cut(df_clean['price'], bins=5,
                                                 labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                                                 duplicates='drop')
        except ValueError as e:
            print(f"Could not create price_bucket due to: {e}. Skipping price_bucket.")
            df_clean['price_bucket'] = 'N/A' # Placeholder
    else:
        df_clean['price_bucket'] = 'N/A' # Placeholder if no price data

    # Create user engagement features
    user_engagement_actions = df_clean.groupby('user_id').agg(
        event_count=('event_type', 'count'),
        unique_products_interacted=('product_id', 'nunique'), # Renamed for clarity
        first_activity=('event_time', 'min'),
        last_activity=('event_time', 'max')
    )
    
    # Calculate total spent per user
    purchases_df = df_clean[df_clean['event_type'] == 'purchase']
    user_total_spent = purchases_df.groupby('user_id')['price'].sum().rename('total_spent')
    user_engagement = user_engagement_actions.join(user_total_spent, how='left').fillna({'total_spent': 0})

    # Calculate user lifetime in days
    user_engagement['lifetime_days'] = (user_engagement['last_activity'] - 
                                        user_engagement['first_activity']).dt.total_seconds() / (60*60*24)
    
    # Calculate purchase conversion rate (per user)
    event_type_counts_user = df_clean.groupby(['user_id', 'event_type']).size().unstack(fill_value=0)
    
    # Ensure 'purchase' and 'view' columns exist
    if 'purchase' not in event_type_counts_user.columns:
        event_type_counts_user['purchase'] = 0
    if 'view' not in event_type_counts_user.columns:
        event_type_counts_user['view'] = 0
        
    all_users = pd.DataFrame(index=df_clean['user_id'].unique())
    all_users = all_users.join(event_type_counts_user.rename(columns={'purchase': 'purchase_count_user', 'view': 'view_count_user'}))
    all_users = all_users.fillna({'purchase_count_user': 0, 'view_count_user': 0}) # Fill NaNs for users with no views/purchases

    all_users['conversion_rate'] = np.where(all_users['view_count_user'] > 0, 
                                           all_users['purchase_count_user'] / all_users['view_count_user'], 
                                           0)
    
    # Merge user engagement metrics back to the main dataframe
    df_clean = df_clean.merge(user_engagement, on='user_id', how='left')
    df_clean = df_clean.merge(all_users[['conversion_rate']], left_on='user_id', right_index=True, how='left')
    
    print(f"\nShape after cleaning and adding initial user features: {df_clean.shape}")
    return df_clean

# %%
# Apply the cleaning function
df_clean = clean_data(df)

# %%
# Display summary of the cleaned data
print("\nCleaned dataset summary (df_clean):")
display(df_clean.describe(include='all', datetime_is_numeric=True).T)
print("\nMissing values after cleaning (df_clean):")
display(df_clean.isnull().sum())

# %%
"""
### 🏭 Feature Engineering
Further feature engineering based on the cleaned data.
"""

# %%
def engineer_features(df_to_eng):
    """
    Create advanced features for statistical analysis.
    
    Parameters:
    -----------
    df_to_eng : pd.DataFrame
        Cleaned dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with additional engineered features
    """
    # Create a copy to avoid modifying the input
    df_eng = df_to_eng.copy()
    
    # Create user behavior sequence aggregates (already partially done in clean_data, can be expanded)
    # Daily event counts per user (example, might be too granular for some analyses)
    # user_daily_events = df_eng.groupby(['user_id', 'date']).agg(
    #     daily_views=('event_type', lambda x: sum(x == 'view')),
    #     daily_carts=('event_type', lambda x: sum(x == 'cart')),
    #     daily_purchases=('event_type', lambda x: sum(x == 'purchase')),
    #     daily_spend=('price', lambda x: sum(x[df_eng.loc[x.index, 'event_type'] == 'purchase']))
    # ).reset_index()
    # df_eng = df_eng.merge(user_daily_events, on=['user_id', 'date'], how='left') # This would increase df size
    
    # Calculate time between events for each user
    df_eng = df_eng.sort_values(['user_id', 'event_time'])
    df_eng['prev_event_time'] = df_eng.groupby('user_id')['event_time'].shift(1)
    df_eng['time_since_last_event_minutes'] = (df_eng['event_time'] - df_eng['prev_event_time']).dt.total_seconds() / 60
    df_eng['time_since_last_event_minutes'] = df_eng['time_since_last_event_minutes'].fillna(0) # First event has 0 time since last

    # Identify returning customers (purchased on more than one day)
    user_purchase_dates = df_eng[df_eng['event_type'] == 'purchase'].groupby('user_id')['date'].nunique()
    returning_customer_ids = user_purchase_dates[user_purchase_dates > 1].index
    df_eng['is_returning_customer'] = df_eng['user_id'].isin(returning_customer_ids).astype(int)
    
    # Brand and category engagement (per user)
    # Favorite brand/category based on total interactions (views, carts, purchases)
    # This can be computationally intensive for large datasets if many brands/categories
    if 'brand' in df_eng.columns and df_eng['brand'].nunique() > 1:
        user_top_brand = df_eng.groupby('user_id')['brand'].apply(lambda x: x.mode()[0] if not x.mode().empty else 'N/A').reset_index()
        user_top_brand.columns = ['user_id', 'favorite_brand']
        df_eng = df_eng.merge(user_top_brand, on='user_id', how='left')
    
    if 'category_code' in df_eng.columns and df_eng['category_code'].nunique() > 1:
        user_top_category = df_eng.groupby('user_id')['category_code'].apply(lambda x: x.mode()[0] if not x.mode().empty else 'N/A').reset_index()
        user_top_category.columns = ['user_id', 'favorite_category']
        df_eng = df_eng.merge(user_top_category, on='user_id', how='left')
    
    # Time-based features (already created: hour, day_of_week, is_weekend)
    # Additional ones for time series context:
    df_eng['month'] = df_eng['event_time'].dt.month # All data is from Oct, so this will be 10
    df_eng['day'] = df_eng['event_time'].dt.day
    try: # isocalendar().week can fail on pandas < 1.1.0 or with certain date issues
      df_eng['week_of_year'] = df_eng['event_time'].dt.isocalendar().week.astype(int)
    except AttributeError:
      df_eng['week_of_year'] = df_eng['event_time'].dt.strftime('%U').astype(int) # Alternative week calculation

    # Purchase funnel progression (per user)
    # Did a user who viewed/carted eventually purchase *anything* in their history?
    # 'reached_purchase' could mean if any purchase event exists for the user.
    # A more sophisticated funnel would track sequences product by product.
    user_has_purchased = df_eng[df_eng['event_type'] == 'purchase']['user_id'].unique()
    df_eng['reached_purchase_ever'] = df_eng['user_id'].isin(user_has_purchased).astype(int)
    
    print(f"Shape after feature engineering: {df_eng.shape}")
    return df_eng

# %%
# Apply feature engineering
df_final = engineer_features(df_clean)

# %%
# Display sample of the engineered features and their summary
print("\nSample of final engineered data (df_final):")
cols_to_show = ['user_id', 'event_time', 'event_type', 'price', 'brand', 'category_code',
                'conversion_rate', 'is_returning_customer', 'is_weekend', 
                'time_since_last_event_minutes', 'favorite_brand', 'favorite_category', 'reached_purchase_ever']
# Filter for columns that exist in df_final to avoid KeyError
cols_to_show = [col for col in cols_to_show if col in df_final.columns]
display(df_final[cols_to_show].head(10))

print("\nFinal dataset summary (df_final):")
display(df_final.describe(include='all', datetime_is_numeric=True).T)
print("\nMissing values in final dataset (df_final):")
display(df_final.isnull().sum())

# %%
"""
## 🔍 Exploratory Data Analysis
This section explores the relationships and patterns in the e-commerce data through visualizations and summary statistics.
"""

# %%
"""
### 📊 Basic Distribution Analysis
"""

# %%
def plot_event_distribution(df_eda):
    """
    Visualize the distribution of event types in the dataset.
    
    Parameters:
    -----------
    df_eda : pd.DataFrame
        Processed dataframe
    """
    if df_eda.empty:
        print("Dataframe is empty, skipping event distribution plot.")
        return
        
    # Count events by type
    event_counts = df_eda['event_type'].value_counts().reset_index()
    event_counts.columns = ['Event Type', 'Count']
    
    # Calculate percentages
    total = event_counts['Count'].sum()
    event_counts['Percentage'] = (event_counts['Count'] / total * 100).round(2)
    
    # Create figure with two subplots
    fig = make_subplots(rows=1, cols=2, 
                        specs=[[{"type": "bar"}, {"type": "pie"}]],
                        subplot_titles=("Event Count Distribution", "Event Percentage"))
    
    # Add bar chart
    fig.add_trace(
        go.Bar(
            x=event_counts['Event Type'],
            y=event_counts['Count'],
            text=event_counts['Count'],
            textposition='auto',
            marker_color=['#FFA15A', '#19D3F3', '#FF6692'] # Colors for view, cart, purchase
        ),
        row=1, col=1
    )
    
    # Add pie chart
    fig.add_trace(
        go.Pie(
            labels=event_counts['Event Type'],
            values=event_counts['Percentage'],
            textinfo='label+percent',
            hole=0.4,
            marker=dict(colors=['#FFA15A', '#19D3F3', '#FF6692'])
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        width=1000,
        title_text="E-Commerce Event Distribution",
        showlegend=False,
    )
    
    fig.show()

# %%
# Plot event type distribution
plot_event_distribution(df_final)

# %%
"""
### 🕒 Event Timing Analysis
"""

# %%
def analyze_event_timing(df_eda):
    """
    Analyze how events are distributed across time dimensions.
    
    Parameters:
    -----------
    df_eda : pd.DataFrame
        Processed dataframe with time features
    """
    if df_eda.empty:
        print("Dataframe is empty, skipping event timing analysis.")
        return

    # Hourly distribution
    hourly_events = df_eda.groupby(['hour', 'event_type']).size().unstack().fillna(0)
    
    # Daily distribution
    daily_events = df_eda.groupby(['day_of_week', 'event_type']).size().unstack().fillna(0)
    daily_events.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] # Adjusted for brevity
    
    # Plot hourly and daily distributions
    plt.figure(figsize=(16, 7))
    
    plt.subplot(1, 2, 1)
    sns.heatmap(hourly_events, cmap='viridis', annot=False, fmt="d") # Annot might be too cluttered
    plt.title('Event Distribution by Hour of Day')
    plt.xlabel('Event Type')
    plt.ylabel('Hour of Day (0-23)')
    
    plt.subplot(1, 2, 2)
    sns.heatmap(daily_events, cmap='viridis', annot=False, fmt="d")
    plt.title('Event Distribution by Day of Week')
    plt.xlabel('Event Type')
    plt.ylabel('Day of Week')
    
    plt.tight_layout()
    plt.show()
    
    # Interactive time series visualization of daily event counts
    # Ensure 'date' column is datetime.date, convert to datetime for Plotly if needed
    df_eda['date_dt'] = pd.to_datetime(df_eda['date'])
    daily_time_series = df_eda.groupby(['date_dt', 'event_type']).size().unstack().fillna(0).reset_index()
    
    event_types_present = [col for col in ['view', 'cart', 'purchase'] if col in daily_time_series.columns]
    if not event_types_present:
        print("No standard event types (view, cart, purchase) found for daily time series plot.")
        return

    fig = px.line(daily_time_series, x='date_dt', y=event_types_present,
                 title='Daily Event Count Over Time',
                 labels={'value': 'Event Count', 'variable': 'Event Type', 'date_dt': 'Date'},
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    
    fig.update_layout(
        height=500,
        width=1000,
        legend_title='Event Type',
        hovermode='x unified'
    )
    
    fig.show()

# %%
# Analyze timing patterns
analyze_event_timing(df_final)

# %%
"""
### 💰 Price Analysis
"""

# %%
def analyze_price_patterns(df_eda):
    """
    Analyze pricing patterns and their relationship with user behavior.
    
    Parameters:
    -----------
    df_eda : pd.DataFrame
        Processed dataframe
    """
    if df_eda.empty or 'price' not in df_eda.columns:
        print("Dataframe is empty or 'price' column missing, skipping price analysis.")
        return

    # Price distribution by event type
    plt.figure(figsize=(16, 7))
    
    plt.subplot(1, 2, 1)
    # Filter out extreme outliers for better visualization if necessary, or use log scale carefully
    sns.histplot(data=df_eda, x='price', hue='event_type', element='step', log_scale=True, bins=50, common_norm=False)
    plt.title('Price Distribution by Event Type (Log Scale)')
    plt.xlabel('Price (Log Scale)')
    plt.ylabel('Count')
    
    plt.subplot(1, 2, 2)
    # For boxplot, consider removing extreme outliers if they skew the plot too much
    # Or use showfliers=False
    sns.boxplot(data=df_eda, x='event_type', y='price', palette='viridis', showfliers=False) # Hiding fliers for clarity
    plt.title('Price Distribution by Event Type (Outliers Hidden)')
    plt.xlabel('Event Type')
    plt.ylabel('Price')
    # plt.yscale('log') # Log scale can be useful if ranges are vast
    
    plt.tight_layout()
    plt.show()
    
    # Conversion rate by price bucket
    if 'price_bucket' in df_eda.columns and df_eda['price_bucket'].nunique() > 1:
        # Ensure 'view' and 'purchase' events are present for calculation
        event_counts_by_bucket = df_eda.groupby(['price_bucket', 'event_type'], observed=True).size().unstack(fill_value=0)

        if 'view' in event_counts_by_bucket.columns and 'purchase' in event_counts_by_bucket.columns:
            conversion_by_price = pd.DataFrame()
            conversion_by_price['view_count'] = event_counts_by_bucket['view']
            conversion_by_price['purchase_count'] = event_counts_by_bucket['purchase']
            
            conversion_by_price['conversion_rate'] = np.where(
                conversion_by_price['view_count'] > 0,
                (conversion_by_price['purchase_count'] / conversion_by_price['view_count'] * 100),
                0
            ).round(2)
            
            # Plot conversion rate by price
            fig = px.bar(conversion_by_price.reset_index(), 
                        x='price_bucket', 
                        y='conversion_rate',
                        title='Conversion Rate (Purchase/View) by Price Range',
                        labels={'price_bucket': 'Price Range', 'conversion_rate': 'Conversion Rate (%)'},
                        text='conversion_rate',
                        color='conversion_rate',
                        color_continuous_scale='viridis')
            
            fig.update_layout(
                height=500,
                width=800,
                xaxis_title='Price Range',
                yaxis_title='Conversion Rate (%)',
                coloraxis_showscale=False
            )
            fig.show()
        else:
            print("Could not calculate conversion rate by price bucket: 'view' or 'purchase' events missing in aggregation.")
    else:
        print("Skipping conversion rate by price_bucket: 'price_bucket' not available or has insufficient unique values.")

# %%
# Analyze price patterns
analyze_price_patterns(df_final)

# %%
"""
### 👥 User Behavior Analysis
"""

# %%
def analyze_user_behavior(df_eda):
    """
    Analyze user engagement and behavior patterns.
    
    Parameters:
    -----------
    df_eda : pd.DataFrame
        Processed dataframe with user metrics
    """
    if df_eda.empty or 'user_id' not in df_eda.columns:
        print("Dataframe is empty or 'user_id' column missing, skipping user behavior analysis.")
        return

    # Create user-level dataset
    # Some user features might already be on df_eda (e.g., conversion_rate, lifetime_days)
    # We'll aggregate or take first for user-level summary
    
    user_event_counts = df_eda.groupby(['user_id', 'event_type']).size().unstack(fill_value=0)
    user_event_counts.columns = [f"{col}_count" for col in user_event_counts.columns] # e.g. view_count
    
    # Ensure standard columns exist
    for event_col in ['view_count', 'cart_count', 'purchase_count']:
        if event_col not in user_event_counts.columns:
            user_event_counts[event_col] = 0

    user_data_agg = {
        'event_count_total': ('event_type', 'count'), # Total events per user
        'conversion_rate_user': ('conversion_rate', 'first'), # User's overall conversion rate
        'is_returning_user': ('is_returning_customer', 'first'),
        'lifetime_days_user': ('lifetime_days', 'first'),
        'total_spent_user': ('total_spent', 'first') # total_spent was precalculated
    }
    
    # Additional aggregations if columns exist
    if 'time_since_last_event_minutes' in df_eda.columns:
      user_data_agg['avg_time_between_events_user'] = ('time_since_last_event_minutes', lambda x: x[x>0].mean()) # Avg for non-first events


    user_summary = df_eda.groupby('user_id').agg(**user_data_agg)
    user_summary = user_summary.join(user_event_counts, how='left').reset_index()
    
    # Fill NaNs that might result from 'first' if a user has only one entry or specific features are NaN
    user_summary.fillna({'conversion_rate_user': 0, 'total_spent_user': 0, 'lifetime_days_user': 0}, inplace=True)
    
    # Calculate purchase frequency
    user_summary['purchase_frequency_user'] = np.where(
        user_summary['lifetime_days_user'] > 0,
        user_summary['purchase_count'] / user_summary['lifetime_days_user'],
        0
    )
    
    # User engagement distribution
    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"type": "histogram"}, {"type": "histogram"}],
                               [{"type": "histogram"}, {"type": "scatter"}]],
                        subplot_titles=("Distribution of Total Events per User", 
                                        "Distribution of User Conversion Rates",
                                        "User Total Spend Distribution",
                                        "User Purchase Count vs. View Count"))
    
    # Events per user
    fig.add_trace(
        go.Histogram(x=user_summary['event_count_total'].clip(upper=user_summary['event_count_total'].quantile(0.99)), # Clip for viz
                    nbinsx=50, 
                    marker_color='#636EFA',
                    name="Events per User"),
        row=1, col=1
    )
    
    # Conversion rate distribution (for users with views)
    fig.add_trace(
        go.Histogram(x=user_summary[user_summary['view_count'] > 0]['conversion_rate_user'],
                    nbinsx=50,
                    marker_color='#EF553B',
                    name="Conversion Rate"),
        row=1, col=2
    )
    
    # Total spend distribution (for users with purchases)
    fig.add_trace(
        go.Histogram(x=user_summary[user_summary['purchase_count'] > 0]['total_spent_user'].clip(upper=user_summary['total_spent_user'].quantile(0.99)), # Clip for viz
                    nbinsx=50,
                    marker_color='#00CC96',
                    name="Total Spend"),
        row=2, col=1
    )
    
    # Purchase vs. view scatter (sample if too many points)
    sample_user_summary = user_summary.sample(min(len(user_summary), 50000), random_state=42)
    fig.add_trace(
        go.Scatter(x=sample_user_summary['view_count'],
                  y=sample_user_summary['purchase_count'],
                  mode='markers',
                  marker=dict(
                      color=sample_user_summary['conversion_rate_user'],
                      colorscale='Viridis',
                      size=5, # Smaller size for many points
                      opacity=0.5,
                      showscale=True,
                      colorbar=dict(title="Conv. Rate")
                  ),
                  name="Purchase vs View"),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        width=1000,
        title_text="User Behavior Analysis (Aggregated per User)",
        showlegend=False,
    )
    
    fig.update_xaxes(title_text="Number of Events (Clipped)", row=1, col=1)
    fig.update_xaxes(title_text="Conversion Rate", row=1, col=2)
    fig.update_xaxes(title_text="Total Spend (Clipped)", row=2, col=1)
    fig.update_xaxes(title_text="View Count (User)", row=2, col=2, type='log') # Log scale for views
    
    fig.update_yaxes(title_text="Number of Users", row=1, col=1)
    fig.update_yaxes(title_text="Number of Users", row=1, col=2)
    fig.update_yaxes(title_text="Number of Users", row=2, col=1)
    fig.update_yaxes(title_text="Purchase Count (User)", row=2, col=2, type='log') # Log scale for purchases
    
    fig.show()

# %%
# Analyze user behavior patterns
analyze_user_behavior(df_final)

# %%
"""
## 📈 Statistical Testing
This section applies various statistical methods to test hypotheses about customer behavior.
"""

# %%
"""
### 🧪 Hypothesis Testing
"""

# %%
def perform_hypothesis_tests(df_hyp):
    """
    Perform statistical hypothesis tests on the e-commerce data.
    
    Parameters:
    -----------
    df_hyp : pd.DataFrame
        Processed dataframe
    """
    if df_hyp.empty:
        print("Dataframe is empty, skipping hypothesis tests.")
        return

    print("🔍 HYPOTHESIS TESTING RESULTS")
    print("=" * 50)
    
    # 1. Does weekend shopping lead to higher conversion rates for users active on those days?
    # User-level conversion rate, comparing users who shopped on weekends vs. weekdays
    # This requires careful definition. Let's compare conversion of weekend events vs weekday events.
    weekend_events = df_hyp[df_hyp['is_weekend'] == 1]
    weekday_events = df_hyp[df_hyp['is_weekend'] == 0]

    if not weekend_events.empty and not weekday_events.empty:
        # Calculate overall conversion for weekend events vs weekday events
        weekend_views = (weekend_events['event_type'] == 'view').sum()
        weekend_purchases = (weekend_events['event_type'] == 'purchase').sum()
        weekday_views = (weekday_events['event_type'] == 'view').sum()
        weekday_purchases = (weekday_events['event_type'] == 'purchase').sum()

        if weekend_views > 0 and weekday_views > 0:
            weekend_conv_rate = weekend_purchases / weekend_views
            weekday_conv_rate = weekday_purchases / weekday_views

            print("\n1️⃣ WEEKEND vs WEEKDAY EVENT CONVERSION RATE (Proportions Test)")
            print(f"Weekend event conversion rate: {weekend_conv_rate:.4f}")
            print(f"Weekday event conversion rate: {weekday_conv_rate:.4f}")

            # Z-test for two proportions
            count = np.array([weekend_purchases, weekday_purchases])
            nobs = np.array([weekend_views, weekday_views])
            
            # Check for zero counts in a group which can cause issues with ztest
            if weekend_purchases == 0 or weekday_purchases == 0 or \
               weekend_purchases == weekend_views or weekday_purchases == weekday_views :
                print("One group has 0% or 100% conversion, chi2_contingency is more robust.")
                # Fallback to chi-square for proportions if z-test might be problematic
                contingency_weekend = [[weekend_purchases, weekend_views - weekend_purchases],
                                       [weekday_purchases, weekday_views - weekday_purchases]]
                chi2_wk, p_value_wk, _, _ = stats.chi2_contingency(contingency_weekend)
                print(f"Chi-square statistic: {chi2_wk:.4f}")
                print(f"P-value: {p_value_wk:.4f}")
                stat_sig_wk = 'Significant' if p_value_wk < 0.05 else 'Not significant'
            else:
                try:
                    z_stat_wk, p_value_wk = sm.stats.proportions_ztest(count, nobs)
                    print(f"Z-statistic: {z_stat_wk:.4f}")
                    print(f"P-value: {p_value_wk:.4f}")
                    stat_sig_wk = 'Significant' if p_value_wk < 0.05 else 'Not significant'
                except Exception as e:
                    print(f"Could not perform Z-test: {e}. Skipping.")
                    stat_sig_wk = "Error in test"

            print(f"Statistical significance: {stat_sig_wk} at α=0.05")

            # Power analysis for proportions (example)
            # Requires assuming an effect size. Let's use the observed difference.
            # prob_diff = weekend_conv_rate - weekday_conv_rate
            # effect_size_prop = sm.stats.proportion_effectsize(weekend_conv_rate, weekday_conv_rate + prob_diff_for_power)
            # power_analysis = TTestIndPower() # This is for T-test, for Z-test proportions use NormalIndPower
            # power = analysis.power(effect_size=effect_size_prop, nobs1=weekend_views, alpha=0.05, ratio=weekday_views/weekend_views)
            # print(f"Effect size (Cohen's h for proportions): {effect_size_prop:.4f}")
            # print(f"Statistical power (approx): {power:.4f}")
        else:
            print("\n1️⃣ Insufficient data for Weekend vs Weekday conversion rate test.")

    else:
        print("\n1️⃣ Insufficient weekend or weekday data for comparison.")
    
    # 2. Is there a significant price difference between purchased and viewed-only items?
    purchase_prices = df_hyp[df_hyp['event_type'] == 'purchase']['price'].dropna()
    
    # Viewed-only: products that were viewed but *never* purchased by *any* user in the dataset for that product_id
    # This is complex. A simpler definition: price of view events vs price of purchase events.
    view_event_prices = df_hyp[df_hyp['event_type'] == 'view']['price'].dropna()

    if not purchase_prices.empty and not view_event_prices.empty:
        # Mann-Whitney U test (non-parametric, doesn't assume normal distribution)
        # Comparing two independent samples.
        # Using a sample to speed up if datasets are very large
        sample_size_mw = min(len(purchase_prices), len(view_event_prices), 50000)
        u_stat, p_value_price = stats.mannwhitneyu(
            purchase_prices.sample(sample_size_mw, random_state=1) if len(purchase_prices) > sample_size_mw else purchase_prices,
            view_event_prices.sample(sample_size_mw, random_state=1) if len(view_event_prices) > sample_size_mw else view_event_prices,
            alternative='two-sided' # Check for any difference
        )
        
        print("\n2️⃣ PRICES OF PURCHASED ITEMS vs VIEWED ITEMS (Event-level)")
        print(f"Purchased items median price: ${purchase_prices.median():.2f} (Sampled for test if large)")
        print(f"Viewed items median price: ${view_event_prices.median():.2f} (Sampled for test if large)")
        print(f"Mann-Whitney U statistic: {u_stat}")
        print(f"P-value: {p_value_price:.4g}") # Use .4g for scientific notation if p-value is tiny
        print(f"Statistical significance: {'Significant' if p_value_price < 0.05 else 'Not significant'} at α=0.05")
    else:
        print("\n2️⃣ Insufficient price data for purchased or viewed items.")
        
    # 3. Chi-square test: Is there an association between price category and event type?
    if 'price_bucket' in df_hyp.columns and df_hyp['price_bucket'].nunique() > 1:
        contingency_price_event = pd.crosstab(df_hyp['price_bucket'], df_hyp['event_type'], dropna=False)
        
        # Perform chi-square test if table is valid
        if contingency_price_event.shape[0] > 1 and contingency_price_event.shape[1] > 1:
            try:
                chi2_pe, p_value_pe, dof_pe, expected_pe = stats.chi2_contingency(contingency_price_event)
                
                print("\n3️⃣ ASSOCIATION BETWEEN PRICE CATEGORY AND EVENT TYPE")
                print("Contingency table (Price Bucket vs Event Type):")
                display(contingency_price_event)
                print(f"\nChi-square statistic: {chi2_pe:.4f}")
                print(f"Degrees of freedom: {dof_pe}")
                print(f"P-value: {p_value_pe:.4g}")
                print(f"Statistical significance: {'Significant' if p_value_pe < 0.05 else 'Not significant'} at α=0.05")
                
                # Create visualization for the chi-square results
                plt.figure(figsize=(14, 7))
                
                plt.subplot(1, 2, 1)
                sns.heatmap(contingency_price_event, annot=True, fmt="d", cmap="viridis")
                plt.title("Observed Frequencies")
                plt.xlabel("Event Type")
                plt.ylabel("Price Category")
                
                plt.subplot(1, 2, 2)
                sns.heatmap(pd.DataFrame(expected_pe, index=contingency_price_event.index, columns=contingency_price_event.columns), 
                            annot=True, fmt=".1f", cmap="viridis")
                plt.title("Expected Frequencies (if independent)")
                plt.xlabel("Event Type")
                plt.ylabel("Price Category")
                
                plt.tight_layout()
                plt.show()
            except ValueError as e:
                print(f"\n3️⃣ Chi-square test failed for Price Category vs Event Type: {e}")
        else:
            print("\n3️⃣ Contingency table for Price Category vs Event Type not valid for Chi-square test (too few rows/cols).")
    else:
        print("\n3️⃣ Skipping Price Category vs Event Type test: 'price_bucket' not available or insufficient categories.")

# %%
# Perform hypothesis tests
perform_hypothesis_tests(df_final)

# %%
"""
### 🧬 Generalized Linear Models (GLM)
"""

# %%
def build_glm_models(df_glm):
    """
    Build and evaluate GLM models for predicting purchasing behavior.
    
    Parameters:
    -----------
    df_glm : pd.DataFrame
        Processed dataframe
    """
    if df_glm.empty:
        print("Dataframe is empty, skipping GLM models.")
        return

    print("🔬 GENERALIZED LINEAR MODELS ANALYSIS")
    print("=" * 50)
    
    # Prepare user-level data for GLMs
    # We need features per user.
    user_event_counts_glm = df_glm.groupby(['user_id', 'event_type']).size().unstack(fill_value=0)
    user_event_counts_glm.columns = [f"{col}_count" for col in user_event_counts_glm.columns]
    
    required_cols = ['view_count', 'cart_count', 'purchase_count']
    for col in required_cols:
        if col not in user_event_counts_glm:
            user_event_counts_glm[col] = 0

    user_data_glm = df_glm.groupby('user_id').agg(
        avg_price_interacted=('price', 'mean'), # Avg price of items user interacted with
        is_weekend_shopper_majority=('is_weekend', lambda x: x.mean() > 0.5), # If >50% events on weekend
        lifetime_days_glm=('lifetime_days', 'first'), # Use the pre-calculated lifetime
        # Add more relevant features, e.g., number of unique categories viewed
        unique_categories_viewed = ('category_code', lambda x: x[df_glm.loc[x.index, 'event_type'] == 'view'].nunique())
    )
    user_data_glm = user_data_glm.join(user_event_counts_glm, how='left').reset_index()
    
    # Fill NaNs (e.g., avg_price if user had no price events, lifetime if new user)
    user_data_glm.fillna({
        'avg_price_interacted': df_glm['price'].mean(), # Impute with global mean price
        'lifetime_days_glm': 0,
        'unique_categories_viewed': 0
    }, inplace=True)
    user_data_glm['is_weekend_shopper_majority'] = user_data_glm['is_weekend_shopper_majority'].astype(int)
    
    # Cap extreme values for stability if necessary (e.g., view_count)
    user_data_glm['view_count_capped'] = user_data_glm['view_count'].clip(upper=user_data_glm['view_count'].quantile(0.99))
    user_data_glm['cart_count_capped'] = user_data_glm['cart_count'].clip(upper=user_data_glm['cart_count'].quantile(0.99))


    # 1. Poisson GLM for purchase count
    print("\n1️⃣ POISSON REGRESSION: PREDICTING USER PURCHASE COUNT")
    
    # Formula: ensure no multicollinearity. Start simple.
    # 'lifetime_days_glm' could be an offset if positive, or a feature.
    # For simplicity, treat as feature. Add 1 to avoid log(0) if used as offset.
    poisson_formula = "purchase_count ~ view_count_capped + cart_count_capped + avg_price_interacted + is_weekend_shopper_majority + unique_categories_viewed"
    
    try:
        poisson_model = smf.glm(
            formula=poisson_formula,
            data=user_data_glm,
            family=sm.families.Poisson()
        ).fit(disp=0) # disp=0 for Poisson, or estimate dispersion for NegativeBinomial
        
        print(poisson_model.summary().tables[1])
        
        # Calculate and display additional metrics
        user_data_glm['predicted_purchases_poisson'] = poisson_model.predict(user_data_glm)
        mse_poisson = np.mean((user_data_glm['purchase_count'] - user_data_glm['predicted_purchases_poisson'])**2)
        rmse_poisson = np.sqrt(mse_poisson)
        
        print(f"\nMean Squared Error (Poisson): {mse_poisson:.4f}")
        print(f"Root Mean Squared Error (Poisson): {rmse_poisson:.4f}")
        
        # Visualize actual vs predicted
        plt.figure(figsize=(10, 6))
        plt.scatter(user_data_glm['purchase_count'], user_data_glm['predicted_purchases_poisson'], 
                    alpha=0.3, color='blue', s=10)
        plt.plot([0, user_data_glm['purchase_count'].max()], 
                 [0, user_data_glm['purchase_count'].max()], 
                 'r--')
        plt.xlabel('Actual Purchase Count (User)')
        plt.ylabel('Predicted Purchase Count (Poisson)')
        plt.title('Poisson GLM: Actual vs Predicted Purchase Counts')
        plt.xscale('log') # Often helpful for count data
        plt.yscale('log')
        plt.xlim(left=0.1) # Avoid log(0) issues
        plt.ylim(bottom=0.1)
        plt.grid(True, alpha=0.3)
        plt.show()
    except Exception as e:
        print(f"Error building Poisson GLM: {e}")

    # 2. Logistic Regression for predicting if user will make a purchase
    print("\n2️⃣ LOGISTIC REGRESSION: PREDICTING PURCHASE LIKELIHOOD (ANY PURCHASE)")
    
    # Create binary target: did the user make any purchase?
    user_data_glm['made_purchase_binary'] = (user_data_glm['purchase_count'] > 0).astype(int)
    
    # Formula for logistic regression
    logit_formula = "made_purchase_binary ~ view_count_capped + cart_count_capped + avg_price_interacted + is_weekend_shopper_majority + unique_categories_viewed"

    if user_data_glm['made_purchase_binary'].nunique() < 2:
        print("Skipping Logistic Regression: Target variable 'made_purchase_binary' has only one unique value.")
    else:
        try:
            logit_model = smf.glm(
                formula=logit_formula,
                data=user_data_glm,
                family=sm.families.Binomial()
            ).fit()
            
            print(logit_model.summary().tables[1])
            
            # Calculate and display additional metrics
            user_data_glm['purchase_probability_logit'] = logit_model.predict(user_data_glm)
            user_data_glm['predicted_purchase_logit'] = (user_data_glm['purchase_probability_logit'] > 0.5).astype(int)
            
            # Calculate accuracy
            accuracy_logit = (user_data_glm['predicted_purchase_logit'] == user_data_glm['made_purchase_binary']).mean()
            print(f"\nAccuracy (Logistic): {accuracy_logit:.4f}")
            
            # Display confusion matrix
            conf_matrix_logit = pd.crosstab(
                user_data_glm['made_purchase_binary'], 
                user_data_glm['predicted_purchase_logit'],
                rownames=['Actual Purchase'], 
                colnames=['Predicted Purchase']
            )
            
            print("\nConfusion Matrix (Logistic):")
            print(conf_matrix_logit)
            
            # Visualize regression results (partial dependence style plots)
            plt.figure(figsize=(14, 6))
            
            plt.subplot(1, 2, 1)
            # For plotting effect of one variable, hold others at mean/median or use model predictions
            # Simpler: plot probability vs. feature directly (marginal plot)
            sns.regplot(x='view_count_capped', y='purchase_probability_logit', data=user_data_glm, 
                        logistic=True, scatter_kws={'alpha': 0.1, 's':5}, line_kws={'color': 'red'})
            plt.title('Effect of View Count on Purchase Probability')
            plt.xlabel('View Count (Capped)')
            plt.ylabel('Predicted Probability of Purchase')
            
            plt.subplot(1, 2, 2)
            sns.regplot(x='avg_price_interacted', y='purchase_probability_logit', data=user_data_glm,
                        logistic=True, scatter_kws={'alpha': 0.1, 's':5}, line_kws={'color': 'red'})
            plt.title('Effect of Avg. Interaction Price on Purchase Probability')
            plt.xlabel('Average Price Interacted With')
            plt.ylabel('Predicted Probability of Purchase')
            
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error building Logistic GLM: {e}")

# %%
# Build GLM models
build_glm_models(df_final)

# %%
"""
### ⌛ Survival Analysis
"""

# %%
def perform_survival_analysis(df_surv):
    """
    Apply survival analysis to understand customer churn and lifetime.
    
    Parameters:
    -----------
    df_surv : pd.DataFrame
        Processed dataframe
    """
    if df_surv.empty:
        print("Dataframe is empty, skipping survival analysis.")
        return pd.DataFrame() # Return empty DF if needed by caller

    print("⏱️ SURVIVAL ANALYSIS: CUSTOMER RETENTION")
    print("=" * 50)
    
    # Prepare data for survival analysis
    # Define "churn": no activity for a certain period before the dataset's max_date
    
    # Get first and last event date for each user
    user_activity_times = df_surv.groupby('user_id')['event_time'].agg(['min', 'max']).reset_index()
    user_activity_times.columns = ['user_id', 'first_event_time', 'last_event_time']
    
    # Overall dataset observation period
    dataset_start_date = df_surv['event_time'].min()
    dataset_end_date = df_surv['event_time'].max()
    
    # Duration of user activity within the dataset
    user_activity_times['duration_active_days'] = (user_activity_times['last_event_time'] - 
                                                   user_activity_times['first_event_time']).dt.total_seconds() / (60*60*24)
    
    # Time since first event until end of dataset (potential max observation time for the user)
    user_activity_times['time_since_first_event_to_dataset_end_days'] = \
        (dataset_end_date - user_activity_times['first_event_time']).dt.total_seconds() / (60*60*24)

    # Define churn: no activity in the last X days of the observation period
    # This definition implies we are looking at churn AT THE END of the dataset period.
    churn_threshold_days = 7 
    user_activity_times['is_churned_at_dataset_end'] = \
        ((dataset_end_date - user_activity_times['last_event_time']).dt.total_seconds() / (60*60*24)) > churn_threshold_days
    user_activity_times['is_churned_at_dataset_end'] = user_activity_times['is_churned_at_dataset_end'].astype(int)
    
    # For survival analysis, 'duration' is time to event (churn) or censoring.
    # If churned: duration is time from first_event to last_event + (churn_threshold_days / 2) (approx time of churn)
    # If not churned (censored): duration is time from first_event to dataset_end_date
    
    # Simplified approach: Time from first_event to last_event for churned users (they completed their "active life")
    # Time from first_event to dataset_end_date for non-churned users (they were still active at censoring point)
    
    # Let T = time from first event to last event (user's observed active period)
    # Let C = time from first event to dataset_end_date (censoring time for this user cohort)
    # Observed time for KMF: min(T, C_i) where C_i is specific to user if they started late.
    # Here, we are observing users from their first event in the dataset.
    # Duration = time_since_first_event_to_dataset_end_days
    # Event_observed = is_churned_at_dataset_end (1 if churned, 0 if censored/active)
    # However, lifelines expects duration to be the time until event OR censoring.
    # For churned users, it's duration_active_days (time until their "death" - last activity).
    # For non-churned, it's time_since_first_event_to_dataset_end_days (they "survived" until dataset end).

    user_activity_times['observed_duration_kmf'] = np.where(
        user_activity_times['is_churned_at_dataset_end'] == 1,
        user_activity_times['duration_active_days'], # Time until "death" (last activity)
        user_activity_times['time_since_first_event_to_dataset_end_days'] # Time until censoring (dataset end)
    )
    # Ensure observed_duration_kmf is not zero or negative, which can happen for users with one event on the last day. Add a small epsilon.
    user_activity_times['observed_duration_kmf'] = user_activity_times['observed_duration_kmf'].clip(lower=0.001)

    # Filter out users with 0 duration if they only have one event (ambiguous for churn definition)
    # user_activity_times = user_activity_times[user_activity_times['observed_duration_kmf'] > 0]

    if user_activity_times.empty:
        print("No user data left for survival analysis after processing. Check churn definitions.")
        return pd.DataFrame()

    # 1. Kaplan-Meier Survival Curve
    print("\n1️⃣ KAPLAN-MEIER SURVIVAL CURVE ANALYSIS (CUSTOMER RETENTION)")
    
    kmf = KaplanMeierFitter()
    kmf.fit(user_activity_times['observed_duration_kmf'], 
            event_observed=user_activity_times['is_churned_at_dataset_end'],
            label="All Users (Retention from first event)")
    
    # Calculate metrics from the KM curve
    try:
        median_lifetime_kmf = kmf.median_survival_time_
        print(f"Median customer active lifetime (KMF): {median_lifetime_kmf:.2f} days (conditional on being active)")
    except Exception as e:
        print(f"Could not calculate median survival time: {e}")
        median_lifetime_kmf = np.nan

    # Plot KM curve
    plt.figure(figsize=(10, 6))
    kmf.plot_survival_function()
    plt.title('Customer Retention: Kaplan-Meier Survival Curve')
    plt.xlabel('Time (Days since first event in dataset)')
    plt.ylabel('Survival Probability (Retention Rate)')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # 2. Cox Proportional Hazards Model
    # We need covariates (user-level features) that might affect churn.
    user_metrics_for_cox = df_surv.groupby('user_id').agg(
        purchase_count_cox=('event_type', lambda x: sum(x == 'purchase')),
        avg_purchase_value_cox=('price', lambda x: x[df_surv.loc[x.index, 'event_type'] == 'purchase'].mean()),
        is_weekend_shopper_cox=('is_weekend', lambda x: (x.mean() > 0.5).astype(int)),
        total_events_cox=('event_type', 'count') 
    ).reset_index()
    
    # Merge with user timeline data
    survival_df_cox = user_activity_times.merge(user_metrics_for_cox, on='user_id', how='left')
    
    # Handle missing values in covariates (e.g., avg_purchase_value for non-purchasers)
    survival_df_cox['avg_purchase_value_cox'] = survival_df_cox['avg_purchase_value_cox'].fillna(0) # Or median of purchasers
    survival_df_cox = survival_df_cox.dropna(subset=['observed_duration_kmf', 'is_churned_at_dataset_end', 
                                                     'purchase_count_cox', 'avg_purchase_value_cox', 
                                                     'is_weekend_shopper_cox', 'total_events_cox'])
    
    # Ensure there's variance in features for Cox model
    features_for_cox = ['purchase_count_cox', 'avg_purchase_value_cox', 'is_weekend_shopper_cox', 'total_events_cox']
    features_to_use_cox = []
    for f in features_for_cox:
        if survival_df_cox[f].nunique() > 1:
            features_to_use_cox.append(f)
        else:
            print(f"Feature '{f}' has no variance, excluding from Cox model.")

    if not features_to_use_cox or survival_df_cox.shape[0] < 20 : # Need enough data and features
        print("\n2️⃣ Insufficient data or feature variance for Cox Proportional Hazards Model.")
        return user_activity_times # Return KMF data

    print("\n2️⃣ COX PROPORTIONAL HAZARDS MODEL (CUSTOMER CHURN)")
    
    # Select columns for CPH model
    cox_model_data = survival_df_cox[['observed_duration_kmf', 'is_churned_at_dataset_end'] + features_to_use_cox]
    # Rename for lifelines convention
    cox_model_data = cox_model_data.rename(columns={'observed_duration_kmf': 'duration', 
                                                    'is_churned_at_dataset_end': 'event'})

    try:
        cph = CoxPHFitter(penalizer=0.1) # Added small penalizer for stability
        cph.fit(cox_model_data, duration_col='duration', event_col='event')
        
        print(cph.summary)
        
        # Visualize hazard ratios
        plt.figure(figsize=(10, max(4, len(features_to_use_cox) * 0.8))) # Adjust height based on num features
        cph.plot()
        plt.title('Cox Proportional Hazards: Feature Impact on Churn Risk (Hazard Ratios)')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error fitting Cox model: {e}")
        
    return survival_df_cox # Return data used for Cox model (includes KMF data too)

# %%
# Perform survival analysis
survival_data = perform_survival_analysis(df_final)

# %%
"""
## 🧮 Advanced Statistical Analysis
This section applies sophisticated statistical techniques for deeper business insights.
"""

# %%
"""
### ⏰ Time Series Decomposition
"""

# %%
def analyze_time_series(df_ts):
    """
    Perform time series decomposition and analysis on e-commerce purchase data.
    
    Parameters:
    -----------
    df_ts : pd.DataFrame
        Processed dataframe
    """
    if df_ts.empty or 'date' not in df_ts.columns:
        print("Dataframe is empty or 'date' column missing, skipping time series analysis.")
        return

    print("📅 TIME SERIES DECOMPOSITION ANALYSIS")
    print("=" * 50)
    
    # Prepare daily time series data
    # Ensure 'date' is datetime.date, convert to pd.Timestamp for setting index
    df_ts['date_dt_ts'] = pd.to_datetime(df_ts['date'])
    
    daily_aggregates = df_ts.groupby('date_dt_ts').agg(
        purchase_count_ts=('event_type', lambda x: sum(x == 'purchase')),
        total_revenue_ts=('price', lambda x: sum(x[df_ts.loc[x.index, 'event_type'] == 'purchase']))
    ).reset_index()
    
    daily_aggregates = daily_aggregates.set_index('date_dt_ts')
    
    # Ensure the time series is continuous (fill missing dates with zeros)
    # This is important for seasonal_decompose
    if not daily_aggregates.empty:
        date_range = pd.date_range(start=daily_aggregates.index.min(), end=daily_aggregates.index.max(), freq='D')
        daily_aggregates = daily_aggregates.reindex(date_range, fill_value=0)
    else:
        print("No data for daily aggregates. Skipping time series decomposition.")
        return

    # Check if series has enough data points for decomposition (e.g., > 2*period)
    period = 7 # Weekly seasonality
    if len(daily_aggregates) < 2 * period:
        print(f"Time series too short for decomposition with period {period}. Needs at least {2*period} data points.")
        # Plot raw series if too short
        plt.figure(figsize=(14, 5))
        plt.subplot(1,2,1); daily_aggregates['purchase_count_ts'].plot(title='Daily Purchase Count (Short Series)')
        plt.subplot(1,2,2); daily_aggregates['total_revenue_ts'].plot(title='Daily Revenue (Short Series)')
        plt.tight_layout(); plt.show()
        return
        
    print("\n1️⃣ PURCHASE COUNT TIME SERIES DECOMPOSITION (Weekly Seasonality)")
    try:
        decomposition_purchases = seasonal_decompose(daily_aggregates['purchase_count_ts'], model='additive', period=period)
        
        # Plot the decomposition
        fig_decomp_p, axes_p = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
        decomposition_purchases.observed.plot(ax=axes_p[0], legend=False, title='Observed Purchases')
        axes_p[0].set_ylabel('Count')
        decomposition_purchases.trend.plot(ax=axes_p[1], legend=False, title='Trend')
        axes_p[1].set_ylabel('Count')
        decomposition_purchases.seasonal.plot(ax=axes_p[2], legend=False, title=f'Seasonal (Period={period} days)')
        axes_p[2].set_ylabel('Count')
        decomposition_purchases.resid.plot(ax=axes_p[3], legend=False, title='Residual')
        axes_p[3].set_ylabel('Count')
        plt.xlabel('Date')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not decompose purchase count series: {e}")

    print("\n2️⃣ REVENUE TIME SERIES DECOMPOSITION (Weekly Seasonality)")
    try:
        decomposition_revenue = seasonal_decompose(daily_aggregates['total_revenue_ts'], model='additive', period=period)
        
        # Plot the decomposition
        fig_decomp_r, axes_r = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
        decomposition_revenue.observed.plot(ax=axes_r[0], legend=False, title='Observed Revenue')
        axes_r[0].set_ylabel('Revenue')
        decomposition_revenue.trend.plot(ax=axes_r[1], legend=False, title='Trend')
        axes_r[1].set_ylabel('Revenue')
        decomposition_revenue.seasonal.plot(ax=axes_r[2], legend=False, title=f'Seasonal (Period={period} days)')
        axes_r[2].set_ylabel('Revenue')
        decomposition_revenue.resid.plot(ax=axes_r[3], legend=False, title='Residual')
        axes_r[3].set_ylabel('Revenue')
        plt.xlabel('Date')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not decompose revenue series: {e}")

    # Interactive time series visualization with Plotly
    fig_plotly_ts = make_subplots(rows=2, cols=1, 
                       subplot_titles=('Daily Purchase Count', 'Daily Revenue'),
                       shared_xaxes=True, vertical_spacing=0.1)
    
    fig_plotly_ts.add_trace(
        go.Scatter(x=daily_aggregates.index, y=daily_aggregates['purchase_count_ts'],
                  mode='lines', name='Purchase Count', line=dict(color='#636EFA')),
        row=1, col=1
    )
    
    fig_plotly_ts.add_trace(
        go.Scatter(x=daily_aggregates.index, y=daily_aggregates['total_revenue_ts'],
                  mode='lines', name='Revenue', line=dict(color='#EF553B')),
        row=2, col=1
    )
    
    # Add trend lines if decomposition was successful
    if 'decomposition_purchases' in locals() and hasattr(decomposition_purchases, 'trend'):
        fig_plotly_ts.add_trace(
            go.Scatter(x=decomposition_purchases.trend.index, y=decomposition_purchases.trend,
                      mode='lines', name='Purchase Trend', line=dict(color='#00CC96', dash='dash')),
            row=1, col=1
        )
    if 'decomposition_revenue' in locals() and hasattr(decomposition_revenue, 'trend'):
        fig_plotly_ts.add_trace(
            go.Scatter(x=decomposition_revenue.trend.index, y=decomposition_revenue.trend,
                      mode='lines', name='Revenue Trend', line=dict(color='#AB63FA', dash='dash')),
            row=2, col=1
        )
    
    fig_plotly_ts.update_layout(
        height=700,
        width=1000,
        title_text="Daily E-Commerce Metrics Over Time (Interactive)",
        showlegend=True,
        hovermode='x unified'
    )
    fig_plotly_ts.update_xaxes(title_text="Date", row=2, col=1)
    fig_plotly_ts.update_yaxes(title_text="Purchase Count", row=1, col=1)
    fig_plotly_ts.update_yaxes(title_text="Total Revenue", row=2, col=1)
    fig_plotly_ts.show()
    
    # Daily patterns analysis (day of week effect)
    # Use original 'day_of_week' (Mon=0, Sun=6)
    daily_patterns_agg = df_ts.groupby('day_of_week').agg(
        view_count_dow=('event_type', lambda x: sum(x == 'view')),
        purchase_count_dow=('event_type', lambda x: sum(x == 'purchase')),
        revenue_dow=('price', lambda x: sum(x[df_ts.loc[x.index, 'event_type'] == 'purchase']))
    ).reset_index()
    
    day_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    daily_patterns_agg['day_name'] = daily_patterns_agg['day_of_week'].map(day_map)
    
    daily_patterns_agg['conversion_rate_dow'] = np.where(
        daily_patterns_agg['view_count_dow'] > 0,
        (daily_patterns_agg['purchase_count_dow'] / daily_patterns_agg['view_count_dow'] * 100),
        0
    ).round(2)
    
    # Visualize day of week patterns
    fig_dow = make_subplots(rows=1, cols=3, 
                       subplot_titles=('Avg. Daily Purchase Count', 'Avg. Daily Revenue', 'Avg. Daily Conversion Rate'),
                       specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}]])
    
    num_weeks_in_data = (df_ts['date_dt_ts'].max() - df_ts['date_dt_ts'].min()).days / 7.0
    num_weeks_in_data = max(1, num_weeks_in_data) # Avoid division by zero if less than a week

    fig_dow.add_trace(
        go.Bar(x=daily_patterns_agg['day_name'], y=daily_patterns_agg['purchase_count_dow']/num_weeks_in_data,
              marker_color='#636EFA', name='Avg Purchases'),
        row=1, col=1
    )
    fig_dow.add_trace(
        go.Bar(x=daily_patterns_agg['day_name'], y=daily_patterns_agg['revenue_dow']/num_weeks_in_data,
              marker_color='#EF553B', name='Avg Revenue'),
        row=1, col=2
    )
    fig_dow.add_trace(
        go.Bar(x=daily_patterns_agg['day_name'], y=daily_patterns_agg['conversion_rate_dow'], # CR is already a rate
              marker_color='#00CC96', name='Avg Conv. Rate'),
        row=1, col=3
    )
    
    fig_dow.update_layout(
        height=450,
        width=1000,
        title_text="Average Daily Patterns by Day of Week",
        showlegend=False,
        xaxis_categoryorder='array', # Ensure days are in order
        xaxis_categoryarray=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    )
    fig_dow.update_xaxes(title_text="Day of Week", row=1, col=1); fig_dow.update_xaxes(title_text="Day of Week", row=1, col=2); fig_dow.update_xaxes(title_text="Day of Week", row=1, col=3)
    fig_dow.update_yaxes(title_text="Avg. Purchases", row=1, col=1)
    fig_dow.update_yaxes(title_text="Avg. Revenue", row=1, col=2)
    fig_dow.update_yaxes(title_text="Avg. Conversion Rate (%)", row=1, col=3)
    fig_dow.show()

# %%
# Analyze time series patterns
analyze_time_series(df_final)

# %%
"""
### 🧩 Principal Component Analysis (PCA) for User Behavior
"""

# %%
def perform_pca_analysis(df_pca_source):
    """
    Use PCA to identify key patterns in customer behavior data (user-level).
    
    Parameters:
    -----------
    df_pca_source : pd.DataFrame
        Processed dataframe (event-level)
    """
    if df_pca_source.empty:
        print("Dataframe is empty, skipping PCA analysis.")
        return pd.DataFrame()

    print("🔬 PRINCIPAL COMPONENT ANALYSIS (USER BEHAVIOR)")
    print("=" * 50)
    
    # Create user-level dataset with behavioral features for PCA
    user_features_pca = df_pca_source.groupby('user_id').agg(
        view_count_pca=('event_type', lambda x: sum(x == 'view')),
        cart_count_pca=('event_type', lambda x: sum(x == 'cart')),
        purchase_count_pca=('event_type', lambda x: sum(x == 'purchase')),
        avg_price_event_pca=('price', 'mean'), # Avg price of items user interacted with
        max_price_event_pca=('price', 'max'),   # Max price of item user interacted with
        total_spent_pca=('total_spent', 'first'), # From pre-calculated df_final.total_spent
        weekend_event_ratio_pca=('is_weekend', 'mean'), # Proportion of events on weekend
        conversion_rate_pca=('conversion_rate', 'first'), # From pre-calculated df_final.conversion_rate
        total_events_pca=('event_type', 'count'), # Overall browsing/interaction intensity
        unique_products_viewed_pca=('product_id', lambda x: x[df_pca_source.loc[x.index, 'event_type'] == 'view'].nunique()),
        unique_categories_viewed_pca=('category_code', lambda x: x[df_pca_source.loc[x.index, 'event_type'] == 'view'].nunique()),
        avg_time_btw_events_pca=('time_since_last_event_minutes', lambda x: x[x > 0].mean()) # Avg for non-first events
    ).reset_index()
    
    # Handle NaNs from aggregations (e.g., avg_price if no price events, avg_time if 1 event)
    user_features_pca = user_features_pca.fillna(user_features_pca.median(numeric_only=True)) # Impute with median
    # For any remaining NaNs (e.g. if median is NaN due to all NaNs in a column), fill with 0
    user_features_pca = user_features_pca.fillna(0)

    features_for_pca = user_features_pca.drop('user_id', axis=1)
    
    # Ensure all features are numeric and no NaNs/Infs
    features_for_pca = features_for_pca.apply(pd.to_numeric, errors='coerce').fillna(0)
    features_for_pca.replace([np.inf, -np.inf], 0, inplace=True) # Replace infs if any

    if features_for_pca.empty or features_for_pca.shape[1] == 0:
        print("No valid features for PCA. Skipping.")
        return pd.DataFrame()
        
    # Scale the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_for_pca)
    
    # Perform PCA
    pca = PCA()
    pca_transformed_data = pca.fit_transform(scaled_features)
    
    # Explained variance
    explained_variance_ratio = pca.explained_variance_ratio_
    cumulative_explained_variance = np.cumsum(explained_variance_ratio)
    
    print("\nVariance Explained by Principal Components:")
    for i, var_ratio in enumerate(explained_variance_ratio[:min(10, len(explained_variance_ratio))]): # Show top 10 or all
        print(f"PC{i+1}: {var_ratio:.4f} (Cumulative: {cumulative_explained_variance[i]:.4f})")
    
    # Plot explained variance
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    num_components_to_plot = min(20, len(explained_variance_ratio))
    plt.bar(range(1, num_components_to_plot + 1), explained_variance_ratio[:num_components_to_plot], alpha=0.7, label='Individual explained variance')
    plt.step(range(1, num_components_to_plot + 1), cumulative_explained_variance[:num_components_to_plot], where='mid', label='Cumulative explained variance', color='red')
    plt.axhline(y=0.95, linestyle='--', color='green', label='95% Variance Threshold')
    plt.title('Scree Plot: Explained Variance by Components')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Explained Variance Ratio')
    plt.xticks(range(1, num_components_to_plot + 1))
    plt.legend(loc='best')
    
    plt.subplot(1, 2, 2)
    plt.plot(range(1, num_components_to_plot + 1), cumulative_explained_variance[:num_components_to_plot], marker='o', linestyle='-')
    plt.axhline(y=0.95, linestyle='--', color='green', label='95% Variance Threshold')
    plt.title('Cumulative Explained Variance')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance Ratio')
    plt.xticks(range(1, num_components_to_plot + 1))
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Optimal number of components (e.g., for 95% variance)
    n_components_95 = np.where(cumulative_explained_variance >= 0.95)[0][0] + 1 if (cumulative_explained_variance >= 0.95).any() else len(explained_variance_ratio)
    print(f"\nOptimal number of components to explain 95% variance: {n_components_95}")
    
    # Component loadings (correlation of original features with PCs)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_) # Scaled loadings
    feature_names = features_for_pca.columns
    loadings_df = pd.DataFrame(loadings, index=feature_names, columns=[f'PC{i+1}' for i in range(loadings.shape[1])])
    
    print("\nFeature Loadings for Top 2 Principal Components (Top 5 features per PC):")
    if 'PC1' in loadings_df.columns:
      print("\nPC1 Influential Features (Absolute Loadings):")
      print(loadings_df['PC1'].abs().sort_values(ascending=False).head())
    if 'PC2' in loadings_df.columns:
      print("\nPC2 Influential Features (Absolute Loadings):")
      print(loadings_df['PC2'].abs().sort_values(ascending=False).head())
    
    # Create a DataFrame with the first two principal components and original features for plotting
    pca_plot_df = pd.DataFrame(data=pca_transformed_data[:, :min(2, pca_transformed_data.shape[1])], 
                               columns=[f'PC{i+1}' for i in range(min(2, pca_transformed_data.shape[1]))])
    pca_plot_df['user_id'] = user_features_pca['user_id']
    # Merge some key original features for coloring/sizing plot
    pca_plot_df = pca_plot_df.merge(user_features_pca[['user_id', 'purchase_count_pca', 'total_spent_pca', 'conversion_rate_pca']], on='user_id')
    
    if 'PC1' in pca_plot_df.columns and 'PC2' in pca_plot_df.columns:
        # Create interactive PCA visualization (sample if too many points)
        sample_pca_plot_df = pca_plot_df.sample(min(len(pca_plot_df), 10000), random_state=42) # Sample for performance
        fig_pca_plotly = px.scatter(
            sample_pca_plot_df, x='PC1', y='PC2',
            color='conversion_rate_pca', 
            size='total_spent_pca',  # Ensure total_spent_pca has reasonable positive values for size
            size_max=15,
            hover_data=['user_id', 'purchase_count_pca'],
            opacity=0.6,
            color_continuous_scale=px.colors.sequential.Viridis,
            title='PCA of User Behavior (PC1 vs PC2)'
        )
        
        # Add feature loading vectors (biplot style)
        # Scale loadings for visibility on the scatter plot
        scale_factor = np.abs(pca_transformed_data[:, :2]).max() / np.abs(loadings_df[['PC1', 'PC2']]).max().max() * 0.5 # Heuristic scaling
        
        for i, feature in enumerate(feature_names):
            fig_pca_plotly.add_shape(
                type='line',
                x0=0, y0=0,
                x1=loadings_df.loc[feature, 'PC1'] * scale_factor, 
                y1=loadings_df.loc[feature, 'PC2'] * scale_factor,
                line=dict(color='red', width=1)
            )
            fig_pca_plotly.add_annotation(
                x=loadings_df.loc[feature, 'PC1'] * scale_factor * 1.15,
                y=loadings_df.loc[feature, 'PC2'] * scale_factor * 1.15,
                text=feature, showarrow=False, font=dict(color='red', size=9)
            )
        
        fig_pca_plotly.update_layout(
            height=700, width=900,
            xaxis_title=f"PC1 ({explained_variance_ratio[0]:.2%} variance)",
            yaxis_title=f"PC2 ({explained_variance_ratio[1]:.2%} variance)",
            coloraxis_colorbar=dict(title="Conv. Rate")
        )
        fig_pca_plotly.show()
    else:
        print("Not enough components for a 2D PCA plot.")

    return pca_plot_df # Return dataframe with PC scores and user_id

# %%
# Perform PCA
pca_user_behavior_df = perform_pca_analysis(df_final)

# %%
"""
### 🔀 Bayesian A/B Testing
"""

# %%
def bayesian_ab_test(df_ab):
    """
    Perform Bayesian A/B testing.
    For demonstration, creates a synthetic A/B test scenario.
    
    Parameters:
    -----------
    df_ab : pd.DataFrame
        Processed dataframe
    """
    if df_ab.empty:
        print("Dataframe is empty, skipping Bayesian A/B test.")
        return

    print("🧪 BAYESIAN A/B TESTING ANALYSIS (SYNTHETIC SCENARIO)")
    print("=" * 50)
    
    # Create a synthetic A/B test scenario:
    # Divide users randomly into two groups (A and B)
    # Analyze conversion rates (e.g., view-to-purchase)
    
    all_user_ids = df_ab['user_id'].unique()
    np.random.seed(42) # For reproducibility
    group_assignment = np.random.choice(['A', 'B'], size=len(all_user_ids), p=[0.5, 0.5])
    user_to_group_map = pd.Series(group_assignment, index=all_user_ids)
    
    df_ab['ab_variant'] = df_ab['user_id'].map(user_to_group_map)
    
    # Calculate conversion metrics for each variant (user-level conversion)
    # Views: number of users who viewed. Purchases: number of users who purchased.
    # Alternative: total views vs total purchases (event-level conversion) - let's use event level for simplicity here.
    
    variant_event_metrics = df_ab.groupby('ab_variant')['event_type'].value_counts().unstack(fill_value=0)
    
    if 'view' not in variant_event_metrics.columns or 'purchase' not in variant_event_metrics.columns:
        print("Synthetic A/B test data lacks 'view' or 'purchase' events. Skipping.")
        return
        
    a_views = variant_event_metrics.loc['A', 'view']
    a_purchases = variant_event_metrics.loc['A', 'purchase']
    b_views = variant_event_metrics.loc['B', 'view']
    b_purchases = variant_event_metrics.loc['B', 'purchase']

    if a_views == 0 or b_views == 0:
        print("One of the synthetic variants has zero views. Skipping A/B test.")
        return

    print("\nSynthetic A/B Test Event Metrics:")
    print(f"Variant A: Views={a_views}, Purchases={a_purchases}, CR={(a_purchases/a_views)*100 if a_views else 0:.2f}%")
    print(f"Variant B: Views={b_views}, Purchases={b_purchases}, CR={(b_purchases/b_views)*100 if b_views else 0:.2f}%")
    
    # Perform chi-square test (Frequentist comparison)
    contingency_ab = np.array([[a_purchases, a_views - a_purchases], 
                               [b_purchases, b_views - b_purchases]])
    
    chi2_ab, p_value_ab, _, _ = stats.chi2_contingency(contingency_ab)
    
    print("\n1️⃣ FREQUENTIST A/B TEST RESULTS (Chi-Square on Event Counts)")
    print(f"Chi-square statistic: {chi2_ab:.4f}")
    print(f"P-value: {p_value_ab:.4f}")
    print(f"Statistical significance: {'Significant' if p_value_ab < 0.05 else 'Not significant'} at α=0.05")
    
    # Bayesian A/B testing using PyMC
    print("\n2️⃣ BAYESIAN A/B TEST ANALYSIS (PYMC)")
    
    with pm.Model() as ab_model:
        # Priors for conversion rates (Beta distribution is conjugate prior for Binomial likelihood)
        # Uniform prior (Beta(1,1)) implies no prior knowledge.
        theta_a = pm.Beta('theta_a', alpha=1.0, beta=1.0)  # Conversion rate for A
        theta_b = pm.Beta('theta_b', alpha=1.0, beta=1.0)  # Conversion rate for B
        
        # Likelihood of observing the data (Binomial distribution for purchases given views)
        # Ensure observed counts are integers
        likelihood_a = pm.Binomial('likelihood_a', n=int(a_views), p=theta_a, observed=int(a_purchases))
        likelihood_b = pm.Binomial('likelihood_b', n=int(b_views), p=theta_b, observed=int(b_purchases))
        
        # Derived quantities (difference between conversion rates)
        delta_abs = pm.Deterministic('delta_abs', theta_b - theta_a) # Absolute difference
        # Relative improvement (handle potential division by zero if theta_a can be zero)
        # Add small epsilon to theta_a in denominator if using non-informative priors that allow zero.
        # Beta(1,1) allows values near zero.
        delta_rel = pm.Deterministic('delta_rel', (theta_b - theta_a) / (theta_a + 1e-6)) 
        
        # MCMC Sampling
        # Suppress progress bar for cleaner notebook output if desired
        trace = pm.sample(draws=2000, tune=1000, chains=2, cores=1, progressbar=True, random_seed=42) 
                                                                                    # cores=1 for reproducibility if issues
    
    # Analyze the trace (posterior samples)
    theta_a_samples = trace.posterior['theta_a'].values.flatten()
    theta_b_samples = trace.posterior['theta_b'].values.flatten()
    delta_abs_samples = trace.posterior['delta_abs'].values.flatten()
    delta_rel_samples = trace.posterior['delta_rel'].values.flatten()
    
    # Probability that B is better than A
    prob_b_better_than_a = (delta_abs_samples > 0).mean()
    
    print(f"\nPosterior Analysis:")
    print(f"Mean posterior conversion rate for A: {theta_a_samples.mean():.4f}")
    print(f"Mean posterior conversion rate for B: {theta_b_samples.mean():.4f}")
    print(f"Probability that Variant B is better than Variant A: {prob_b_better_than_a:.2%}")
    
    # Expected lift (relative improvement)
    expected_lift_mean = delta_rel_samples.mean()
    print(f"Expected relative lift of B over A (mean): {expected_lift_mean:.2%}")
    
    # Credible Intervals
    hdi_delta_abs = pm.hdi(delta_abs_samples, hdi_prob=0.95)
    hdi_delta_rel = pm.hdi(delta_rel_samples, hdi_prob=0.95)
    
    print(f"95% HDI for absolute difference (B - A): [{hdi_delta_abs[0]:.4f}, {hdi_delta_abs[1]:.4f}]")
    print(f"95% HDI for relative improvement of B over A: [{hdi_delta_rel[0]:.2%}, {hdi_delta_rel[1]:.2%}]")
    
    # Visualize posterior distributions (Matplotlib)
    plt.figure(figsize=(14, 10))
    
    plt.subplot(2, 2, 1)
    sns.histplot(theta_a_samples, bins=50, kde=True, label='Variant A Posterior CR', color='skyblue', stat="density")
    sns.histplot(theta_b_samples, bins=50, kde=True, label='Variant B Posterior CR', color='lightcoral', stat="density")
    plt.title('Posterior Distributions of Conversion Rates')
    plt.xlabel('Conversion Rate')
    plt.ylabel('Density')
    plt.legend()
    
    plt.subplot(2, 2, 2)
    sns.histplot(delta_abs_samples, bins=50, kde=True, color='mediumseagreen', stat="density")
    plt.axvline(x=0, color='black', linestyle='--')
    plt.title('Posterior Distribution of Absolute Difference (B - A)')
    plt.xlabel('Absolute Conversion Rate Difference')
    plt.ylabel('Density')
    
    plt.subplot(2, 2, 3)
    # Clip relative improvement for better visualization if extremes are present
    sns.histplot(np.clip(delta_rel_samples, -2, 2), bins=50, kde=True, color='mediumpurple', stat="density")
    plt.axvline(x=0, color='black', linestyle='--')
    plt.title('Posterior Distribution of Relative Improvement (B over A)')
    plt.xlabel('Relative Improvement (Clipped at +/- 200%)')
    plt.ylabel('Density')
    
    # Expected Loss "Risk" Plot (Example)
    # How much do we stand to lose if we choose B and A was actually better?
    # loss_if_b_chosen = np.maximum(0, theta_a_samples - theta_b_samples) # Loss if B is chosen but A is better
    # expected_loss_b = loss_if_b_chosen.mean()
    # loss_if_a_chosen = np.maximum(0, theta_b_samples - theta_a_samples) # Loss if A is chosen but B is better
    # expected_loss_a = loss_if_a_chosen.mean()
    # print(f"Expected loss if choosing B (and A was better): {expected_loss_b:.4f}")
    # print(f"Expected loss if choosing A (and B was better): {expected_loss_a:.4f}")
    # Plotting these can also be insightful for decision making.

    plt.subplot(2, 2, 4) # Summary bar chart with HDI
    variants = ['A', 'B']
    means = [theta_a_samples.mean(), theta_b_samples.mean()]
    hdi_a = pm.hdi(theta_a_samples, hdi_prob=0.95)
    hdi_b = pm.hdi(theta_b_samples, hdi_prob=0.95)
    errors = np.array([[means[0]-hdi_a[0], hdi_a[1]-means[0]], 
                       [means[1]-hdi_b[0], hdi_b[1]-means[1]]]).T

    plt.bar(variants, means, yerr=errors, capsize=5, color=['skyblue', 'lightcoral'], alpha=0.7)
    plt.title('Mean Conversion Rates with 95% HDI')
    plt.ylabel('Conversion Rate')
    plt.ylim(bottom=0)

    plt.tight_layout()
    plt.show()

    # Create an interactive comparison visualization using Plotly (example)
    fig_plotly_ab = make_subplots(rows=1, cols=3, 
                                  subplot_titles=('Posterior CR for A', 'Posterior CR for B', 'Posterior Difference (B-A)'))
    
    fig_plotly_ab.add_trace(go.Histogram(x=theta_a_samples, name='Variant A CR', marker_color='skyblue', histnorm='probability density'), row=1, col=1)
    fig_plotly_ab.add_trace(go.Histogram(x=theta_b_samples, name='Variant B CR', marker_color='lightcoral', histnorm='probability density'), row=1, col=2)
    fig_plotly_ab.add_trace(go.Histogram(x=delta_abs_samples, name='Delta (B-A)', marker_color='mediumseagreen', histnorm='probability density'), row=1, col=3)
    
    fig_plotly_ab.update_layout(title_text="Interactive Bayesian A/B Test Posterior Distributions (Plotly)", 
                                showlegend=False, height=400, width=1000)
    fig_plotly_ab.update_xaxes(title_text="Conv. Rate", row=1, col=1); fig_plotly_ab.update_xaxes(title_text="Conv. Rate", row=1, col=2)
    fig_plotly_ab.update_xaxes(title_text="Abs. Difference", row=1, col=3)
    fig_plotly_ab.show()

# %%
# Perform Bayesian A/B test
bayesian_ab_test(df_final)

# %%
"""
## 🏁 Conclusion & Next Steps

This project demonstrated the application of several advanced statistical techniques to analyze e-commerce customer behavior. Key findings include:
*   *(Summarize key insights from EDA, Hypothesis Testing, GLMs, Survival Analysis, Time Series, PCA, and A/B testing here based on actual run results)*
*   For example: "Weekend shopping showed a statistically significant higher conversion rate compared to weekdays."
*   "The Cox Proportional Hazards model identified `total_events_cox` and `purchase_count_cox` as significant predictors of customer retention."
*   "PCA revealed two primary dimensions of user behavior: one related to purchase frequency/volume and another to price sensitivity/browsing intensity."
*   "Bayesian A/B testing provided probabilistic insights into variant performance, suggesting Variant B has a X% probability of being better than A."

### Potential Next Steps:
1.  **Customer Segmentation:** Apply clustering algorithms (K-Means, DBSCAN, GMM) on PCA components or original user features to identify distinct customer segments.
2.  **Advanced Time Series Forecasting:** Use ARIMA, SARIMA, or Prophet models to forecast future sales or user activity.
3.  **Causal Inference:** Employ techniques like propensity score matching or regression discontinuity to understand the causal impact of specific interventions (e.g., promotions).
4.  **Personalization:** Develop models to predict individual user preferences or next actions, feeding into a recommendation system.
5.  **Deep Dive into Churn Drivers:** Further investigate factors influencing churn using more granular features and survival models by segments.
6.  **Deployment:** Package key models or insights into a dashboard or API for business stakeholders.

This comprehensive analysis provides a solid foundation for data-driven decision-making to enhance customer experience and optimize business strategies in the e-commerce domain.
"""

# %%
"""
*End of Notebook*
"""
```