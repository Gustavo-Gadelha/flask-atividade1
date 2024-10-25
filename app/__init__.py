import os

from flask import Flask

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

    return app
