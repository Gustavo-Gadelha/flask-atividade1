from itertools import product

from flask import jsonify, request, Blueprint

from app import user_account, product

api_bp = Blueprint('api', __name__)


@api_bp.route('/products/insert', methods=['POST'])
def insert_product():
    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')
    price = data.get('price')
    user_id = user_account.session_id()

    if not name or not isinstance(name, str):
        return jsonify({"error": "Product name is required and must be a string"}), 400
    if quantity is None or not isinstance(quantity, int) or quantity < 0:
        return jsonify({"error": "Quantity must be a non-negative integer"}), 400
    if price is None or not isinstance(price, (float, int)) or price < 0:
        return jsonify({"error": "Price must be a non-negative number"}), 400

    if new_product := product.create(name, quantity, price, user_id):
        return jsonify(new_product), 200


@api_bp.route('/products/name/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id: int):
    if query_product := product.get_by_id(product_id):
        return jsonify(query_product)
    else:
        return jsonify({"error": "Product not found"}), 404


@api_bp.route('/products/id/<string:product_name>', methods=['GET'])
def get_product_by_name(product_name: str):
    if query_product := product.get_by_name(product_name):
        return jsonify(query_product)
    else:
        return jsonify({"error": "Product not found"}), 404


@api_bp.route('/products', methods=['GET'])
def get_all_products():
    return jsonify(product.get_all()), 200


@api_bp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(user_account.get_all()), 200
