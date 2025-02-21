import os
import uuid
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.cloud import bigquery

app = Flask(__name__)

PROJECT_ID = "capstoneurus-jv"
DATASET_NAME = "capstone"

client = bigquery.Client(project=PROJECT_ID)

# ------------------------------------------------------------
# Funciones de Validación
# ------------------------------------------------------------

def validate_email_format(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def validate_numeric(value, min_value=None, max_value=None):
    try:
        num = float(value)
        if min_value is not None and num < min_value:
            return False
        if max_value is not None and num > max_value:
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_date_format(date_str, format='%Y-%m-%d'):
    try:
        datetime.strptime(date_str, format)
        return True
    except (ValueError, TypeError):
        return False

def validate_string_length(s, max_length):
    if s is not None and len(s) <= max_length:
        return True
    return False

# ------------------------------------------------------------
# Funciones para Verificar Existencia (Foreign Keys)
# ------------------------------------------------------------

def check_user_exists(user_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
    query = f"SELECT COUNT(*) as total FROM `{table_id}` WHERE user_id = '{user_id}'"
    try:
        results = list(client.query(query).result())
        return results[0]["total"] > 0
    except Exception as e:
        app.logger.error(f"Error al verificar user: {e}")
        return False

def check_duplicate_email(email):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
    query = f"SELECT COUNT(*) as total FROM `{table_id}` WHERE email = '{email}'"
    try:
        results = list(client.query(query).result())
        return results[0]["total"] > 0
    except Exception as e:
        app.logger.error(f"Error al verificar email duplicado: {e}")
        return False

def check_asset_exists(asset_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.asset_data"
    query = f"SELECT COUNT(*) as total FROM `{table_id}` WHERE asset_id = '{asset_id}'"
    try:
        results = list(client.query(query).result())
        return results[0]["total"] > 0
    except Exception as e:
        app.logger.error(f"Error al verificar asset: {e}")
        return False

def check_portfolio_exists(portfolio_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_data"
    query = f"SELECT COUNT(*) as total FROM `{table_id}` WHERE portfolio_id = '{portfolio_id}'"
    try:
        results = list(client.query(query).result())
        return results[0]["total"] > 0
    except Exception as e:
        app.logger.error(f"Error al verificar portfolio: {e}")
        return False

# ------------------------------------------------------------
# Endpoints CRUD con Plantillas HTML
# ------------------------------------------------------------

@app.route('/')
def index():
    return "¡Bienvenido a la API de Urus Portfolio Management!"

# ------------------ USERS (User_Data) ------------------

@app.route('/users_html', methods=['GET'])
def list_users_html():
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
    query = f"""
        SELECT user_id, email, hashed_password, first_name, last_name, created_at
        FROM `{table_id}`
        LIMIT 50
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        users_list = []
        for row in results:
            users_list.append({
                "user_id": row["user_id"],
                "email": row["email"],
                "hashed_password": row["hashed_password"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "created_at": str(row["created_at"])
            })
        return render_template("users.html", users=users_list)
    except Exception as e:
        return f"Error al listar usuarios: {e}", 500

@app.route('/add_user_html', methods=['GET', 'POST'])
def add_user_html():
    if request.method == 'GET':
        return render_template("add_user.html")
    else:
        email = request.form.get('email')
        hashed_password = request.form.get('hashed_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validaciones
        if not email or not hashed_password or not first_name or not last_name:
            return "Faltan campos", 400
        if not validate_email_format(email):
            return "El formato del email no es válido", 400
        if not validate_string_length(first_name, 50) or not validate_string_length(last_name, 50):
            return "Los nombres no deben exceder 50 caracteres", 400
        if check_duplicate_email(email):
            return f"El email {email} ya existe", 400
        
        user_id = str(uuid.uuid4())
        table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
        rows_to_insert = [{
            "user_id": user_id,
            "email": email,
            "hashed_password": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "created_at": "2025-02-21T12:00:00Z"
        }]
        try:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
                return redirect(url_for('list_users_html'))
            else:
                return f"Error al insertar usuario: {errors}", 400
        except Exception as e:
            return f"Error: {e}", 500

@app.route('/update_user_html/<user_id>', methods=['GET', 'POST'])
def update_user_html(user_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
    if request.method == 'GET':
        query = f"""
            SELECT user_id, email, hashed_password, first_name, last_name, created_at
            FROM `{table_id}`
            WHERE user_id = '{user_id}'
        """
        try:
            query_job = client.query(query)
            results = list(query_job.result())
            if not results:
                return "Usuario no encontrado", 404
            user = dict(results[0])
            return render_template("update_user.html", user=user)
        except Exception as e:
            return f"Error al obtener usuario: {e}", 500
    else:
        email = request.form.get('email')
        hashed_password = request.form.get('hashed_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if not email or not hashed_password or not first_name or not last_name:
            return "Faltan campos", 400
        if not validate_email_format(email):
            return "El formato del email no es válido", 400
        if not validate_string_length(first_name, 50) or not validate_string_length(last_name, 50):
            return "Los nombres no deben exceder 50 caracteres", 400

        update_query = f"""
            UPDATE `{table_id}`
            SET email = '{email}',
                hashed_password = '{hashed_password}',
                first_name = '{first_name}',
                last_name = '{last_name}'
            WHERE user_id = '{user_id}'
        """
        try:
            client.query(update_query).result()
            return redirect(url_for('list_users_html'))
        except Exception as e:
            return f"Error al actualizar usuario: {e}", 500

@app.route('/delete_user_html/<user_id>', methods=['GET'])
def delete_user_html(user_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.User_Data"
    delete_query = f"DELETE FROM `{table_id}` WHERE user_id = '{user_id}'"
    try:
        client.query(delete_query).result()
        return redirect(url_for('list_users_html'))
    except Exception as e:
        return f"Error al borrar usuario: {e}", 500

# ------------------ ASSETS (asset_data) ------------------

@app.route('/assets_html', methods=['GET'])
def list_assets_html():
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.asset_data"
    query = f"""
        SELECT asset_id, ticker, name, asset_type, currency
        FROM `{table_id}`
        LIMIT 50
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        assets_list = []
        for row in results:
            assets_list.append({
                "asset_id": row["asset_id"],
                "ticker": row["ticker"],
                "name": row["name"],
                "asset_type": row["asset_type"],
                "currency": row["currency"]
            })
        return render_template("assets.html", assets=assets_list)
    except Exception as e:
        return f"Error al listar assets: {e}", 500

@app.route('/add_asset_html', methods=['GET', 'POST'])
def add_asset_html():
    if request.method == 'GET':
        return render_template("add_asset.html")
    else:
        ticker = request.form.get('ticker')
        name = request.form.get('name')
        asset_type = request.form.get('asset_type')
        currency = request.form.get('currency')

        if not ticker or not name or not asset_type or not currency:
            return "Faltan campos", 400

        asset_id = str(uuid.uuid4())
        table_id = f"{PROJECT_ID}.{DATASET_NAME}.asset_data"
        rows_to_insert = [{
            "asset_id": asset_id,
            "ticker": ticker,
            "name": name,
            "asset_type": asset_type,
            "currency": currency
        }]
        try:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
                return redirect(url_for('list_assets_html'))
            else:
                return f"Error al insertar asset: {errors}", 400
        except Exception as e:
            return f"Error: {e}", 500

@app.route('/update_asset_html/<asset_id>', methods=['GET', 'POST'])
def update_asset_html(asset_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.asset_data"
    if request.method == 'GET':
        query = f"""
            SELECT asset_id, ticker, name, asset_type, currency
            FROM `{table_id}`
            WHERE asset_id = '{asset_id}'
        """
        try:
            query_job = client.query(query)
            results = list(query_job.result())
            if not results:
                return "Asset no encontrado", 404
            asset = dict(results[0])
            return render_template("update_asset.html", asset=asset)
        except Exception as e:
            return f"Error al obtener asset: {e}", 500
    else:
        ticker = request.form.get('ticker')
        name = request.form.get('name')
        asset_type = request.form.get('asset_type')
        currency = request.form.get('currency')

        if not ticker or not name or not asset_type or not currency:
            return "Faltan campos", 400

        update_query = f"""
            UPDATE `{table_id}`
            SET ticker = '{ticker}',
                name = '{name}',
                asset_type = '{asset_type}',
                currency = '{currency}'
            WHERE asset_id = '{asset_id}'
        """
        try:
            client.query(update_query).result()
            return redirect(url_for('list_assets_html'))
        except Exception as e:
            return f"Error al actualizar asset: {e}", 500

@app.route('/delete_asset_html/<asset_id>', methods=['GET'])
def delete_asset_html(asset_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.asset_data"
    delete_query = f"DELETE FROM `{table_id}` WHERE asset_id = '{asset_id}'"
    try:
        client.query(delete_query).result()
        return redirect(url_for('list_assets_html'))
    except Exception as e:
        return f"Error al borrar asset: {e}", 500

# ------------------ PORTFOLIOS (portfolio_data) ------------------

@app.route('/portfolios_html', methods=['GET'])
def list_portfolios_html():
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_data"
    query = f"""
        SELECT portfolio_id, user_id, portfolio_name, created_at
        FROM `{table_id}`
        LIMIT 50
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        portfolios_list = []
        for row in results:
            portfolios_list.append({
                "portfolio_id": row["portfolio_id"],
                "user_id": row["user_id"],
                "portfolio_name": row["portfolio_name"],
                "created_at": str(row["created_at"])
            })
        return render_template("portfolios.html", portfolios=portfolios_list)
    except Exception as e:
        return f"Error al listar portfolios: {e}", 500

@app.route('/add_portfolio_html', methods=['GET', 'POST'])
def add_portfolio_html():
    if request.method == 'GET':
        return render_template("add_portfolio.html")
    else:
        user_id = request.form.get('user_id')
        portfolio_name = request.form.get('portfolio_name')

        if not user_id or not portfolio_name:
            return "Faltan campos", 400
        if not check_user_exists(user_id):
            return f"Error: El user_id {user_id} no existe.", 400

        portfolio_id = str(uuid.uuid4())
        table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_data"
        rows_to_insert = [{
            "portfolio_id": portfolio_id,
            "user_id": user_id,
            "portfolio_name": portfolio_name,
            "created_at": "2025-02-21T12:00:00Z"
        }]
        try:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
                return redirect(url_for('list_portfolios_html'))
            else:
                return f"Error al insertar portfolio: {errors}", 400
        except Exception as e:
            return f"Error: {e}", 500

@app.route('/update_portfolio_html/<portfolio_id>', methods=['GET', 'POST'])
def update_portfolio_html(portfolio_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_data"
    if request.method == 'GET':
        query = f"""
            SELECT portfolio_id, user_id, portfolio_name, created_at
            FROM `{table_id}`
            WHERE portfolio_id = '{portfolio_id}'
        """
        try:
            query_job = client.query(query)
            results = list(query_job.result())
            if not results:
                return "Portfolio no encontrado", 404
            portfolio = dict(results[0])
            return render_template("update_portfolio.html", portfolio=portfolio)
        except Exception as e:
            return f"Error al obtener portfolio: {e}", 500
    else:
        user_id = request.form.get('user_id')
        portfolio_name = request.form.get('portfolio_name')
        if not user_id or not portfolio_name:
            return "Faltan campos", 400
        if not check_user_exists(user_id):
            return f"Error: El user_id {user_id} no existe.", 400

        update_query = f"""
            UPDATE `{table_id}`
            SET user_id = '{user_id}',
                portfolio_name = '{portfolio_name}'
            WHERE portfolio_id = '{portfolio_id}'
        """
        try:
            client.query(update_query).result()
            return redirect(url_for('list_portfolios_html'))
        except Exception as e:
            return f"Error al actualizar portfolio: {e}", 500

@app.route('/delete_portfolio_html/<portfolio_id>', methods=['GET'])
def delete_portfolio_html(portfolio_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_data"
    delete_query = f"DELETE FROM `{table_id}` WHERE portfolio_id = '{portfolio_id}'"
    try:
        client.query(delete_query).result()
        return redirect(url_for('list_portfolios_html'))
    except Exception as e:
        return f"Error al borrar portfolio: {e}", 500

# ------------------ PORTFOLIO ASSET DATA (portfolio_asset_data) ------------------

@app.route('/portfolio_assets_html', methods=['GET'])
def list_portfolio_assets_html():
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_asset_data"
    query = f"""
        SELECT portfolio_asset_id, portfolio_id, asset_id, quantity, avg_cost, created_at
        FROM `{table_id}`
        LIMIT 50
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        pa_list = []
        for row in results:
            pa_list.append({
                "portfolio_asset_id": row["portfolio_asset_id"],
                "portfolio_id": row["portfolio_id"],
                "asset_id": row["asset_id"],
                "quantity": row["quantity"],
                "avg_cost": row["avg_cost"],
                "created_at": str(row["created_at"])
            })
        return render_template("portfolio_assets.html", portfolio_assets=pa_list)
    except Exception as e:
        return f"Error al listar portfolio_assets: {e}", 500

@app.route('/add_portfolio_asset_html', methods=['GET', 'POST'])
def add_portfolio_asset_html():
    if request.method == 'GET':
        return render_template("add_portfolio_asset.html")
    else:
        portfolio_id = request.form.get('portfolio_id')
        asset_id = request.form.get('asset_id')
        quantity = request.form.get('quantity')
        avg_cost = request.form.get('avg_cost')

        if not portfolio_id or not asset_id or not quantity or not avg_cost:
            return "Faltan campos", 400
        if not check_portfolio_exists(portfolio_id):
            return f"Error: El portfolio_id {portfolio_id} no existe.", 400
        if not check_asset_exists(asset_id):
            return f"Error: El asset_id {asset_id} no existe.", 400

        portfolio_asset_id = str(uuid.uuid4())
        table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_asset_data"
        rows_to_insert = [{
            "portfolio_asset_id": portfolio_asset_id,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": float(quantity),
            "avg_cost": float(avg_cost),
            "created_at": "2025-02-21T12:00:00Z"
        }]
        try:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
                return redirect(url_for('list_portfolio_assets_html'))
            else:
                return f"Error al insertar portfolio_asset: {errors}", 400
        except Exception as e:
            return f"Error: {e}", 500

@app.route('/update_portfolio_asset_html/<portfolio_asset_id>', methods=['GET', 'POST'])
def update_portfolio_asset_html(portfolio_asset_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_asset_data"
    if request.method == 'GET':
        query = f"""
            SELECT portfolio_asset_id, portfolio_id, asset_id, quantity, avg_cost, created_at
            FROM `{table_id}`
            WHERE portfolio_asset_id = '{portfolio_asset_id}'
        """
        try:
            query_job = client.query(query)
            results = list(query_job.result())
            if not results:
                return "Portfolio asset no encontrado", 404
            pa = dict(results[0])
            return render_template("update_portfolio_asset.html", portfolio_asset=pa)
        except Exception as e:
            return f"Error al obtener portfolio asset: {e}", 500
    else:
        portfolio_id = request.form.get('portfolio_id')
        asset_id = request.form.get('asset_id')
        quantity = request.form.get('quantity')
        avg_cost = request.form.get('avg_cost')

        if not portfolio_id or not asset_id or not quantity or not avg_cost:
            return "Faltan campos", 400
        if not check_portfolio_exists(portfolio_id):
            return f"Error: El portfolio_id {portfolio_id} no existe.", 400
        if not check_asset_exists(asset_id):
            return f"Error: El asset_id {asset_id} no existe.", 400

        update_query = f"""
            UPDATE `{table_id}`
            SET portfolio_id = '{portfolio_id}',
                asset_id = '{asset_id}',
                quantity = {float(quantity)},
                avg_cost = {float(avg_cost)}
            WHERE portfolio_asset_id = '{portfolio_asset_id}'
        """
        try:
            client.query(update_query).result()
            return redirect(url_for('list_portfolio_assets_html'))
        except Exception as e:
            return f"Error al actualizar portfolio asset: {e}", 500

@app.route('/delete_portfolio_asset_html/<portfolio_asset_id>', methods=['GET'])
def delete_portfolio_asset_html(portfolio_asset_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.portfolio_asset_data"
    delete_query = f"DELETE FROM `{table_id}` WHERE portfolio_asset_id = '{portfolio_asset_id}'"
    try:
        client.query(delete_query).result()
        return redirect(url_for('list_portfolio_assets_html'))
    except Exception as e:
        return f"Error al borrar portfolio asset: {e}", 500

# ------------------ PRICE DATA (price_data) ------------------

@app.route('/prices_html', methods=['GET'])
def list_prices_html():
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.price_data"
    query = f"""
        SELECT price_id, asset_id, date, open_price, close_price, high_price, low_price, volume
        FROM `{table_id}`
        LIMIT 50
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        prices_list = []
        for row in results:
            prices_list.append({
                "price_id": row["price_id"],
                "asset_id": row["asset_id"],
                "date": str(row["date"]),
                "open_price": row["open_price"],
                "close_price": row["close_price"],
                "high_price": row["high_price"],
                "low_price": row["low_price"],
                "volume": row["volume"]
            })
        return render_template("prices.html", prices=prices_list)
    except Exception as e:
        return f"Error al listar prices: {e}", 500

@app.route('/add_price_html', methods=['GET', 'POST'])
def add_price_html():
    if request.method == 'GET':
        return render_template("add_price.html")
    else:
        asset_id = request.form.get('asset_id')
        date = request.form.get('date')  # 'YYYY-MM-DD'
        open_price = request.form.get('open_price')
        close_price = request.form.get('close_price')
        high_price = request.form.get('high_price')
        low_price = request.form.get('low_price')
        volume = request.form.get('volume')

        if not asset_id or not date or not open_price or not close_price or \
           not high_price or not low_price or not volume:
            return "Faltan campos", 400

        if not validate_date_format(date):
            return "El formato de la fecha debe ser YYYY-MM-DD", 400

        if not validate_numeric(open_price, min_value=0) or \
           not validate_numeric(close_price, min_value=0) or \
           not validate_numeric(high_price, min_value=0) or \
           not validate_numeric(low_price, min_value=0) or \
           not validate_numeric(volume, min_value=0):
            return "Los precios y volumen deben ser números válidos y no negativos", 400

        if not check_asset_exists(asset_id):
            return f"Error: El asset_id {asset_id} no existe.", 400

        price_id = str(uuid.uuid4())
        table_id = f"{PROJECT_ID}.{DATASET_NAME}.price_data"
        rows_to_insert = [{
            "price_id": price_id,
            "asset_id": asset_id,
            "date": date,
            "open_price": float(open_price),
            "close_price": float(close_price),
            "high_price": float(high_price),
            "low_price": float(low_price),
            "volume": int(volume)
        }]
        try:
            errors = client.insert_rows_json(table_id, rows_to_insert)
            if not errors:
                return redirect(url_for('list_prices_html'))
            else:
                return f"Error al insertar price: {errors}", 400
        except Exception as e:
            return f"Error: {e}", 500

@app.route('/update_price_html/<price_id>', methods=['GET', 'POST'])
def update_price_html(price_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.price_data"
    if request.method == 'GET':
        query = f"""
            SELECT price_id, asset_id, date, open_price, close_price, high_price, low_price, volume
            FROM `{table_id}`
            WHERE price_id = '{price_id}'
        """
        try:
            query_job = client.query(query)
            results = list(query_job.result())
            if not results:
                return "Price no encontrado", 404
            price = dict(results[0])
            return render_template("update_price.html", price=price)
        except Exception as e:
            return f"Error al obtener price: {e}", 500
    else:
        asset_id = request.form.get('asset_id')
        date = request.form.get('date')
        open_price = request.form.get('open_price')
        close_price = request.form.get('close_price')
        high_price = request.form.get('high_price')
        low_price = request.form.get('low_price')
        volume = request.form.get('volume')

        if not asset_id or not date or not open_price or not close_price or not high_price or not low_price or not volume:
            return "Faltan campos", 400

        if not validate_date_format(date):
            return "El formato de la fecha debe ser YYYY-MM-DD", 400

        if not validate_numeric(open_price, min_value=0) or \
           not validate_numeric(close_price, min_value=0) or \
           not validate_numeric(high_price, min_value=0) or \
           not validate_numeric(low_price, min_value=0) or \
           not validate_numeric(volume, min_value=0):
            return "Los precios y volumen deben ser números válidos y no negativos", 400

        if not check_asset_exists(asset_id):
            return f"Error: El asset_id {asset_id} no existe.", 400

        update_query = f"""
            UPDATE `{table_id}`
            SET asset_id = '{asset_id}',
                date = '{date}',
                open_price = {float(open_price)},
                close_price = {float(close_price)},
                high_price = {float(high_price)},
                low_price = {float(low_price)},
                volume = {int(volume)}
            WHERE price_id = '{price_id}'
        """
        try:
            client.query(update_query).result()
            return redirect(url_for('list_prices_html'))
        except Exception as e:
            return f"Error al actualizar price: {e}", 500

@app.route('/delete_price_html/<price_id>', methods=['GET'])
def delete_price_html(price_id):
    table_id = f"{PROJECT_ID}.{DATASET_NAME}.price_data"
    delete_query = f"DELETE FROM `{table_id}` WHERE price_id = '{price_id}'"
    try:
        client.query(delete_query).result()
        return redirect(url_for('list_prices_html'))
    except Exception as e:
        return f"Error al borrar price: {e}", 500

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)

