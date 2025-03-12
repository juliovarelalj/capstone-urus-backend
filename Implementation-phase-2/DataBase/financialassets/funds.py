import csv
import numpy as np
from datetime import datetime, timedelta

# Configuración del periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29
dates = [start_date + timedelta(days=i) for i in range(days)]

# Lista de 30 fondos de inversión reales (tickers reconocidos)
funds = [
    ("VFIAX", np.random.uniform(50, 150)),  # Vanguard 500 Index Fund
    ("FCNTX", np.random.uniform(50, 150)),  # Fidelity Contrafund
    ("VTSAX", np.random.uniform(50, 150)),  # Vanguard Total Stock Market Index Fund
    ("AGTHX", np.random.uniform(50, 150)),  # American Funds Growth Fund of America
    ("VWELX", np.random.uniform(50, 150)),  # Vanguard Wellington Fund
    ("TRBCX", np.random.uniform(50, 150)),  # T. Rowe Price Blue Chip Growth Fund
    ("FXAIX", np.random.uniform(50, 150)),  # Fidelity 500 Index Fund
    ("VINIX", np.random.uniform(50, 150)),  # Vanguard Institutional Index Fund
    ("DODGX", np.random.uniform(50, 150)),  # Dodge & Cox Stock Fund
    ("VBTLX", np.random.uniform(50, 150)),  # Vanguard Total Bond Market Index Fund
    ("FPURX", np.random.uniform(50, 150)),  # Fidelity Puritan Fund
    ("AEPGX", np.random.uniform(50, 150)),  # American Funds EuroPacific Growth
    ("VEXAX", np.random.uniform(50, 150)),  # Vanguard Extended Market Index Fund
    ("FLPSX", np.random.uniform(50, 150)),  # Fidelity Low-Priced Stock Fund
    ("PRFDX", np.random.uniform(50, 150)),  # T. Rowe Price Equity Income Fund
    ("VIGAX", np.random.uniform(50, 150)),  # Vanguard Growth Index Fund
    ("VIVAX", np.random.uniform(50, 150)),  # Vanguard Value Index Fund
    ("VTIAX", np.random.uniform(50, 150)),  # Vanguard International Index Fund
    ("FSPSX", np.random.uniform(50, 150)),  # Fidelity International Index Fund
    ("AIVSX", np.random.uniform(50, 150)),  # American Funds Investment Company of America
    ("VIMSX", np.random.uniform(50, 150)),  # Vanguard Mid-Cap Index Fund
    ("FSCKX", np.random.uniform(50, 150)),  # Fidelity Mid Cap Index Fund
    ("VSMAX", np.random.uniform(50, 150)),  # Vanguard Small-Cap Index Fund
    ("FSSNX", np.random.uniform(50, 150)),  # Fidelity Small Cap Index Fund
    ("PRSVX", np.random.uniform(50, 150)),  # T. Rowe Price Small-Cap Value Fund
    ("VEMAX", np.random.uniform(50, 150)),  # Vanguard Emerging Markets Stock Index Fund
    ("FEMKX", np.random.uniform(50, 150)),  # Fidelity Emerging Markets Fund
    ("ANWPX", np.random.uniform(50, 150)),  # American Funds New Perspective
    ("VGSLX", np.random.uniform(50, 150)),  # Vanguard REIT Index Fund
    ("FRESX", np.random.uniform(50, 150))   # Fidelity Real Estate Investment Portfolio
]

# Lista para almacenar las filas que se escribirán en el CSV
rows = []
rows.append(["date", "identifier", "open", "high", "low", "close", "volume"])

# Parámetros de simulación para fondos: drift y volatilidad moderados
for fund in funds:
    identifier, base_price = fund
    prev_close = base_price
    # Drift diario y volatilidad para fondos (valores moderados)
    drift = np.random.uniform(0.001, 0.005)
    volatility = np.random.uniform(0.005, 0.02)
    
    for d, current_date in enumerate(dates):
        date_str = current_date.strftime("%Y-%m-%d")
        # El precio de apertura es el cierre del día anterior; para el primer día usamos el precio base
        open_price = prev_close
        # Simular el rendimiento diario mediante un modelo similar a GBM
        r = np.random.normal(drift, volatility)
        close_price = round(prev_close * (1 + r), 2)
        # Generar high y low con ligeras variaciones (aproximadamente ±0.5%)
        high_price = round(max(open_price, close_price) * 1.005, 2)
        low_price = round(min(open_price, close_price) * 0.995, 2)
        # Simular un volumen razonable para fondos (considerando liquidez de ETFs o trading de fondos)
        volume = np.random.randint(500000, 5000000)
        
        rows.append([date_str, identifier, f"{open_price:.2f}", f"{high_price:.2f}", f"{low_price:.2f}", f"{close_price:.2f}", volume])
        prev_close = close_price

# Escribir el dataset en un archivo CSV
with open("funds_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset de fondos generado en 'funds_dataset.csv'")
