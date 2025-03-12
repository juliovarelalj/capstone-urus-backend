import random
import csv

# List of 30 ETF tickers from your dataset (example tickers)
etf_tickers = [
    "SPY", "IVV", "VOO", "VTI", "QQQ", "EFA", "EEM", "IWM", "AGG", "LQD",
    "VWO", "GDX", "VNQ", "XLF", "XLE", "XLY", "XLI", "XLV", "XLB", "XLC",
    "IYR", "VHT", "VUG", "VTV", "IWF", "IWD", "IEMG", "SPYG", "IJH", "MTUM"
]

# Possible risk profiles and time horizons for ETFs
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 ETF portfolios
for i in range(1, 21):
    # Randomly select the number of ETFs to include (between 10 and 20)
    num_etfs = random.randint(10, 20)
    # Choose a random subset of ETFs from the list
    subset = random.sample(etf_tickers, num_etfs)
    
    # Assign random weights (random integers between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_etfs)]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "TICKER:XX.XX%"
    assets_str_parts = [f"{ticker}:{weight:.2f}%" for ticker, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For ETFs, we use moderate ranges
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.01, 0.03), 3)  # e.g., 1%-3%
        average_return = round(random.uniform(0.003, 0.01), 3)       # e.g., 0.3%-1%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.03, 0.06), 3)  # e.g., 3%-6%
        average_return = round(random.uniform(0.01, 0.02), 3)        # e.g., 1%-2%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.06, 0.10), 3)  # e.g., 6%-10%
        average_return = round(random.uniform(0.02, 0.04), 3)        # e.g., 2%-4%
    
    # Portfolio name
    portfolio_name = f"ETF_Portfolio_{i}"
    
    # Append the portfolio row to our list
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "etfs_portfolios.csv"
with open("etfs_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'etfs_portfolios.csv' has been created successfully.")
