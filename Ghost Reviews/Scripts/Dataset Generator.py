import os
import random
import pandas as pd
from datetime import datetime, timedelta

# Parameters
hotel_count = 50
review_count = 10000
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)

# Helper functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Sample data
hotel_names = [f"Hotel {i+1}" for i in range(hotel_count)]
review_text_pool = {
    "positive": ["Excellent service!", "Very clean and comfortable.", "Highly recommend this place."],
    "neutral": ["It was okay.", "Average experience.", "Could be better."],
    "negative": ["Terrible service!", "Room was dirty.", "Not worth the price."]
}

# Generate dataset
data = []
for _ in range(review_count):
    hotel_id = f"H{random.randint(1, hotel_count):03}"
    hotel_name = hotel_names[int(hotel_id[1:]) - 1]
    review_id = f"R{_ + 1:05}"
    rating = random.randint(1, 5)
    sentiment = (
        "positive" if rating >= 4 else "neutral" if rating == 3 else "negative"
    )
    review_text = random.choice(review_text_pool[sentiment])
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    ghost_review = random.choice([True, False])
    business_status = random.choice(["active", "inactive"])
    data.append(
        [hotel_id, hotel_name, review_id, review_text, rating, date, sentiment, ghost_review, business_status]
    )

# Create DataFrame
columns = ["Hotel ID", "Hotel Name", "Review ID", "Review Text", "Rating", "Date", "Sentiment", "Ghost Review", "Business Status"]
df = pd.DataFrame(data, columns=columns)

# Define save path
save_path = r"C:\Users\ASUS\Videos\OCR Table"

# Ensure directory exists
os.makedirs(save_path, exist_ok=True)

# Save to CSV
file_name = "hotel_reviews_dataset.csv"
full_path = os.path.join(save_path, file_name)
df.to_csv(full_path, index=False)
print(f"Dataset created and saved successfully at {full_path}!")
