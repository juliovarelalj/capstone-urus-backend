import random
import csv

# List of 30 bond identifiers from your dataset
bonds = [
    "US 10Y Treasury", "US 2Y Treasury", "US 30Y Treasury", "UK 10Y Gilt", "UK 5Y Gilt",
    "Germany 10Y Bund", "Germany 5Y Bund", "France 10Y OAT", "France 5Y OAT", "Italy 10Y BTP",
    "Italy 5Y BTP", "Spain 10Y Bono", "Spain 5Y Bono", "Canada 10Y Government Bond", "Canada 5Y Government Bond",
    "Australia 10Y Bond", "Australia 5Y Bond", "Japan 10Y Government Bond", "Japan 5Y Government Bond",
    "Switzerland 10Y Bond", "Switzerland 5Y Bond", "Netherlands 10Y Bond", "Netherlands 5Y Bond", 
    "Sweden 10Y Bond", "Sweden 5Y Bond", "Norway 10Y Bond", "Norway 5Y Bond", "Denmark 10Y Bond", 
    "Denmark 5Y Bond", "Brazil 10Y Bond", "Brazil 5Y Bond"
]

# Possible risk profiles and time horizons
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 bond portfolios
for i in range(1, 21):
    # Randomly select number of bonds to include (between 10 and 20)
    num_bonds = random.randint(10, 20)
    # Choose a random subset of bonds from the list
    subset = random.sample(bonds, num_bonds)
    
    # Assign random weights (between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_bonds)]
    total = sum(raw_weights)
    scaled_weights = [(w / total) * 100 for w in raw_weights]
    
    # Build the assets string in the format "BOND_NAME:XX.XX%"
    assets_str_parts = [f"{bond}:{weight:.2f}%" for bond, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # For bonds, volatility is generally lower
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.005, 0.015), 3)  # e.g., 0.5% - 1.5%
        average_return = round(random.uniform(0.002, 0.005), 3)         # e.g., 0.2% - 0.5%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.015, 0.03), 3)    # e.g., 1.5% - 3%
        average_return = round(random.uniform(0.005, 0.01), 3)          # e.g., 0.5% - 1%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.03, 0.05), 3)     # e.g., 3% - 5%
        average_return = round(random.uniform(0.01, 0.02), 3)           # e.g., 1% - 2%
    
    # Portfolio name
    portfolio_name = f"Bond_Portfolio_{i}"
    
    # Append the portfolio row
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "bonds_portfolios.csv"
with open("bonds_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'bonds_portfolios.csv' has been created successfully.")
