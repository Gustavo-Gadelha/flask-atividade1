from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    from . import database
    with app.app_context():
        database.init_db()

    return app
