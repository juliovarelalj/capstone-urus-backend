import random
import csv

# List of 15 cryptocurrencies based on your provided dataset
cryptos = [
    "BTC",  # Bitcoin
    "ETH",  # Ethereum
    "BNB",  # Binance Coin
    "ADA",  # Cardano
    "SOL",  # Solana
    "XRP",  # Ripple
    "DOT",  # Polkadot
    "DOGE", # Dogecoin
    "AVAX", # Avalanche
    "LINK", # Chainlink
    "LTC",  # Litecoin
    "UNI",  # Uniswap
    "XLM",  # Stellar
    "MATIC",# Polygon
    "ATOM"  # Cosmos
]

# Possible risk profiles and time horizons
risk_profiles = ["Low", "Medium", "High"]
time_horizons = ["Short Term", "Medium Term", "Long Term"]

# List to store CSV rows
rows = []
# CSV header
rows.append(["portfolio_name", "risk_profile", "time_horizon", "assets", "estimated_volatility", "average_return"])

# Generate 20 crypto portfolios
for i in range(1, 21):
    # Randomly select the number of cryptos to include (between 10 and 15)
    num_cryptos = random.randint(10, len(cryptos))
    # Choose a random subset of cryptocurrencies
    subset = random.sample(cryptos, num_cryptos)
    
    # Assign random weights (between 1 and 10) and scale them to sum to 100%
    raw_weights = [random.randint(1, 10) for _ in range(num_cryptos)]
    total_weight = sum(raw_weights)
    scaled_weights = [(w / total_weight) * 100 for w in raw_weights]
    
    # Build the assets string in the format "CRYPTO:XX.XX%"
    assets_str_parts = [f"{crypto}:{weight:.2f}%" for crypto, weight in zip(subset, scaled_weights)]
    assets_str = "; ".join(assets_str_parts)
    
    # Randomly choose a risk profile and time horizon
    risk = random.choice(risk_profiles)
    horizon = random.choice(time_horizons)
    
    # Generate simulated estimated volatility and average return based on risk profile
    # Cryptocurrencies generally have higher volatility and returns
    if risk == "Low":
        estimated_volatility = round(random.uniform(0.05, 0.10), 3)  # e.g., 5% - 10%
        average_return = round(random.uniform(0.02, 0.05), 3)        # e.g., 2% - 5%
    elif risk == "Medium":
        estimated_volatility = round(random.uniform(0.10, 0.20), 3)  # e.g., 10% - 20%
        average_return = round(random.uniform(0.05, 0.10), 3)        # e.g., 5% - 10%
    else:  # High risk
        estimated_volatility = round(random.uniform(0.20, 0.40), 3)  # e.g., 20% - 40%
        average_return = round(random.uniform(0.10, 0.20), 3)        # e.g., 10% - 20%
    
    # Portfolio name
    portfolio_name = f"Crypto_Portfolio_{i}"
    
    # Append the portfolio row
    rows.append([portfolio_name, risk, horizon, assets_str, estimated_volatility, average_return])

# Write the rows to a CSV file named "cryptos_portfolios.csv"
with open("cryptos_portfolios.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("The file 'cryptos_portfolios.csv' has been created successfully.")
