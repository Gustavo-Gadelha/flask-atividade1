from flask import jsonify, request, Blueprint

from app import db
from app.models import Product, UserAccount
from app.schemas.product import products_schema, product_schema
from app.schemas.user_account import user_accounts_schema

api_bp = Blueprint('api', __name__)


@api_bp.route('/products/insert', methods=['POST'])
def insert_product():
    data = request.json

    product = product_schema.load(data)

    db.session.add(product)
    db.session.commit()

    return jsonify(product_schema.dump(product)), 200


@api_bp.route('/products/id/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product_schema.dump(product)), 200
    else:
        return jsonify({
            "error": "Product not found",
            "requested_product_id": product_id,
        }), 404


@api_bp.route('/products/name/<string:product_name>', methods=['GET'])
def get_product_by_name(product_name):
    products = Product.query.filter_by(name=product_name).all()
    if products:
        return jsonify(products_schema.dump(products)), 200
    else:
        return jsonify({
            "error": "Product not found",
            "requested_product": product_name
        }), 404


@api_bp.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200


@api_bp.route('/users', methods=['GET'])
def get_all_users():
    user_accounts = UserAccount.query.all()
    return jsonify(user_accounts_schema.dump(user_accounts)), 200
