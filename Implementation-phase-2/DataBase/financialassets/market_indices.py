import csv
import numpy as np
from datetime import datetime, timedelta

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 10 market indices relevantes con valores base aproximados (simulando el nivel del índice)
indices = [
    ("SPX", 4500),     # S&P 500 (EE.UU.)
    ("DJI", 36000),    # Dow Jones Industrial Average (EE.UU.)
    ("NDX", 15000),    # NASDAQ 100 (EE.UU.)
    ("FTSE", 7000),    # FTSE 100 (Reino Unido)
    ("DAX", 15000),    # DAX (Alemania)
    ("CAC", 6800),     # CAC 40 (Francia)
    ("NIK", 29000),    # Nikkei 225 (Japón)
    ("HSI", 25000),    # Hang Seng Index (Hong Kong)
    ("SSE", 3500),     # Shanghai Composite (China)
    ("BOVESPA", 120000) # Bovespa (Brasil)
]

# Cabecera del CSV
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Simulación de precios diarios para cada índice
for index in indices:
    identifier, base_value = index
    prev_close = base_value
    # Parámetros de simulación: drift y volatilidad moderados, adecuados para índices de mercado
    drift = np.random.uniform(0.001, 0.005)
    volatility = np.random.uniform(0.005, 0.02)
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        open_value = prev_close  # El open es igual al cierre del día anterior (o el valor base en el primer día)
        # Simular el rendimiento diario mediante un modelo similar al movimiento browniano geométrico
        r = np.random.normal(drift, volatility)
        close_value = round(prev_close * (1 + r), 2)
        # Generar high y low con ligeras variaciones (aproximadamente ±0.2%)
        high_value = round(max(open_value, close_value) * 1.002, 2)
        low_value = round(min(open_value, close_value) * 0.998, 2)
        # Simular un volumen elevado, propio del trading de índices (por ejemplo, entre 1M y 10M)
        volume = np.random.randint(1000000, 10000000)
        
        rows.append([date_str, identifier, f"{open_value:.2f}", f"{high_value:.2f}", f"{low_value:.2f}", f"{close_value:.2f}", volume])
        prev_close = close_value

# Escribir el dataset en un archivo CSV
with open("market_indices_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de market indices generado en 'market_indices_dataset.csv'")
