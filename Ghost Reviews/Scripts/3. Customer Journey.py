import pandas as pd
import numpy as np
import random

# --- Configuration Parameters ---
BUSINESSES_FILE = 'businesses.csv'
REVIEWS_FILE = 'reviews.csv'
OUTPUT_FILENAME = 'customer_journeys.csv'

NUM_JOURNEYS = 10000  # Number of customer journeys to simulate

# --- Assumption: Standardized economic impact per category ---
REVENUE_PER_CATEGORY = {
    'Cafe': 15.50,
    'Restaurant': 55.00,
    'Bookstore': 28.00,
    'Electronics Store': 120.00,
    'Clothing Store': 75.00,
    'Bar': 40.00,
    'Bakery': 12.00,
    'Gym': 30.00  # e.g., a day pass
}

# --- Helper Function ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two lat/lon points in km.
    This is a simplified distance calculation for our simulation.
    """
    R = 6371  # Radius of Earth in kilometers
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dLon / 2) * np.sin(dLon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

# --- Step 1: Load and Pre-process Data ---
print("Loading prerequisite data...")
try:
    df_businesses = pd.read_csv(BUSINESSES_FILE)
    df_reviews = pd.read_csv(REVIEWS_FILE)
except FileNotFoundError as e:
    print(f"Error: {e}. Make sure both '{BUSINESSES_FILE}' and '{REVIEWS_FILE}' exist.")
    exit()

# Calculate average rating for each business
print("Calculating average ratings...")
df_avg_ratings = df_reviews.groupby('business_id')['rating'].mean().reset_index()
df_avg_ratings = df_avg_ratings.rename(columns={'rating': 'avg_rating'})

# Create a master business DataFrame with all necessary info
df_master_biz = pd.merge(df_businesses, df_avg_ratings, on='business_id', how='left')
# Fill missing ratings (for any business that had no reviews) with a neutral score
df_master_biz['avg_rating'].fillna(2.5, inplace=True)

# --- Step 2: Main Simulation Loop ---
print(f"Simulating {NUM_JOURNEYS} customer journeys...")
journeys_list = []

for i in range(NUM_JOURNEYS):
    if (i + 1) % 1000 == 0:
        print(f"  ...simulated {i+1}/{NUM_JOURNEYS} journeys")

    # a. Simulate the customer's need and location
    search_category = random.choice(list(REVENUE_PER_CATEGORY.keys()))
    # Customer starts near a random business to ensure they are in a valid zone
    start_point = df_master_biz.sample(1).iloc[0]
    customer_lat = start_point['latitude'] + np.random.normal(0, 0.01)
    customer_lon = start_point['longitude'] + np.random.normal(0, 0.01)

    # b. Find potential businesses for the customer
    potential_biz = df_master_biz[df_master_biz['category'] == search_category].copy()
    if potential_biz.empty:
        continue # Skip if no businesses exist for this category

    # c. Calculate "Attractiveness Score" (Rating vs. Distance)
    potential_biz['distance_km'] = haversine_distance(
        customer_lat, customer_lon,
        potential_biz['latitude'], potential_biz['longitude']
    )
    # Add a small epsilon to distance to avoid division by zero
    potential_biz['attractiveness'] = potential_biz['avg_rating'] ** 2 / (potential_biz['distance_km'] + 0.1)

    # d. Make the Initial (Uninformed) Choice
    # Customer picks the business with the highest attractiveness, regardless of status
    initial_choice = potential_biz.loc[potential_biz['attractiveness'].idxmax()]
    initial_choice_id = initial_choice['business_id']
    
    # e. Check for a Ghost Interaction
    is_ghost_interaction = 1 if initial_choice['status'] == 'Permanently Closed' else 0
    
    # f. Determine Final Choice and Revenue Leakage
    if is_ghost_interaction:
        # The customer was misled, now they must find an OPEN alternative
        open_alternatives = potential_biz[potential_biz['status'] == 'Open']
        
        if not open_alternatives.empty:
            # They choose the best among the remaining open options
            final_choice = open_alternatives.loc[open_alternatives['attractiveness'].idxmax()]
            final_choice_id = final_choice['business_id']
            revenue_leaked = REVENUE_PER_CATEGORY[search_category]
        else:
            # No open alternative found, customer gives up
            final_choice_id = None
            revenue_leaked = 0
    else:
        # The initial choice was a valid, open business
        final_choice_id = initial_choice_id
        revenue_leaked = 0

    # g. Store the result
    journeys_list.append({
        'journey_id': f'JNY-{i+1:06d}',
        'customer_start_lat': round(customer_lat, 6),
        'customer_start_lon': round(customer_lon, 6),
        'search_category': search_category,
        'initial_choice_id': initial_choice_id,
        'is_ghost_interaction': is_ghost_interaction,
        'final_choice_id': final_choice_id,
        'revenue_leaked': revenue_leaked
    })

# --- Step 3: Finalize and Save ---
df_journeys = pd.DataFrame(journeys_list)
df_journeys.to_csv(OUTPUT_FILENAME, index=False)

print(f"\nSuccessfully generated {len(df_journeys)} journeys.")
print(f"Data saved to '{OUTPUT_FILENAME}'.")

# --- Verification Step ---
print("\n--- Simulation Summary ---")
ghost_interactions_count = df_journeys['is_ghost_interaction'].sum()
total_revenue_leaked = df_journeys['revenue_leaked'].sum()

print(f"Total ghost interactions detected: {ghost_interactions_count}")
print(f"Total estimated revenue leaked: ${total_revenue_leaked:,.2f}")

if ghost_interactions_count > 0:
    print("\nSample of ghost interactions:")
    print(df_journeys[df_journeys['is_ghost_interaction'] == 1].head())
