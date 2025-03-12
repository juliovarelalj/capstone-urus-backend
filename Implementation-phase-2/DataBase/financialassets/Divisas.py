import csv
import numpy as np
from datetime import datetime, timedelta

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 10 divisas relevantes (códigos ISO o tickers comunes)
divisas = [
    ("USD", 1.00),    # Dólar estadounidense (base)
    ("EUR", 0.90),    # Euro
    ("JPY", 110.00),  # Yen japonés
    ("GBP", 0.78),    # Libra esterlina
    ("AUD", 1.40),    # Dólar australiano
    ("CAD", 1.30),    # Dólar canadiense
    ("CHF", 0.95),    # Franco suizo
    ("CNY", 6.80),    # Yuan chino
    ("HKD", 7.80),    # Dólar de Hong Kong
    ("NZD", 1.50)     # Dólar neozelandés
]

# Cabecera del CSV
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Simulación de precios diarios para cada divisa
for divisa in divisas:
    identifier, base_rate = divisa
    prev_close = base_rate
    # Parámetros de simulación: en Forex los movimientos suelen ser pequeños, con baja volatilidad diaria
    drift = np.random.uniform(-0.001, 0.001)
    volatility = np.random.uniform(0.001, 0.005)
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        open_rate = prev_close  # El open es igual al cierre del día anterior (o el valor base en el primer día)
        # Simulación del rendimiento diario
        r = np.random.normal(drift, volatility)
        close_rate = round(prev_close * (1 + r), 4)
        # Generar high y low con ligeras variaciones (aprox. ±0.1%)
        high_rate = round(max(open_rate, close_rate) * 1.001, 4)
        low_rate = round(min(open_rate, close_rate) * 0.999, 4)
        # Simular un volumen de trading para divisas (por ejemplo, en millones de unidades)
        volume = np.random.randint(1000000, 10000000)
        
        rows.append([date_str, identifier, f"{open_rate:.4f}", f"{high_rate:.4f}", f"{low_rate:.4f}", f"{close_rate:.4f}", volume])
        prev_close = close_rate

# Escribir el dataset en un archivo CSV
with open("divisas_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de divisas generado en 'divisas_dataset.csv'")
