from flask import Flask


# product_dao = ProductDAO()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    from . import database
    database.init_app(app)

    return app
