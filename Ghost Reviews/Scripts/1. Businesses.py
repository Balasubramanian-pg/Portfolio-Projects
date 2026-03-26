import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# -------------------------------
# CONFIGURATION
# -------------------------------
SEED = 42
NUM_BUSINESSES = 2000
PCT_CLOSED = 0.30
START_DATE = datetime(2010, 1, 1)
OUTPUT_FILENAME = "businesses_realistic.csv"

np.random.seed(SEED)
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

CATEGORIES = ['Cafe', 'Restaurant', 'Bookstore', 'Electronics Store',
              'Clothing Store', 'Bar', 'Bakery', 'Gym']

CITY_CENTERS = {
    "Downtown": {'lat': 40.7128, 'lon': -74.0060, 'scale': 0.05},
    "Midtown": {'lat': 34.0522, 'lon': -118.2437, 'scale': 0.07},
    "Suburbia": {'lat': 41.8781, 'lon': -87.6298, 'scale': 0.15}
}

CHAIN_NAMES = ['QuickMart', 'Urban Cafe', 'FitZone', 'TechHub']

existing_ids = []
previous_locations = []

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def generate_id():
    if random.random() < 0.01 and existing_ids:
        return random.choice(existing_ids)  # duplicate ID
    return f"BIZ-{random.randint(10000, 99999)}"


def generate_location():
    center_name = random.choice(list(CITY_CENTERS.keys()))
    center = CITY_CENTERS[center]

    scale = center['scale'] * random.uniform(0.5, 1.5)
    lat = np.random.normal(center['lat'], scale)
    lon = np.random.normal(center['lon'], scale)

    # clamp
    lat = max(min(lat, 90), -90)
    lon = max(min(lon, 180), -180)

    # shared building
    if random.random() < 0.1 and previous_locations:
        return random.choice(previous_locations), center_name

    return (round(lat, 6), round(lon, 6)), center_name


def generate_opening_date():
    return START_DATE + timedelta(days=random.randint(0, 5000))


def hazard_probability(age_days):
    return min(0.0005 * age_days, 0.8)


def pandemic_bias(date):
    if datetime(2020, 3, 1) <= date <= datetime(2021, 12, 31):
        return random.random() < 0.6
    return False


def generate_closure(opening_date, category):
    age_days = (datetime.now() - opening_date).days

    if age_days < 180:
        return False, None

    base_prob = hazard_probability(age_days)

    # category survival bias
    if category == 'Bar':
        base_prob += 0.2
    elif category == 'Bookstore':
        base_prob -= 0.1

    if pandemic_bias(opening_date):
        base_prob += 0.3

    is_closed = random.random() < base_prob

    if not is_closed:
        return False, None

    min_close = opening_date + timedelta(days=90)
    max_close = datetime.now() - timedelta(days=1)

    if min_close >= max_close:
        return False, None

    closure_date = min_close + timedelta(
        days=random.randint(0, (max_close - min_close).days)
    )

    return True, closure_date


def category_by_location(center_name):
    if center_name == "Downtown":
        return random.choice(['Cafe', 'Bar', 'Restaurant', 'Bakery'])
    elif center_name == "Midtown":
        return random.choice(['Electronics Store', 'Clothing Store', 'Restaurant'])
    else:
        return random.choice(['Gym', 'Bookstore', 'Cafe'])


def introduce_typo(text):
    if random.random() < 0.1:
        return text[:-1]
    return text


def messy_case(text):
    r = random.random()
    if r < 0.05:
        return text.upper()
    elif r < 0.10:
        return text.lower()
    return text


def generate_revenue():
    return np.random.lognormal(mean=10, sigma=1.2)


def generate_reviews_and_rating():
    reviews = int(np.random.exponential(50))
    rating = np.clip(
        5 - np.log(reviews + 1)/2 + np.random.normal(0, 0.3),
        1, 5
    )
    return reviews, round(rating, 2)


def generate_popularity():
    return np.random.pareto(2.5) + 1


# -------------------------------
# MAIN GENERATION LOOP
# -------------------------------

business_data = []

for i in range(NUM_BUSINESSES):

    business_id = generate_id()
    existing_ids.append(business_id)

    opening_date = generate_opening_date()

    (latitude, longitude), center_name = generate_location()
    previous_locations.append((latitude, longitude))

    category = category_by_location(center_name)

    # category drift
    if random.random() < 0.05:
        category = random.choice(CATEGORIES)

    # missing category
    if random.random() < 0.05:
        category = None

    # chain logic
    is_chain = random.random() < 0.2

    if is_chain:
        name = random.choice(CHAIN_NAMES)
    else:
        name = fake.company()

    name = introduce_typo(name)
    name = messy_case(name)

    is_closed, closure_date = generate_closure(opening_date, category)

    # economic latent variable
    economic_index = np.random.normal(0, 1)

    revenue = generate_revenue() * (1 + economic_index * 0.2)
    popularity = generate_popularity()

    reviews, rating = generate_reviews_and_rating()

    # missing geo
    if random.random() < 0.03:
        latitude = None

    record = {
        "business_id": business_id,
        "business_name": name,
        "category": category,
        "latitude": latitude,
        "longitude": longitude,
        "center": center_name,
        "opening_date": opening_date.date(),
        "closure_date": closure_date.date() if closure_date else None,
        "status": "Closed" if is_closed else "Open",
        "is_chain": is_chain,
        "revenue": round(revenue, 2),
        "popularity_score": round(popularity, 2),
        "review_count": reviews,
        "rating": rating,
        "economic_index": round(economic_index, 3)
    }

    business_data.append(record)

# -------------------------------
# FINAL DATAFRAME
# -------------------------------

df = pd.DataFrame(business_data)

df['closure_date'] = pd.to_datetime(df['closure_date'])

df.to_csv(OUTPUT_FILENAME, index=False)

# -------------------------------
# OUTPUT SUMMARY
# -------------------------------

print("Dataset generated successfully")
print(f"Total records: {len(df)}")

print("\nSample Data:")
print(df.head())

print("\nStatus Distribution:")
print(df['status'].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())
