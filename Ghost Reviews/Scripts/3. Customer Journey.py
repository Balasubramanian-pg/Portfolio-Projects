import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration & Seed Control ---
random.seed(808)
np.random.seed(808)

# Input dependencies from previous simulations
BUSINESSES_FILE = 'simulated_businesses.csv' 
OUTPUT_FILENAME = 'simulated_customer_journeys.csv'

NUM_JOURNEYS = 25000  # Scaling up to build enough statistical depth
TODAY = datetime.now()
MIN_HISTORY_YEARS = 5

# Demand Power-Laws (Weighted likelihood of someone searching for this category)
CATEGORY_DEMAND_WEIGHTS = {
    'Restaurant': 35,
    'Cafe': 25,
    'Clothing Store': 10,
    'Bar': 12,
    'Bakery': 8,
    'Gym': 5,
    'Bookstore': 3,
    'Electronics Store': 2
}

# Lognormal Baseline spend params (Mean, Sigma) to replace flat assumptions
# Real economies feature heavily skewed spend variations
SPEND_BASE = {
    'Cafe': (np.log(14.0), 0.6),
    'Restaurant': (np.log(45.0), 0.8),
    'Bookstore': (np.log(25.0), 0.5),
    'Electronics Store': (np.log(150.0), 1.1),
    'Clothing Store': (np.log(75.0), 0.9),
    'Bar': (np.log(40.0), 0.7),
    'Bakery': (np.log(12.0), 0.4),
    'Gym': (np.log(20.0), 0.3) 
}

# Realistic Telemetry metadata sources
SEARCH_PLATFORMS =['iOS Maps', 'Android Google Maps', 'Web Search Desktop', 'Web Search Mobile', 'Direct Link']

print("[*] Initializing Spatiotemporal Customer Journey Simulator...")

# --- High-Performance Haversine Logic ---
def vectorized_haversine(lat1, lon1, lat_arr, lon_arr):
    """Calculates array-based distances instantly."""
    R = 6371  # Radius of Earth in kilometers
    dLat = np.radians(lat_arr - lat1)
    dLon = np.radians(lon_arr - lon1)
    a = np.sin(dLat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat_arr)) * np.sin(dLon / 2)**2
    return R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

# --- Step 1: Self-Healing Data Ingestion ---
print("[-] Loading infrastructure boundaries (Businesses)...")
try:
    df_biz = pd.read_csv(BUSINESSES_FILE)
except FileNotFoundError:
    print(f"[!] Critical Error: Make sure '{BUSINESSES_FILE}' exists in directory.")
    exit()

# System robustness: Date parsing with fallbacks
df_biz['opening_date'] = pd.to_datetime(df_biz['opening_date'], errors='coerce')
df_biz['closure_date'] = pd.to_datetime(df_biz['closure_date'], errors='coerce')
df_biz['average_rating'] = pd.to_numeric(df_biz['average_rating'], errors='coerce').fillna(3.5)

# Fast lookups mapping category names
search_categories = list(CATEGORY_DEMAND_WEIGHTS.keys())
search_weights = list(CATEGORY_DEMAND_WEIGHTS.values())

# We establish global coordinates to ensure customer starts inside viable geometry
avg_lat, avg_lon = df_biz['latitude'].mean(), df_biz['longitude'].mean()

# Extract list of available IDs and Data arrays
df_biz_cached = df_biz[['business_id', 'category', 'opening_date', 'closure_date', 'latitude', 'longitude', 'average_rating']].copy()


# --- Step 2: High-Velocity Journey Engine ---
print(f"[-] Compacting and running {NUM_JOURNEYS} complex lifecycle trajectories...")
journeys_list =[]

for i in range(NUM_JOURNEYS):
    if (i + 1) % 5000 == 0:
        print(f"    -> Computed {i+1}/{NUM_JOURNEYS} transactions.")

    # 1. Establish the Timestamp of this Journey
    # History stretches back dynamically. Journey time determines reality state.
    days_back = int(np.random.beta(2, 5) * (MIN_HISTORY_YEARS * 365))
    j_datetime = TODAY - timedelta(days=days_back)
    
    # 2. Emulate the Need & The Demographic constraint
    search_cat = random.choices(search_categories, weights=search_weights, k=1)[0]
    
    # Platform footprint & telemetry tracking
    platform = random.choices(SEARCH_PLATFORMS, weights=[40, 35, 10, 10, 5])[0]

    # Geographic initialization. 10% are extreme out-of-town searches
    if random.random() < 0.10:
        c_lat = avg_lat + np.random.normal(0, 0.5) 
        c_lon = avg_lon + np.random.normal(0, 0.5)
    else:
        # Bounded within cluster bounds
        anchor = df_biz.sample(1).iloc[0]
        c_lat = anchor['latitude'] + np.random.normal(0, 0.04)
        c_lon = anchor['longitude'] + np.random.normal(0, 0.04)

    # Calculate intrinsic financial scope (Log Normal Demand curve)
    base_mu, base_sig = SPEND_BASE[search_cat]
    planned_spend = max(2.50, round(np.random.lognormal(base_mu, base_sig), 2))

    # --- THE PHYSICAL SIMULATION: What did the search yield AT THIS SPECIFIC DATE? ---
    # First, rule out businesses that weren't born yet.
    mask = (df_biz_cached['category'] == search_cat) & (df_biz_cached['opening_date'] <= j_datetime)
    df_visible = df_biz_cached.loc[mask].copy()

    if df_visible.empty:
        # Organic data structural reality: Customer searched for a category not present yet in that era
        continue 
    
    # Apply distance computation efficiently
    df_visible['distance_km'] = vectorized_haversine(c_lat, c_lon, df_visible['latitude'].values, df_visible['longitude'].values)

    # Filter out bizarrely far logic (>100km unless specific conditions exist)
    df_visible = df_visible[df_visible['distance_km'] < 100]
    if df_visible.empty: continue

    # Attractiveness = Rating^3 / (Distance_km + Epsilon). Includes Gaussian SEO Noise.
    # Imperfect rationality is a major missing feature of basic synthetic datasets.
    info_friction_noise = np.random.normal(1.0, 0.4, size=len(df_visible)) 
    
    df_visible['attractiveness'] = ((df_visible['average_rating']**3) / (df_visible['distance_km'] + 0.5)) * info_friction_noise
    
    # User makes initial decision
    top_hit = df_visible.loc[df_visible['attractiveness'].idxmax()]
    initial_id = top_hit['business_id']

    # Was this a physical collision with a boarded up store? 
    # Must check if closed BEFORE the journey timestamp.
    # Note: If it closed a week AFTER the journey, the interaction is totally fine.
    is_ghost = pd.notnull(top_hit['closure_date']) and (top_hit['closure_date'] < j_datetime)
    
    actual_spend = 0.0
    final_id = None
    ghost_flag_code = 0
    search_fatigue = False
    
    if is_ghost:
        ghost_flag_code = 1
        # The Ghost routing protocol: User bounces off a locked door. Do they find another place?
        # Fatgue dictates a 40% rage-quit drop-off metric. (Total Revenue Ecosystem Bleed)
        if random.random() < 0.40:
            search_fatigue = True
            # Leaked entirely
        else:
            # We look for the NEXT best. Note: System glitch... sometimes they bounce to ANOTHER closed store.
            df_visible_rest = df_visible.drop(top_hit.name)
            if not df_visible_rest.empty:
                bounce_hit = df_visible_rest.loc[df_visible_rest['attractiveness'].idxmax()]
                
                is_bounce_ghost = pd.notnull(bounce_hit['closure_date']) and (bounce_hit['closure_date'] < j_datetime)
                if not is_bounce_ghost:
                    # Successfully navigated
                    final_id = bounce_hit['business_id']
                    # Rage penalty on wallet
                    actual_spend = max(1.00, planned_spend * random.uniform(0.6, 0.95))
                else:
                    search_fatigue = True # Double-fail, always yields rage quit.
    else:
        # Standard clean transactional operation
        final_id = initial_id
        actual_spend = planned_spend

    
    # Determine absolute system damage metrics
    leaked_funds = 0.0 if not search_fatigue else planned_spend

    # Insert noise directly on device coordinates occasionally simulating GPS / Telemetry lag
    record_lat = c_lat if random.random() < 0.98 else np.nan
    record_lon = c_lon if random.random() < 0.98 else np.nan
    
    # Compile analytical footprint
    journey = {
        'journey_id': f'JNY-{100000+i:07d}',
        'user_cookie': f"U_{''.join(random.choices('0123456789ABCDEF', k=12))}",
        'platform': platform if random.random() < 0.99 else np.nan,
        'journey_timestamp': j_datetime.isoformat(timespec='seconds'),
        'client_lat_origin': round(record_lat, 6) if pd.notnull(record_lat) else record_lat,
        'client_lon_origin': round(record_lon, 6) if pd.notnull(record_lon) else record_lon,
        'search_category': search_cat,
        'distance_driven_km': round(top_hit['distance_km'], 2),
        'intended_biz_target': initial_id,
        'ghost_collision_event': ghost_flag_code,
        'rage_quit_dropoff': 1 if search_fatigue else 0,
        'final_visited_biz': final_id if pd.notna(final_id) else None,
        'economic_transaction_value': round(actual_spend, 2),
        'ecosystem_value_leaked': round(leaked_funds, 2)
    }
    journeys_list.append(journey)

# --- Output Pipeline and Degradation Simulation ---
print("[*] Formatting systemic boundaries...")

df_journeys = pd.DataFrame(journeys_list)

# Data Normalization Friction (Inject formatting inconsistency typical of legacy databases)
def temporal_skew(dt_str):
    if pd.isnull(dt_str): return dt_str
    if random.random() < 0.05:
        # Remove standard 'T' from iso formatting natively to irritate parsers later
        return dt_str.replace("T", " ")
    return dt_str

df_journeys['journey_timestamp'] = df_journeys['journey_timestamp'].apply(temporal_skew)

# Output operation
df_journeys.to_csv(OUTPUT_FILENAME, index=False)

# --- Executive Audit / QA Analytics ---
print(f"\n[+] Processing Phase Finished. Yielded {len(df_journeys)} simulated traces to '{OUTPUT_FILENAME}'.")
print("\n========== CUSTOMER PLATFORM INTEGRITY AUDIT ==========")

gross_platform = df_journeys['economic_transaction_value'].sum()
ghost_damage = df_journeys['ecosystem_value_leaked'].sum()

print(f"[-] Cumulative Capital Facilitated: ${gross_platform:,.2f}")
print(f"[-] Defective Ecosystem Deficit (Revenue Bleed): ${ghost_damage:,.2f}")

collision_rate = df_journeys['ghost_collision_event'].mean() * 100
abandonment_rate = df_journeys[df_journeys['ghost_collision_event'] == 1]['rage_quit_dropoff'].mean() * 100
print(f"[-] Ghost Interaction Incident Volume: {collision_rate:.1f}% of total sessions.")
print(f"[-] Post-Collision Abandonment (Rage-Quit) Profile: {abandonment_rate:.1f}%")

print("\n[-] Spend Anomalies (Min/Max vs Category Bounds):")
metrics = df_journeys.groupby('search_category')['economic_transaction_value'].agg(['mean', 'max', lambda x: x[x>0].min()])
metrics.rename(columns={'mean': 'Average Basket', 'max': 'High-Roller Check', '<lambda_0>': 'Floor Value'}, inplace=True)
print(metrics.round(2))

telemetry_loss = df_journeys['client_lat_origin'].isna().sum()
print(f"\n[!] Log Pipeline Notice: Caught {telemetry_loss} client connections missing payload telemetry coordinates.")
