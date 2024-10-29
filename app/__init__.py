import os

from flask import Flask, url_for, redirect

from app.config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV', 'development') == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    from . import database
    with app.app_context():
        database.init_db()

    from .routes import user_bp, product_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/product')

    @app.route('/')
    def index():
        return redirect(url_for('product.list_all'))

    return app
