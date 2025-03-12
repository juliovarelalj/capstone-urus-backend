import csv
import numpy as np
from datetime import datetime, timedelta

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 15 criptomonedas relevantes con un precio base aproximado
cryptos = [
    ("BTC", 20000),   # Bitcoin
    ("ETH", 1500),    # Ethereum
    ("BNB", 300),     # Binance Coin
    ("ADA", 0.45),    # Cardano
    ("SOL", 20),      # Solana
    ("XRP", 0.50),    # Ripple
    ("DOT", 5),       # Polkadot
    ("DOGE", 0.07),   # Dogecoin
    ("AVAX", 15),     # Avalanche
    ("LINK", 7),      # Chainlink
    ("LTC", 100),     # Litecoin
    ("UNI", 5),       # Uniswap
    ("XLM", 0.10),    # Stellar
    ("MATIC", 1),     # Polygon
    ("ATOM", 10)      # Cosmos
]

# Lista para almacenar las filas (incluyendo la cabecera)
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Simulación de precios diarios para cada criptomoneda
for crypto in cryptos:
    identifier, base_price = crypto
    prev_close = base_price
    # Parámetros de simulación: las criptos presentan mayor volatilidad
    drift = np.random.uniform(0.01, 0.05)         # drift diario
    volatility = np.random.uniform(0.05, 0.2)       # volatilidad diaria
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        open_price = prev_close  # El open es igual al cierre del día anterior (o el precio base en el primer día)
        # Simular el rendimiento diario usando una distribución normal
        r = np.random.normal(drift, volatility)
        close_price = round(prev_close * (1 + r), 2)
        # Para cryptos, se usan márgenes un poco más amplios para high y low (aprox. ±1%)
        high_price = round(max(open_price, close_price) * 1.01, 2)
        low_price = round(min(open_price, close_price) * 0.99, 2)
        # Simular un volumen de trading, que en cripto suele ser elevado (valor aleatorio entre 1,000 y 1,000,000)
        volume = np.random.randint(1000, 1000000)
        
        rows.append([date_str, identifier, f"{open_price:.2f}", f"{high_price:.2f}", f"{low_price:.2f}", f"{close_price:.2f}", volume])
        prev_close = close_price

# Escribir el dataset en un archivo CSV
with open("cryptos_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de criptomonedas generado en 'cryptos_dataset.csv'")
