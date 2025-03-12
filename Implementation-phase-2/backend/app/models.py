# app/models.py
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Diccionario que mapea la "clase de activo" a la tabla y la columna que identifica cada activo
ASSET_CLASS_TABLES = {
    "stocks": {
        "table_name": "stocks",
        "id_column": "ticker"
    },
    "bonds": {
        "table_name": "bonds",
        "id_column": "identifier"
    },
    "cryptos": {
        "table_name": "crypto",
        "id_column": "identifier"
    },
    "funds": {
        "table_name": "funds",
        "id_column": "identifier"
    },
    "etf": {
        "table_name": "etf",
        "id_column": "identifier"
    },
    "exchanges": {
        "table_name": "exchanges",
        "id_column": "identifier"
    },
    "market_indices": {
        "table_name": "market_indices",
        "id_column": "identifier"
    }
}


def get_bigquery_client():
    """
    Crea y retorna un cliente de BigQuery usando credenciales y ID de proyecto del .env
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("GCP_PROJECT_ID")

    if not credentials_path or not project_id:
        raise ValueError("Faltan variables de entorno (credenciales o project ID).")

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=project_id)
    return client

def get_dataset_id():
    """
    Retorna el ID del dataset definido en .env
    """
    dataset_id = os.getenv("GCP_DATASET_ID")
    if not dataset_id:
        raise ValueError("Falta la variable 'GCP_DATASET_ID' en .env.")
    return dataset_id

def get_asset_classes():
    """
    Devuelve la lista de clases de activos (claves del diccionario).
    """
    return list(ASSET_CLASS_TABLES.keys())

def get_assets_by_class(asset_class):
    """
    Devuelve un listado de activos únicos para la clase dada.
    Usamos DISTINCT en la columna identificadora para no repetir activos.
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    class_info = ASSET_CLASS_TABLES.get(asset_class)
    if not class_info:
        return []

    table_name = class_info["table_name"]
    id_column = class_info["id_column"]

    # Usamos DISTINCT para que no se repita el mismo activo varias veces
    query = f"""
        SELECT DISTINCT {id_column} AS asset_id
        FROM `{client.project}.{dataset_id}.{table_name}`
        ORDER BY {id_column}
    """
    query_job = client.query(query)
    rows = list(query_job.result())  # Cada fila tendrá una sola columna: asset_id
    return rows

def get_asset_detail(asset_class, asset_id):
    """
    Devuelve TODAS las filas (histórico) de un activo específico, ordenadas por fecha.
    Ajusta 'date' si tu tabla usa otro nombre (por ejemplo, 'fecha' o 'datetime').
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    class_info = ASSET_CLASS_TABLES.get(asset_class)
    if not class_info:
        return []

    table_name = class_info["table_name"]
    id_column = class_info["id_column"]

    # Devolvemos todas las filas para ese activo, ordenadas por fecha
    query = f"""
        SELECT *
        FROM `{client.project}.{dataset_id}.{table_name}`
        WHERE {id_column} = '{asset_id}'
        ORDER BY date
    """
    query_job = client.query(query)
    rows = list(query_job.result())
    return rows




# app/models.py (al final del archivo)

# Supongamos que tienes un diccionario similar para los portfolios.
PORTFOLIO_CLASS_TABLES = {
    "bonds": {
        "table_name": "bonds_portolios",
        "id_column": "portfolio_id"  # Ajusta según la columna que uses para identificar el portfolio
    },
    "stocks": {
        "table_name": "portfoliostock",
        "id_column": "portfolio_id"
    },
    "cryptos": {
        "table_name": "cryptoportfolios",
        "id_column": "portfolio_id"
    },
    # Agrega más clases según tu estructura...
}

def get_portfolio_classes():
    """
    Devuelve la lista de clases de portfolios precreados.
    """
    return list(PORTFOLIO_CLASS_TABLES.keys())

def get_portfolios_by_class(portfolio_class):
    """
    Devuelve un listado de portfolios únicos para la categoría dada.
    Se usa DISTINCT en la columna identificadora.
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    class_info = PORTFOLIO_CLASS_TABLES.get(portfolio_class)
    if not class_info:
        return []

    table_name = class_info["table_name"]
    id_column = class_info["id_column"]

    query = f"""
        SELECT DISTINCT {id_column} AS portfolio_id
        FROM `{client.project}.{dataset_id}.{table_name}`
        ORDER BY {id_column}
    """
    query_job = client.query(query)
    rows = list(query_job.result())
    return rows

def get_portfolio_detail(portfolio_class, portfolio_id):
    """
    Devuelve todas las filas (histórico o detalle) de un portfolio específico, ordenadas (por ejemplo, por fecha o por otro criterio).
    """
    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    class_info = PORTFOLIO_CLASS_TABLES.get(portfolio_class)
    if not class_info:
        return []

    table_name = class_info["table_name"]
    id_column = class_info["id_column"]

    query = f"""
        SELECT *
        FROM `{client.project}.{dataset_id}.{table_name}`
        WHERE {id_column} = '{portfolio_id}'
        ORDER BY date  -- o el campo que convenga
    """
    query_job = client.query(query)
    rows = list(query_job.result())
    return rows
