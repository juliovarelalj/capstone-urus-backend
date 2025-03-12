import random
import csv

# List of exchanges from your dataset (example list based on your selection)
exchanges = [
    "NYSE",      # New York Stock Exchange
    "NASDAQ",    # NASDAQ
    "LSE",       # London Stock Exchange
    "JPX",       # Japan Exchange Group
    "SSE",       # Shanghai Stock Exchange
    "HKEX",      # Hong Kong Stock Exchange
    "Euronext",  # Euronext
    "TSX",       # Toronto Stock Exchange
    "BSE",       # Bombay Stock Exchange
    "ASX"        # Australian Securities Exchange
]

# Possible risk profiles and time horizons for exchanges
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 exchange portfolios
# Since the list of exchanges is small, we randomly select between 3 and all available exchanges per portfolio
for i in range(1, 21):
    num_exchanges = random.randint(3, len(exchanges))
    subset = random.sample(exchanges, num_exchanges)
    
    # Assign random weights (random integers between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_exchanges)]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "EXCHANGE:XX.XX%"
    assets_str_parts = [f"{exch}:{weight:.2f}%" for exch, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For exchanges, we use moderate ranges (typically low volatility, as these are indices of markets)
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.005, 0.015), 3)  # e.g., 0.5%-1.5%
        average_return = round(random.uniform(0.002, 0.005), 3)          # e.g., 0.2%-0.5%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.015, 0.03), 3)   # e.g., 1.5%-3%
        average_return = round(random.uniform(0.005, 0.01), 3)         # e.g., 0.5%-1%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.03, 0.05), 3)    # e.g., 3%-5%
        average_return = round(random.uniform(0.01, 0.02), 3)           # e.g., 1%-2%
    
    # Portfolio name
    portfolio_name = f"Exchanges_Portfolio_{i}"
    
    # Append the portfolio row to our list
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "exchanges_portfolios.csv"
with open("exchanges_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'exchanges_portfolios.csv' has been created successfully.")
