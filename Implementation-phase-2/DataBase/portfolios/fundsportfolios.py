import random
import csv

# List of investment fund identifiers from your dataset
# (Assuming these are the funds chosen from your funds_dataset.csv)
investment_funds = [
    "VFIAX", "FCNTX", "VTSAX", "AGTHX", "VWELX", "TRBCX", "FXAIX", "VINIX", "DODGX", "VBTLX",
    "FPURX", "AEPGX", "VEXAX", "FLPSX", "PRFDX", "VIGAX", "VIVAX", "VTIAX", "FSPSX", "AIVSX",
    "VIMSX", "FSCKX", "VSMAX", "FSSNX", "PRSVX", "VEMAX", "FEMKX", "ANWPX", "VGSLX", "FRESX"
]

# Possible risk profiles and time horizons for investment funds
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 investment fund portfolios
for i in range(1, 21):
    # Randomly select the number of funds to include (between 10 and 20)
    num_funds = random.randint(10, 20)
    # Choose a random subset of funds from the list
    subset = random.sample(investment_funds, num_funds)
    
    # Assign random weights (random integers between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_funds)]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "FUND:XX.XX%"
    assets_str_parts = [f"{fund}:{weight:.2f}%" for fund, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For investment funds, we use moderate ranges:
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.005, 0.015), 3)  # e.g., 0.5% - 1.5%
        average_return = round(random.uniform(0.002, 0.005), 3)          # e.g., 0.2% - 0.5%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.015, 0.03), 3)   # e.g., 1.5% - 3%
        average_return = round(random.uniform(0.005, 0.01), 3)         # e.g., 0.5% - 1%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.03, 0.05), 3)    # e.g., 3% - 5%
        average_return = round(random.uniform(0.01, 0.02), 3)          # e.g., 1% - 2%
    
    # Portfolio name
    portfolio_name = f"Funds_Portfolio_{i}"
    
    # Append the portfolio row to our list
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "funds_portfolios.csv"
with open("funds_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'funds_portfolios.csv' has been created successfully.")
