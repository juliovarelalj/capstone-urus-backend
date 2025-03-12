import random
import csv

# List of currencies from your dataset (example list)
currencies = [
    "USD",  # US Dollar
    "EUR",  # Euro
    "JPY",  # Japanese Yen
    "GBP",  # British Pound
    "AUD",  # Australian Dollar
    "CAD",  # Canadian Dollar
    "CHF",  # Swiss Franc
    "CNY",  # Chinese Yuan
    "HKD",  # Hong Kong Dollar
    "NZD"   # New Zealand Dollar
]

# Possible risk profiles and time horizons for currencies
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 currency portfolios
for i in range(1, 21):
    # Randomly select the number of currencies to include (between 5 and 10)
    num_currencies = random.randint(5, len(currencies))
    # Choose a random subset of currencies from the list
    subset = random.sample(currencies, num_currencies)
    
    # Assign random weights (random integers between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_currencies)]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "CURRENCY:XX.XX%"
    assets_str_parts = [f"{cur}:{weight:.2f}%" for cur, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For currencies, we assume relatively low volatility and modest returns
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.001, 0.005), 3)  # e.g., 0.1% - 0.5%
        average_return = round(random.uniform(0.001, 0.003), 3)        # e.g., 0.1% - 0.3%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.005, 0.01), 3)   # e.g., 0.5% - 1%
        average_return = round(random.uniform(0.003, 0.007), 3)        # e.g., 0.3% - 0.7%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.01, 0.02), 3)    # e.g., 1% - 2%
        average_return = round(random.uniform(0.007, 0.015), 3)        # e.g., 0.7% - 1.5%
    
    # Portfolio name
    portfolio_name = f"Currency_Portfolio_{i}"
    
    # Append the portfolio row
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "currencies_portfolios.csv"
with open("currencies_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'currencies_portfolios.csv' has been created successfully.")
