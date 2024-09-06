from flask import Flask

from app.database import DatabaseManager
from config import config_manager

db_manager = DatabaseManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_manager[config_name])

    config_manager[config_name].init_app(app)

    db_manager.init_app(app)

    with app.app_context():
        db_manager.init_db()

    return app
