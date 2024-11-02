import os

from flask import Flask, url_for, redirect
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from app.config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    if os.environ.get('FLASK_ENV', 'production') == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    # TODO: use flask-Migrate to make migrations instead of overwriting the database on update
    from .models import UserAccount, product
    with app.app_context():
        db.create_all()

    from .routes import user_bp, product_bp, api_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(api_bp, url_prefix='/api')

    from .schemas import ProductSchema

    @app.route('/')
    def index():
        return redirect(url_for('product.list_all'))

    return app
