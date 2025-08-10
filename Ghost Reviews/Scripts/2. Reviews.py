import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration Parameters ---
INPUT_FILENAME = 'businesses.csv'
OUTPUT_FILENAME = 'reviews.csv'
MIN_REVIEWS_PER_BIZ = 15      # Minimum reviews a business can have
MAX_REVIEWS_PER_BIZ = 250     # Maximum reviews a business can have
GHOST_REVIEW_PROBABILITY = 0.15 # 15% chance a review for a closed biz is a "ghost review"

# --- Assumption: Review text is strongly correlated with rating ---
REVIEW_TEXT_TEMPLATES = {
    5: ["Absolutely fantastic! Best experience ever.", "A must-visit. Five stars all the way!", "Incredible service and quality. Highly recommended.", "Perfect in every way. I'll be back!", "Loved it! You won't be disappointed."],
    4: ["Very good experience, just a few minor issues.", "Great place, really enjoyed my time here.", "Solid choice, would recommend to friends.", "Impressive overall, happy with the service.", "A really nice spot, almost perfect."],
    3: ["It was okay. Nothing special, but not bad either.", "An average experience. Met expectations.", "Decent, but there's room for improvement.", "Good, but not great. Fairly standard.", "Middle of the road. It gets the job done."],
    2: ["Quite disappointing. I wouldn't go back.", "Not a great experience. Had several problems.", "Below average. Expected much more.", "Unfortunately, it was a letdown.", "Needs a lot of improvement."],
    1: ["A terrible experience from start to finish. Avoid.", "Absolutely awful. A complete waste of time and money.", "Worst service I have ever received.", "Do not go here. You've been warned.", "Horrible. I wish I could give zero stars."]
}

# --- Helper Functions ---
def generate_review_text(rating):
    """Selects a random text template based on the star rating."""
    return random.choice(REVIEW_TEXT_TEMPLATES[rating])

def generate_random_date(start_date, end_date):
    """Generates a random date between two given dates."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

print(f"Loading business data from '{INPUT_FILENAME}'...")
try:
    df_businesses = pd.read_csv(INPUT_FILENAME)
except FileNotFoundError:
    print(f"Error: The file '{INPUT_FILENAME}' was not found.")
    print("Please run the script to generate the business dataset first.")
    exit()

# Ensure date columns are in datetime format for comparison
df_businesses['closure_date'] = pd.to_datetime(df_businesses['closure_date'])
today = datetime.now()

# --- Main Script ---
reviews_list = []
review_id_counter = 1

print("Generating reviews for each business...")

# Iterate through each business to generate reviews for it
for index, business in df_businesses.iterrows():
    business_id = business['business_id']
    status = business['status']
    closure_date = business['closure_date']

    num_reviews = random.randint(MIN_REVIEWS_PER_BIZ, MAX_REVIEWS_PER_BIZ)
    
    # --- Assumption: Closed businesses were historically popular (higher ratings) ---
    if status == 'Permanently Closed':
        # Skew ratings to be higher for closed businesses
        rating_probabilities = [0.05, 0.05, 0.15, 0.35, 0.40] # Higher chance of 4 or 5
    else:
        # Standard rating distribution for open businesses
        rating_probabilities = [0.10, 0.10, 0.20, 0.30, 0.30]

    for _ in range(num_reviews):
        # Generate rating and corresponding text
        rating = np.random.choice([1, 2, 3, 4, 5], p=rating_probabilities)
        review_text = generate_review_text(rating)
        
        # --- Assumption: Systematic generation of Ghost Reviews ---
        review_date = None
        if status == 'Permanently Closed':
            # Decide if this will be a ghost review
            if random.random() < GHOST_REVIEW_PROBABILITY:
                # GHOST REVIEW: Date is *after* closure
                review_date = generate_random_date(closure_date, today)
            else:
                # NORMAL REVIEW: Date is *before* closure
                # Assuming business was "born" 5 years before closure for review history
                start_review_period = closure_date - timedelta(days=5*365)
                review_date = generate_random_date(start_review_period, closure_date)
        else:
            # For open businesses, reviews can be from any time in the last 5 years
            start_review_period = today - timedelta(days=5*365)
            review_date = generate_random_date(start_review_period, today)

        # Create the review record
        reviews_list.append({
            'review_id': f'REV-{review_id_counter:07d}',
            'business_id': business_id,
            'user_id': f'USER-{random.randint(1000, 99999)}',
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date.date()
        })
        review_id_counter += 1

# Convert list to DataFrame and save to CSV
df_reviews = pd.DataFrame(reviews_list)
df_reviews.to_csv(OUTPUT_FILENAME, index=False)

print(f"\nSuccessfully generated {len(df_reviews)} reviews.")
print(f"Data saved to '{OUTPUT_FILENAME}'.")

# --- Verification Step ---
# Check for ghost reviews to confirm the script worked
df_merged = pd.merge(df_reviews, df_businesses, on='business_id')
df_merged['review_date'] = pd.to_datetime(df_merged['review_date'])

ghost_reviews = df_merged[
    (df_merged['status'] == 'Permanently Closed') &
    (df_merged['review_date'] > df_merged['closure_date'])
]

print(f"\n--- Verification ---")
print(f"Total ghost reviews found: {len(ghost_reviews)}")
if not ghost_reviews.empty:
    print("Ghost review generation was successful. Sample:")
    print(ghost_reviews[['business_id', 'status', 'closure_date', 'review_date']].head())
else:
    print("No ghost reviews were generated. Check configuration.")
