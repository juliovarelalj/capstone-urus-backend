# app/portfolios.py

from flask import Blueprint, render_template, abort
from app.auth import login_required
from app.models import get_bigquery_client, get_dataset_id

portfolios_bp = Blueprint("portfolios_bp", __name__, url_prefix="/portfolios")

# Diccionario que mapea cada categoría de portfolio a su tabla de BigQuery
# y la columna que identifica el portfolio (portfolio_name en este caso)
PORTFOLIO_CLASS_TABLES = {
    "bonds": {
        "table_name": "bonds_portolio",
        "id_column": "portfolio_name"
    },
    "cryptos": {
        "table_name": "cryptoportfolios",
        "id_column": "portfolio_name"
    },
    "currencies": {
        "table_name": "currenciesportfolios",
        "id_column": "portfolio_name"
    },
    "exchanges": {
        "table_name": "exchangesportolios",
        "id_column": "portfolio_name"
    },
    "funds": {
        "table_name": "fundsportolios",
        "id_column": "portfolio_name"
    },
    "market_indices": {
        "table_name": "marketindicesportfolio",
        "id_column": "portfolio_name"
    },
    "stocks": {
        "table_name": "portfoliostock",
        "id_column": "portfolio_name"
    },
    "etf": {
    "table_name": "etfportfolio",
    "id_column": "portfolio_name"
}
}

@portfolios_bp.route("")
@login_required
def portfolio_classes():
    """
    Muestra la lista de categorías de portfolios precreados.
    (bonds, stocks, cryptos, etc.)
    """
    portfolio_classes = list(PORTFOLIO_CLASS_TABLES.keys())
    return render_template("portfolio_classes.html", portfolio_classes=portfolio_classes)

@portfolios_bp.route("/<portfolio_class>")
@login_required
def portfolio_list(portfolio_class):
    """
    Lista todos los portfolios precreados de la categoría especificada.
    Por ejemplo, /portfolios/bonds -> muestra los portfolios de 'bonds_portfolio'.
    """
    class_info = PORTFOLIO_CLASS_TABLES.get(portfolio_class)
    if not class_info:
        # Si la categoría no está en el diccionario, devolvemos error o lista vacía
        return render_template("portfolio_list.html", portfolio_class=portfolio_class, portfolios=[], error=True)

    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    # Hacemos un SELECT DISTINCT para listar únicamente el nombre de cada portfolio
    query = f"""
        SELECT DISTINCT {class_info['id_column']} AS portfolio_id
        FROM `{client.project}.{dataset_id}.{class_info['table_name']}`
        ORDER BY {class_info['id_column']}
    """
    rows = list(client.query(query).result())

    if not rows:
        return render_template("portfolio_list.html", portfolio_class=portfolio_class, portfolios=[], error=True)

    return render_template("portfolio_list.html", portfolio_class=portfolio_class, portfolios=rows)

@portfolios_bp.route("/<portfolio_class>/<portfolio_id>")
@login_required
def portfolio_detail(portfolio_class, portfolio_id):
    """
    Muestra el detalle de un portfolio específico.
    Por ejemplo, /portfolios/bonds/BondPortfolio1 -> consulta 'bonds_portfolio'
    donde portfolio_name = 'BondPortfolio1'.
    """
    class_info = PORTFOLIO_CLASS_TABLES.get(portfolio_class)
    if not class_info:
        abort(404, description="Portfolio class no existe.")

    client = get_bigquery_client()
    dataset_id = get_dataset_id()

    # Seleccionamos todas las columnas del portfolio donde portfolio_name = portfolio_id
    query = f"""
        SELECT *
        FROM `{client.project}.{dataset_id}.{class_info['table_name']}`
        WHERE {class_info['id_column']} = '{portfolio_id}'
    """
    rows = list(client.query(query).result())

    if not rows:
        abort(404, description="Portfolio no encontrado o sin registros.")

    return render_template("portfolio_detail.html",
                           portfolio_class=portfolio_class,
                           portfolio_id=portfolio_id,
                           rows=rows)
