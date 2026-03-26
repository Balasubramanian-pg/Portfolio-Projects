import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# --- Configuration & Reproducibility ---
random.seed(42)
np.random.seed(42)
fake = Faker()

NUM_BUSINESSES = 2500
START_DATE = datetime(2010, 1, 1) # Earlier start date to allow history
TODAY = datetime.now()

OUTPUT_FILENAME = 'simulated_businesses.csv'

# Base Definitions
CATEGORIES =['Cafe', 'Restaurant', 'Bookstore', 'Electronics Store', 'Clothing Store', 'Bar', 'Bakery', 'Gym']
CHAIN_NAMES = ['Star Coffee', 'QuickMart', 'FitZone', 'Burger King', 'TechHub', 'Urban Cafe']

# Category location biases (Guardrail 9)
CATEGORY_WEIGHTS = {
    "Downtown":['Cafe', 'Restaurant', 'Bar', 'Bakery'],
    "Midtown":['Electronics Store', 'Clothing Store', 'Restaurant', 'Gym'],
    "Suburbia":['Gym', 'Bookstore', 'Cafe', 'Clothing Store']
}

CITY_CENTERS = {
    "Downtown":    {'lat': 40.7128, 'lon': -74.0060, 'scale': 0.05}, # Dense
    "Midtown":     {'lat': 34.0522, 'lon': -118.2437, 'scale': 0.08},
    "Suburbia":    {'lat': 41.8781, 'lon': -87.6298, 'scale': 0.20}  # Sparse
}

print("Initializing Economic Simulation Engine...")

business_data = []
existing_ids =[]
previous_location = None

for i in range(NUM_BUSINESSES):
    # --- 5. STATISTICAL STRUCTURE: Hidden Variables ---
    # Guardrail 22 (Hidden Stat): Latent Economic Index (-2 to 2). Affects survival and revenue.
    economic_index = np.random.normal(0, 1) 

    # --- 1. IDENTITY & RECORD INTEGRITY ---
    # Guardrail 1: Non-sequential, partially structured IDs
    business_id = f"BIZ-{random.randint(10000, 99999)}"
    
    # Guardrail 2: Occasional duplicate IDs (system bugs)
    if existing_ids and random.random() < 0.01:
        business_id = random.choice(existing_ids)
    else:
        existing_ids.append(business_id)

    # --- 3. GEOGRAPHIC REALISM ---
    center_name = random.choice(list(CITY_CENTERS.keys()))
    center = CITY_CENTERS[center_name]

    # Guardrail 11: Shared coordinates (same building / duplicate data)
    if previous_location and random.random() < 0.1:
        latitude, longitude = previous_location
    else:
        # Guardrail 10: Coordinate clustering with noise (Density variation)
        scale_mod = random.uniform(0.5, 1.5)
        latitude = np.random.normal(center['lat'], center['scale'] * scale_mod)
        longitude = np.random.normal(center['lon'], center['scale'] * scale_mod)
        
        # Guardrail: Avoid impossible coordinates (Clamping)
        latitude = max(min(latitude, 90.0), -90.0)
        longitude = max(min(longitude, 180.0), -180.0)
        
        latitude, longitude = round(latitude, 6), round(longitude, 6)
        previous_location = (latitude, longitude)

    # --- 4. BUSINESS BEHAVIOR & LOGIC ---
    # Guardrail 14 & 15: Chain vs Independent logic
    is_chain = random.random() < 0.20
    if is_chain:
        raw_name = random.choice(CHAIN_NAMES)
    else:
        raw_name = fake.company()

    # Guardrail 9: Location-based category bias
    if random.random() < 0.7:  # 70% chance to follow location archetype
        category = random.choice(CATEGORY_WEIGHTS[center_name])
    else:
        category = random.choice(CATEGORIES)

    # --- 2. TEMPORAL REALISM ---
    # Guardrail 4: Opening date required
    opening_date = START_DATE + timedelta(days=random.randint(0, (TODAY - START_DATE).days))
    age_days = (TODAY - opening_date).days

    # Guardrail 16: Category drift / Time-based Cohort Effects
    if opening_date.year < 2015 and random.random() < 0.3:
        category = random.choice(['Bookstore', 'Bakery', 'Cafe']) # Older businesses skew traditional

    # --- SURVIVAL ANALYSIS (Hazard Function) ---
    is_closed = False
    closure_date = None
    
    # Guardrail 7: Recent businesses rarely closed
    if age_days > 180:
        # Hazard probability increases with age
        hazard_prob = min(0.0005 * age_days, 0.8)
        
        # Guardrail 13: Category-specific survival rates
        if category == 'Bar': hazard_prob *= 1.5       # Fail faster
        if category == 'Bookstore': hazard_prob *= 0.7 # Survive longer
        
        # Chains are less likely to close
        if is_chain: hazard_prob *= 0.4 
        
        # Latent economy shifts hazard
        hazard_prob -= (economic_index * 0.1) 
        
        is_closed = random.random() < hazard_prob

    # Guardrail 5 & 6 & 8: Lifespan logic & Pandemic Spike
    if is_closed:
        min_close_date = opening_date + timedelta(days=90) # Min lifespan 90 days
        max_close_days = (TODAY - min_close_date).days
        
        if max_close_days <= 0:
            is_closed = False # Force open if it hasn't lived long enough yet
        else:
            # Determine when it closed
            closure_date = min_close_date + timedelta(days=random.randint(0, max_close_days))
            
            # Guardrail 8: Economic shock (Pandemic bias)
            if min_close_date < datetime(2021, 12, 31) and opening_date < datetime(2020, 3, 1):
                if random.random() < 0.6: # 60% of struggling businesses failed during pandemic
                    p_start = max(min_close_date, datetime(2020, 3, 1))
                    p_end = datetime(2021, 12, 31)
                    if p_start < p_end:
                        closure_date = p_start + timedelta(days=random.randint(0, (p_end - p_start).days))

    # --- 5. STATISTICAL STRUCTURE ---
    # Guardrail 17: Heavy-tailed popularity (Power-Law)
    popularity_score = round(np.random.pareto(a=2.5) + 1, 2)

    # Guardrail 18: Log-Normal Revenue Distribution
    revenue_mean = 10 + (0.5 if is_chain else 0) + (economic_index * 0.2)
    revenue = round(np.random.lognormal(mean=revenue_mean, sigma=1.2), 2)

    # Guardrail 19: Review Count vs Rating Correlation
    # Large businesses stabilize around 3.5-4.2, small are volatile
    review_count = int(np.random.exponential(50 * popularity_score))
    rating_noise = np.random.normal(0, max(0.1, 1.0 / (np.log(review_count + 2)))) 
    # Formula tweaking user's idea to ensure it converges realistically
    rating = np.clip(3.8 + rating_noise, 1.0, 5.0) if review_count > 0 else 0.0
    rating = round(rating, 1)

    # --- 6. DATA QUALITY IMPERFECTIONS ---
    
    # Guardrail 21: Typographical noise & Inconsistent formats
    name = raw_name
    if random.random() < 0.05:
        name = name.lower()
    elif random.random() < 0.05:
        name = name.upper()
    
    if random.random() < 0.05 and len(name) > 3:
        name = name[:-1] # Typo: dropped last letter

    # Guardrail 20 & 12: Missing fields
    if random.random() < 0.03: latitude = None
    if random.random() < 0.03: longitude = None
    if random.random() < 0.02: category = None

    # Compile the final record
    business = {
        'business_id': business_id,
        'business_name': name,
        'is_chain': is_chain,
        'category': category,
        'neighborhood': center_name,
        'latitude': latitude,
        'longitude': longitude,
        'opening_date': opening_date.date(),
        'status': 'Permanently Closed' if is_closed else 'Open',
        'closure_date': closure_date.date() if closure_date else None,
        'popularity_score': popularity_score,
        'annual_revenue': revenue,
        'review_count': review_count,
        'average_rating': rating if review_count > 0 else None
    }
    
    business_data.append(business)

# --- Final Output and Formatting ---
df = pd.DataFrame(business_data)

# Ensure pandas handles dates properly
df['opening_date'] = pd.to_datetime(df['opening_date'])
df['closure_date'] = pd.to_datetime(df['closure_date'])

# Save to CSV
df.to_csv(OUTPUT_FILENAME, index=False)

print(f"\nSuccessfully generated {NUM_BUSINESSES} records.")
print(f"Data saved to '{OUTPUT_FILENAME}'.")

# --- Verification & Analytics ---
print("\n--- Data Quality Checks ---")
print(f"Missing Categories: {df['category'].isna().sum()}")
print(f"Missing Coordinates: {df['latitude'].isna().sum()}")
print(f"Duplicate IDs: {df.duplicated(subset=['business_id']).sum()}")

print("\n--- Statistical Realism Checks ---")
print("Status Distribution:")
print(df['status'].value_counts(normalize=True).map('{:.1%}'.format))

print("\nChain vs Independent Survival Rate:")
print(df.groupby('is_chain')['status'].value_counts(normalize=True).unstack().fillna(0).applymap('{:.1%}'.format))

print("\nClosure Rate by Category (Notice Bars vs Bookstores):")
cat_closure = df[df['status'] == 'Permanently Closed']['category'].value_counts() / df['category'].value_counts()
print(cat_closure.sort_values(ascending=False).map('{:.1%}'.format).head())

print("\nRevenue Distribution (Min / Median / Max):")
print(f"${df['annual_revenue'].min():,.0f} / ${df['annual_revenue'].median():,.0f} / ${df['annual_revenue'].max():,.0f}")

print("\nData Sample:")
print(df[['business_id', 'business_name', 'category', 'status', 'opening_date', 'review_count']].head(5))
