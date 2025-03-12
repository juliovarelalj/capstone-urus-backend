import csv
import numpy as np
from datetime import datetime, timedelta

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 30 ETFs relevantes con precios base aproximados (valores en USD)
etfs = [
    ("SPY", np.random.uniform(300, 400)),    # SPDR S&P 500 ETF Trust
    ("IVV", np.random.uniform(300, 400)),    # iShares Core S&P 500 ETF
    ("VOO", np.random.uniform(300, 400)),    # Vanguard S&P 500 ETF
    ("VTI", np.random.uniform(150, 250)),    # Vanguard Total Stock Market ETF
    ("QQQ", np.random.uniform(250, 350)),    # Invesco QQQ ETF
    ("EFA", np.random.uniform(70, 90)),      # iShares MSCI EAFE ETF
    ("EEM", np.random.uniform(50, 70)),      # iShares MSCI Emerging Markets ETF
    ("IWM", np.random.uniform(150, 250)),    # iShares Russell 2000 ETF
    ("AGG", np.random.uniform(100, 120)),    # iShares Core U.S. Aggregate Bond ETF
    ("LQD", np.random.uniform(100, 110)),    # iShares iBoxx $ Investment Grade Corporate Bond ETF
    ("VWO", np.random.uniform(40, 60)),      # Vanguard FTSE Emerging Markets ETF
    ("GDX", np.random.uniform(20, 30)),      # VanEck Vectors Gold Miners ETF
    ("VNQ", np.random.uniform(80, 100)),     # Vanguard Real Estate ETF
    ("XLF", np.random.uniform(30, 40)),      # Financial Select Sector SPDR Fund
    ("XLE", np.random.uniform(40, 50)),      # Energy Select Sector SPDR Fund
    ("XLY", np.random.uniform(150, 200)),    # Consumer Discretionary Select Sector SPDR Fund
    ("XLI", np.random.uniform(80, 100)),     # Industrial Select Sector SPDR Fund
    ("XLV", np.random.uniform(100, 120)),    # Health Care Select Sector SPDR Fund
    ("XLB", np.random.uniform(70, 90)),      # Materials Select Sector SPDR Fund
    ("XLC", np.random.uniform(50, 70)),      # Communication Services Select Sector SPDR Fund
    ("IYR", np.random.uniform(80, 100)),     # iShares U.S. Real Estate ETF
    ("VHT", np.random.uniform(150, 200)),    # Vanguard Health Care ETF
    ("VUG", np.random.uniform(200, 300)),    # Vanguard Growth ETF
    ("VTV", np.random.uniform(100, 150)),    # Vanguard Value ETF
    ("IWF", np.random.uniform(200, 300)),    # iShares Russell 1000 Growth ETF
    ("IWD", np.random.uniform(80, 120)),     # iShares Russell 1000 Value ETF
    ("IEMG", np.random.uniform(40, 60)),     # iShares Core MSCI Emerging Markets ETF
    ("SPYG", np.random.uniform(100, 150)),    # SPDR Portfolio S&P 500 Growth ETF
    ("IJH", np.random.uniform(150, 250)),    # iShares Core S&P Mid-Cap ETF
    ("MTUM", np.random.uniform(100, 150))     # iShares Edge MSCI USA Momentum Factor ETF
]

# Cabecera del CSV
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Simulación de precios diarios para cada ETF
for etf in etfs:
    identifier, base_price = etf
    prev_close = base_price
    # Parámetros de simulación para ETFs: drift moderado y volatilidad moderada
    drift = np.random.uniform(0.001, 0.005)
    volatility = np.random.uniform(0.01, 0.03)
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        open_price = prev_close  # El open es igual al cierre del día anterior (o el precio base en el primer día)
        # Simular el rendimiento diario mediante un modelo similar al GBM
        r = np.random.normal(drift, volatility)
        close_price = round(prev_close * (1 + r), 2)
        # Generar high y low con ligeras variaciones (aproximadamente ±0.2%)
        high_price = round(max(open_price, close_price) * 1.002, 2)
        low_price = round(min(open_price, close_price) * 0.998, 2)
        # Simular un volumen razonable para ETFs
        volume = np.random.randint(500000, 5000000)
        
        rows.append([date_str, identifier, f"{open_price:.2f}", f"{high_price:.2f}", f"{low_price:.2f}", f"{close_price:.2f}", volume])
        prev_close = close_price

# Escribir el dataset en un archivo CSV
with open("etfs_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de ETFs generado en 'etfs_dataset.csv'")
