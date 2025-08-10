import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# --- Configuration Parameters ---
NUM_BUSINESSES = 2000          # Total number of businesses to generate
PCT_CLOSED = 0.30              # Percentage of businesses that are permanently closed (30%)
START_DATE = datetime(2018, 1, 1) # The earliest a business could have closed
OUTPUT_FILENAME = 'businesses.csv'

# Define business categories
CATEGORIES = ['Cafe', 'Restaurant', 'Bookstore', 'Electronics Store', 'Clothing Store', 'Bar', 'Bakery', 'Gym']

# Define geographic clusters (city centers) to make the data realistic
# Using real-world coordinates for realism
CITY_CENTERS = {
    "Downtown":    {'lat': 40.7128, 'lon': -74.0060, 'scale': 0.1},
    "Midtown":     {'lat': 34.0522, 'lon': -118.2437, 'scale': 0.08},
    "Suburbia":    {'lat': 41.8781, 'lon': -87.6298, 'scale': 0.2}
}

# --- Main Script ---

# Initialize Faker for generating fake data
fake = Faker()

def generate_location():
    """
    Selects a random city center and generates a latitude/longitude
    coordinate with some noise to create a realistic cluster.
    """
    # Choose a random city center from our defined clusters
    center_name = random.choice(list(CITY_CENTERS.keys()))
    center = CITY_CENTERS[center_name]

    # Generate coordinates with a normal distribution around the center
    # The 'scale' determines how spread out the businesses are
    lat = np.random.normal(loc=center['lat'], scale=center['scale'])
    lon = np.random.normal(loc=center['lon'], scale=center['scale'])

    return round(lat, 6), round(lon, 6)

def generate_closure_date():
    """
    Generates a random closure date between START_DATE and yesterday.
    This function is only called for businesses marked as closed.
    """
    end_date = datetime.now() - timedelta(days=1)
    total_days = (end_date - START_DATE).days
    random_days = random.randint(0, total_days)
    return START_DATE + timedelta(days=random_days)

print("Generating business data...")

# Create a list to hold all the business records (as dictionaries)
business_data = []

for i in range(NUM_BUSINESSES):
    # --- Assumption 1: A significant minority of businesses are closed ---
    is_closed = random.random() < PCT_CLOSED
    
    if is_closed:
        status = 'Permanently Closed'
        closure_date = generate_closure_date().date()
    else:
        status = 'Open'
        closure_date = None # Use None for open businesses

    # --- Assumption 2: Businesses are geographically clustered ---
    latitude, longitude = generate_location()

    # Create the business record
    business = {
        'business_id': f'BIZ-{i+1:05d}',  # Formats as BIZ-00001
        'business_name': fake.company(),
        'category': random.choice(CATEGORIES),
        'latitude': latitude,
        'longitude': longitude,
        'status': status,
        'closure_date': closure_date
    }
    
    business_data.append(business)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(business_data)

# Ensure the closure_date is in the correct format (Pandas NaT for missing)
df['closure_date'] = pd.to_datetime(df['closure_date'])

# Save the DataFrame to a CSV file
df.to_csv(OUTPUT_FILENAME, index=False)

print(f"Successfully generated {NUM_BUSINESSES} records.")
print(f"Data saved to '{OUTPUT_FILENAME}'.")

# Display a sample of the data and stats
print("\n--- Data Sample ---")
print(df.head())

print("\n--- Data Summary ---")
print(df.info())

print("\n--- Status Distribution ---")
print(df['status'].value_counts())
