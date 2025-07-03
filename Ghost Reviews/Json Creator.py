import os
import random
import pandas as pd
from datetime import datetime, timedelta
import json

# Parameters
hotel_count = 50
review_count = 10000
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)

# Helper function
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
for i in range(review_count):
    hotel_id = f"H{random.randint(1, hotel_count):03}"
    hotel_name = hotel_names[int(hotel_id[1:]) - 1]
    review_id = f"R{i + 1:05}"
    rating = random.randint(1, 5)
    sentiment = (
        "positive" if rating >= 4 else "neutral" if rating == 3 else "negative"
    )
    review_text = random.choice(review_text_pool[sentiment])
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    ghost_review = random.choice([True, False])
    business_status = random.choice(["active", "inactive"])
    
    data.append({
        "Hotel ID": hotel_id,
        "Hotel Name": hotel_name,
        "Review ID": review_id,
        "Review Text": review_text,
        "Rating": rating,
        "Date": date,
        "Sentiment": sentiment,
        "Ghost Review": ghost_review,
        "Business Status": business_status
    })

# Create DataFrame
df = pd.DataFrame(data)

# Define save path
save_path = r"C:\Users\ASUS\Videos\OCR Table"
os.makedirs(save_path, exist_ok=True)

# Save to JSON
file_name = "hotel_reviews_dataset.json"
full_path = os.path.join(save_path, file_name)
df.to_json(full_path, orient='records', indent=4)

print(f"Dataset created and saved successfully as JSON at {full_path}!")
