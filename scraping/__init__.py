from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Creamos instancia de la clase SQLAlchemy
db = SQLAlchemy()


# @audit create_app()
def create_app():
    # Creamos Aplicación Flask.
    app = Flask(__name__)

    # Agregamos archivo config.py
    app.config.from_object('config.Config')

    # Inicializamos la base de datos y mandamos app.
    db.init_app(app)

    # Registramos las vistas de home.py
    from scraping import home
    app.register_blueprint(home.bp)

    # Registramos las vistas de auth.py
    from scraping import auth
    app.register_blueprint(auth.bp)
    
    # Registramos las vistas de post.py
    from scraping import post
    app.register_blueprint(post.bp)

    # Importamos los modulos creados.
    from .models import (User, Post)

    # Migramos los Modelos creados de manera automática.
    with app.app_context():
        db.create_all()

    return app
