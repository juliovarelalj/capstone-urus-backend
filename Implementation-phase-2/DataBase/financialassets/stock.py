import csv
from datetime import datetime, timedelta

# Lista de 30 stocks relevantes con su precio base (valores aproximados)
tickers = [
    ("AAPL", 150.00),
    ("MSFT", 280.00),
    ("AMZN", 3300.00),
    ("GOOGL", 2700.00),
    ("FB", 350.00),
    ("TSLA", 800.00),
    ("BRK.B", 300.00),
    ("NVDA", 200.00),
    ("JPM", 160.00),
    ("JNJ", 170.00),
    ("UNH", 450.00),
    ("V", 230.00),
    ("PG", 150.00),
    ("MA", 350.00),
    ("HD", 330.00),
    ("DIS", 180.00),
    ("BAC", 40.00),
    ("ADBE", 600.00),
    ("CMCSA", 50.00),
    ("NFLX", 550.00),
    ("INTC", 55.00),
    ("T", 30.00),
    ("VZ", 60.00),
    ("KO", 55.00),
    ("PFE", 45.00),
    ("MRK", 80.00),
    ("WMT", 150.00),
    ("CRM", 250.00),
    ("ORCL", 90.00),
    ("ABT", 120.00)
]

# Periodo: desde el 21 de febrero de 2025 hasta el 21 de marzo de 2025 (29 días)
start_date = datetime(2025, 2, 21)
days = 29

# Secuencia de retornos diarios (r) para simular movimientos de precio (puedes ajustar estos valores)
r_seq = [0.01, -0.005, 0.007, 0.003, -0.002]  # Por ejemplo, +1%, -0.5%, +0.7%, +0.3%, -0.2%

# Lista para almacenar las filas del CSV (incluyendo la cabecera)
rows = []
rows.append(["date", "ticker", "open", "high", "low", "close", "volume"])

# Para cada ticker, se simulan los precios diarios
for ticker_index, (ticker, base_price) in enumerate(tickers, start=1):
    prev_close = base_price  # Precio de partida
    for d in range(days):
        current_date = start_date + timedelta(days=d)
        date_str = current_date.strftime("%Y-%m-%d")
        # El precio "open" es igual al cierre del día anterior; para el primer día se usa el precio base
        open_price = prev_close  
        # Seleccionar el rendimiento del día de forma cíclica
        r = r_seq[d % len(r_seq)]
        # Calcular el "close" aplicando el rendimiento
        close_price = round(prev_close * (1 + r), 2)
        # Generar "high" y "low" a partir de una pequeña variación de open y close
        high_price = round(max(open_price, close_price) * 1.005, 2)
        low_price = round(min(open_price, close_price) * 0.995, 2)
        # Generar un volumen "realista": usamos una fórmula determinista para este ejemplo
        volume = 1000000 + ((ticker_index * (d + 1) * 1000) % 9000000)
        # Agregar la fila
        rows.append([date_str, ticker, f"{open_price:.2f}", f"{high_price:.2f}", f"{low_price:.2f}", f"{close_price:.2f}", volume])
        # Actualizar el precio anterior para el siguiente día
        prev_close = close_price

# Escribir el dataset completo en un archivo CSV
with open("dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Dataset generado en 'dataset.csv'")
