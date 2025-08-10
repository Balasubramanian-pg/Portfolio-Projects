import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Parameters
num_products = 10000
num_transactions = 100000
num_resales = 20000
num_surveys = 5000
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)

# Helper Functions
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# 1. Products Table
products = []
categories = ["Electronics", "Clothing", "Home & Kitchen", "Beauty", "Sports"]
for i in range(1, num_products + 1):
    products.append({
        "product_id": f"P{i:05}",
        "product_name": fake.word().capitalize(),
        "product_category": random.choice(categories),
        "price": round(random.uniform(5, 500), 2)
    })
products_df = pd.DataFrame(products)

# 2. Transactions Table
transactions = []
for i in range(1, num_transactions + 1):
    transactions.append({
        "transaction_id": f"T{i:06}",
        "product_id": random.choice(products_df["product_id"]),
        "purchase_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
        "amount": round(random.uniform(5, 500), 2),
        "payment_method": random.choice(["Credit Card", "PayPal", "Cash"]),
        "customer_demographics": f"{random.randint(18, 65)} years, {fake.city()}, {fake.random_element(['Low', 'Medium', 'High'])} Income"
    })
transactions_df = pd.DataFrame(transactions)

# 3. Resale and Return Table
resales = []
for i in range(1, num_resales + 1):
    resales.append({
        "resale_id": f"R{i:06}",
        "product_id": random.choice(products_df["product_id"]),
        "resale_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
        "resale_amount": round(random.uniform(5, 400), 2),
        "return_id": f"RT{i:06}",
        "return_date": random_date(start_date, end_date).strftime("%Y-%m-%d"),
        "return_reason": random.choice(["Defective", "Not as described", "Changed mind"])
    })
resales_df = pd.DataFrame(resales)

# 4. User Surveys Table
surveys = []
for i in range(1, num_surveys + 1):
    surveys.append({
        "survey_id": f"S{i:05}",
        "product_id": random.choice(products_df["product_id"]),
        "purchase_motivation": random.choice(["Price", "Trend", "Recommendation"]),
        "regret_level": random.choice(["Low", "Medium", "High"]),
        "satisfaction": random.choice(["Satisfied", "Neutral", "Dissatisfied"]),
        "demographic_data": f"{random.randint(18, 65)} years, {fake.city()}, {fake.random_element(['Low', 'Medium', 'High'])} Income"
    })
surveys_df = pd.DataFrame(surveys)

# Save to Excel with multiple sheets
file_path = r"C:\Users\ASUS\Videos\OCR Table\dataset.xlsx"
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    products_df.to_excel(writer, sheet_name="Products", index=False)
    transactions_df.to_excel(writer, sheet_name="Transactions", index=False)
    resales_df.to_excel(writer, sheet_name="Resale & Return", index=False)
    surveys_df.to_excel(writer, sheet_name="User Surveys", index=False)

print(f"Dataset created and saved successfully at {file_path}!")
