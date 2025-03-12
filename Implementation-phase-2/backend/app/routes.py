# app/routes.py
from flask import Blueprint, render_template, abort, redirect, url_for
from app.models import (
    get_asset_classes,
    get_assets_by_class,
    get_asset_detail,
    ASSET_CLASS_TABLES
)

routes_bp = Blueprint("routes_bp", __name__)

# @routes_bp.route("/")
# def home():
#     """
#     Redirige a /asset-classes para evitar un 404 en la raíz.
#     """
#     return redirect(url_for("routes_bp.asset_classes"))

@routes_bp.route("/asset-classes")
def asset_classes():
    """
    Muestra la lista de clases de activos.
    """
    classes = get_asset_classes()
    return render_template("asset_classes.html", classes=classes)

@routes_bp.route("/asset-classes/<asset_class>")
def asset_list(asset_class):
    """
    Muestra la lista de activos (únicos) pertenecientes a la clase seleccionada.
    """
    assets = get_assets_by_class(asset_class)
    
    # Obtenemos la información de la clase para pasar la columna identificadora a la plantilla (opcional)
    class_info = ASSET_CLASS_TABLES.get(asset_class)
    id_column = class_info["id_column"] if class_info else ""

    if not assets:
        # Si no hay resultados o la clase no existe
        return render_template("asset_list.html", asset_class=asset_class, assets=[], error=True, id_column=id_column)

    return render_template("asset_list.html", asset_class=asset_class, assets=assets, id_column=id_column)

# @routes_bp.route("/assets/<asset_class>/<asset_id>")
# def asset_detail(asset_class, asset_id):
#     """
#     Muestra todas las filas (histórico) de un activo específico.
#     """
#     rows = get_asset_detail(asset_class, asset_id)
#     if not rows:
#         abort(404, description="Activo no encontrado o sin registros.")

#     # Obtenemos la info de la clase para saber la columna de ID
#     class_info = ASSET_CLASS_TABLES.get(asset_class)
#     id_column = class_info["id_column"] if class_info else ""

#     return render_template(
#         "asset_detail.html",
#         asset_class=asset_class,
#         asset_id=asset_id,
#         rows=rows,
#         id_column=id_column
#     )

# app/routes.py (extracto)

@routes_bp.route("/assets/<asset_class>/<asset_id>")
def asset_detail(asset_class, asset_id):
    rows = get_asset_detail(asset_class, asset_id)
    if not rows:
        abort(404, description="Activo no encontrado o sin registros.")

    class_info = ASSET_CLASS_TABLES.get(asset_class)
    id_column = class_info["id_column"] if class_info else ""

    # Construimos listas de fechas y precios (o el campo que quieras graficar)
    # Asumiendo que la columna se llama 'date' y 'close'
    dates = [str(row.date) for row in rows]   # convertimos la fecha a string para JSON
    closes = [float(row.close) for row in rows]

    return render_template(
        "asset_detail.html",
        asset_class=asset_class,
        asset_id=asset_id,
        rows=rows,
        id_column=id_column,
        dates=dates,
        closes=closes
    )
