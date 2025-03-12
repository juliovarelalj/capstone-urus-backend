import csv
from datetime import datetime, timedelta
import numpy as np

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 30 bonos con nombres reales (representativos de diferentes mercados)
bond_names = [
    "US 10Y Treasury",
    "US 2Y Treasury",
    "US 30Y Treasury",
    "UK 10Y Gilt",
    "UK 5Y Gilt",
    "Germany 10Y Bund",
    "Germany 5Y Bund",
    "France 10Y OAT",
    "France 5Y OAT",
    "Italy 10Y BTP",
    "Italy 5Y BTP",
    "Spain 10Y Bono",
    "Spain 5Y Bono",
    "Canada 10Y Government Bond",
    "Canada 5Y Government Bond",
    "Australia 10Y Bond",
    "Australia 5Y Bond",
    "Japan 10Y Government Bond",
    "Japan 5Y Government Bond",
    "Switzerland 10Y Bond",
    "Switzerland 5Y Bond",
    "Netherlands 10Y Bond",
    "Netherlands 5Y Bond",
    "Sweden 10Y Bond",
    "Sweden 5Y Bond",
    "Norway 10Y Bond",
    "Norway 5Y Bond",
    "Denmark 10Y Bond",
    "Denmark 5Y Bond",
    "Brazil 10Y Bond",
    "Brazil 5Y Bond"
]

# Lista para almacenar los registros que se escribirán en el CSV
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Parámetros de simulación propios para bonos: precios cercanos a la par (95-105) y baja volatilidad
for bond in bond_names:
    base_price = np.random.uniform(95, 105)
    prev_close = base_price
    # Drift y volatilidad diarios reducidos para bonos
    drift = np.random.uniform(0, 0.002)
    volatility = np.random.uniform(0.001, 0.01)
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        # El precio de apertura es el cierre del día anterior; para el primer día usamos el precio base
        open_price = prev_close
        # Simulación del rendimiento diario
        r = np.random.normal(drift, volatility)
        close_price = round(prev_close * (1 + r), 2)
        # Generar high y low a partir de pequeñas variaciones (ejemplo: ±0.2%)
        high_price = round(max(open_price, close_price) * 1.002, 2)
        low_price = round(min(open_price, close_price) * 0.998, 2)
        # Simular un volumen razonable para bonos (en este ejemplo se asume menor liquidez)
        volume = np.random.randint(1000, 5000)
        
        rows.append([date_str, bond, f"{open_price:.2f}", f"{high_price:.2f}", f"{low_price:.2f}", f"{close_price:.2f}", volume])
        prev_close = close_price

# Escribir el dataset en un archivo CSV
with open("bonds_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de bonos generado en 'bonds_dataset.csv'")
