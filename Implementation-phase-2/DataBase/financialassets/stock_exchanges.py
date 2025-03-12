import random
import csv

# List of 30 stock tickers from your dataset
tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "BRK.B", "NVDA", "JPM", "JNJ",
    "UNH", "V", "PG", "MA", "HD", "DIS", "BAC", "ADBE", "CMCSA", "NFLX",
    "INTC", "T", "VZ", "KO", "PFE", "MRK", "WMT", "CRM", "ORCL", "ABT"
]

# Possible risk profiles and time horizons
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 portfolios
for i in range(1, 21):
    # Randomly select the number of tickers to include (between 10 and 20)
    num_stocks = random.randint(10, 20)
    # Choose a random subset of tickers
    subset = random.sample(tickers, num_stocks)
    
    # Assign random weights (between 1 and 10) and scale them to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_stocks)]
    total = sum(raw_weights)
    scaled_weights = [(w / total) * 100 for w in raw_weights]
    
    # Build the assets string in the format "TICKER:XX.XX%"
    assets_str_parts = [f"{ticker}:{weight:.2f}%" for ticker, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.01, 0.02), 3)  # e.g., 1%-2%
        average_return = round(random.uniform(0.003, 0.008), 3)      # e.g., 0.3%-0.8%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.02, 0.04), 3)  # e.g., 2%-4%
        average_return = round(random.uniform(0.008, 0.015), 3)      # e.g., 0.8%-1.5%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.04, 0.07), 3)  # e.g., 4%-7%
        average_return = round(random.uniform(0.015, 0.03), 3)       # e.g., 1.5%-3%
    
    # Portfolio name
    portfolio_name = f"Portfolio_{i}"
    
    # Append the row to the CSV rows list
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "portfolios.csv"
with open("portfoliostock.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'portfoliostock.csv' has been created successfully.")
