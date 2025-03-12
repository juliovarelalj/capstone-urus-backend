import random
import csv

# List of market indices from your dataset (example list based on your selection)
market_indices = [
    "SPX",       # S&P 500
    "DJI",       # Dow Jones Industrial Average
    "NDX",       # NASDAQ 100
    "FTSE",      # FTSE 100
    "DAX",       # DAX (Germany)
    "CAC",       # CAC 40 (France)
    "NIK",       # Nikkei 225 (Japan)
    "HSI",       # Hang Seng Index (Hong Kong)
    "SSE",       # Shanghai Composite (China)
    "BOVESPA",   # Bovespa (Brazil)
    "TSX",       # Toronto Stock Exchange
    "ASX",       # Australian Securities Exchange
    "NIFTY",     # Nifty 50 (India)
    "KOSPI",     # KOSPI (South Korea)
    "IPC"        # IPC (Mexico)
    # Add more indices if your dataset contains them
]

# Possible risk profiles and time horizons for market indices
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 market indices portfolios
for i in range(1, 21):
    # Randomly select the number of indices to include (between 10 and 20)
    num_indices = random.randint(10, 20)
    # Choose a random subset of indices from the list (if the list has less than 10, adjust accordingly)
    subset = random.sample(market_indices, min(num_indices, len(market_indices)))
    
    # Assign random weights (random integers between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(len(subset))]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "INDEX:XX.XX%"
    assets_str_parts = [f"{index}:{weight:.2f}%" for index, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For market indices, we use moderate ranges
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.005, 0.015), 3)  # e.g., 0.5% - 1.5%
        average_return = round(random.uniform(0.002, 0.005), 3)          # e.g., 0.2% - 0.5%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.015, 0.03), 3)   # e.g., 1.5% - 3%
        average_return = round(random.uniform(0.005, 0.01), 3)          # e.g., 0.5% - 1%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.03, 0.05), 3)    # e.g., 3% - 5%
        average_return = round(random.uniform(0.01, 0.02), 3)           # e.g., 1% - 2%
    
    # Portfolio name
    portfolio_name = f"Market_Indices_Portfolio_{i}"
    
    # Append the portfolio row to our list
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "market_indices_portfolios.csv"
with open("market_indices_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'market_indices_portfolios.csv' has been created successfully.")
