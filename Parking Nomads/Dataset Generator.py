import pandas as pd
import numpy as np

# File path
file_path = r"C:\Users\ASUS\Videos\OCR Table\urban_parking_dataset.xlsx"

# Dataset Parameters
days_in_year = 365
transactions_per_day = 200  # Adjusted number of daily transactions
total_transactions = days_in_year * transactions_per_day

# Generate sample data
parking_spots_df = pd.DataFrame({
    "ID": range(1, 10001),
    "Location": np.random.choice(["Downtown", "Suburb", "Airport"], 10000),
    "Capacity": np.random.randint(10, 100, 10000),
    "Type": np.random.choice(["On-street", "Off-street", "Handicapped"], 10000),
    "Availability": np.random.choice([True, False], 10000)
})

predictive_df = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", periods=days_in_year),
    "Time": np.random.choice(["Morning", "Afternoon", "Evening", "Night"], days_in_year),
    "Forecasted Demand": np.random.randint(50, 500, days_in_year),
    "Confidence Interval": [f"{x}-{x+10}" for x in np.random.randint(50, 490, days_in_year)],
    "Event": np.random.choice(["Concert", "Sports Game", "Festival", "None"], days_in_year),
    "Weather": np.random.choice(["Sunny", "Rainy", "Snowy"], days_in_year)
})

driver_behavior_df = pd.DataFrame({
    "ID": range(1, 1001),
    "Search Time": np.random.randint(1, 30, 1000),
    "Fuel Consumption": np.random.uniform(0.1, 2.5, 1000).round(2),
    "Parking Preference": np.random.choice(["Closest", "Cheapest"], 1000),
    "Payment Method": np.random.choice(["Credit Card", "PayPal", "Cash"], 1000)
})

revenue_df = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", periods=days_in_year).repeat(transactions_per_day),
    "Time": np.random.choice(["Morning", "Afternoon", "Evening", "Night"], total_transactions),
    "Transaction Amount": np.random.uniform(5, 50, total_transactions).round(2),
    "Payment Method": np.random.choice(["Credit Card", "PayPal", "Cash"], total_transactions),
    "Revenue Stream": np.random.choice(["Parking Fees", "Advertising"], total_transactions)
})

# Save data to Excel
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    parking_spots_df.to_excel(writer, sheet_name="Parking Spots", index=False)
    predictive_df.to_excel(writer, sheet_name="Predictive Analytics", index=False)
    driver_behavior_df.to_excel(writer, sheet_name="Driver Behavior", index=False)
    revenue_df.to_excel(writer, sheet_name="Revenue Data", index=False)

print(f"Urban Parking Optimization dataset created and saved successfully at {file_path}!")
