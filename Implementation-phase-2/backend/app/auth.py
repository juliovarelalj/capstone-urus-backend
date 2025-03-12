# app/auth.py
import uuid
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import get_bigquery_client, get_dataset_id
from google.cloud import bigquery

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates/auth')

def login_required(f):
    """
    Decorador para proteger rutas que requieren inicio de sesión.
    Si no existe 'user_id' en la sesión, redirige a /login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        if not email or not password or not first_name or not last_name:
            flash('Por favor, completa todos los campos.', 'danger')
            return redirect(url_for('auth_bp.register'))

        hashed_pw = generate_password_hash(password)
        user_id = str(uuid.uuid4())

        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_ref = f"{client.project}.{dataset_id}.User_Data"

        query = f"""
            INSERT INTO `{table_ref}` (user_id, email, hashed_password, first_name, last_name, created_at)
            VALUES (
                '{user_id}',
                '{email}',
                '{hashed_pw}',
                '{first_name}',
                '{last_name}',
                CURRENT_TIMESTAMP()
            )
        """
        client.query(query)

        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Completa todos los campos.', 'danger')
            return redirect(url_for('auth_bp.login'))

        client = get_bigquery_client()
        dataset_id = get_dataset_id()
        table_ref = f"{client.project}.{dataset_id}.User_Data"

        query = f"""
            SELECT user_id, hashed_password, first_name, last_name
            FROM `{table_ref}`
            WHERE email = '{email}'
            LIMIT 1
        """
        rows = list(client.query(query).result())

        if not rows:
            flash('No existe un usuario con ese email.', 'danger')
            return redirect(url_for('auth_bp.login'))

        user = rows[0]
        stored_hashed_pw = user.get("hashed_password")
        user_id = user.get("user_id")

        if not check_password_hash(stored_hashed_pw, password):
            flash('Contraseña incorrecta.', 'danger')
            return redirect(url_for('auth_bp.login'))

        session['user_id'] = user_id
        session['email'] = email
        session['first_name'] = user.get("first_name")
        session['last_name'] = user.get("last_name")

        flash('Sesión iniciada correctamente.', 'success')
        return redirect(url_for('routes_bp.asset_classes'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth_bp.login'))
