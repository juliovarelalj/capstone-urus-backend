# app/__init__.py
import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

def create_app():
    # Carga variables de entorno desde .env
    load_dotenv()

    # Crea la aplicación Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cualquier-valor-seguro'  # Para sesiones o formularios

    # Registrar el blueprint de autenticación
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Registra las rutas (blueprint)
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    # Registrar blueprint de portfolios
    from app.portfolios import portfolios_bp
    app.register_blueprint(portfolios_bp)

    from app.chat import chat_bp
    app.register_blueprint(chat_bp)

    # La raíz "/" redirige a la página de login para que sea la primera en mostrarse
    @app.route('/')
    def index():
        return redirect(url_for('auth_bp.login'))

    return app
