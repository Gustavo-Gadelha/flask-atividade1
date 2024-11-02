from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_login import login_required, current_user
from marshmallow import ValidationError

from app import db
from app.models import Product, UserAccount
from app.models.user_account import AccountType, NORMAL_ACCOUNT_MAX_PRODUCTS
from app.schemas.product import products_schema, product_schema
from app.schemas.user_account import user_accounts_schema, user_account_schema

api_bp = Blueprint('api', __name__)


@api_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    access_token = create_access_token(identity=user_account_schema.dump(current_user))
    return render_template('api/dashboard.html', access_token=access_token)


@api_bp.route('/user/token', methods=['POST'])
def get_token():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Both username and password are required in the request"}), 400

    username = data.get('username')
    password = data.get('password')

    user = UserAccount.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Username not found. Please check your credentials or sign up if you don't have an account"}), 404

    if user.check_password(password):
        access_token = create_access_token(identity=user_account_schema.dump(user))
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Incorrect password. Please try again"}), 401


@api_bp.route('/products/insert', methods=['POST'])
@jwt_required()
def insert_product():
    data = request.json
    user = UserAccount.query.get(get_jwt_identity()['id'])

    if not user:
        return jsonify({"error": "Username not found. Please check your credentials or sign up if you don't have an account"}), 404

    data['user_id'] = user.id

    try:
        product = product_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if user.account_type == AccountType.NORMAL:
        product_count = Product.query.filter_by(user_id=user.id).count()
        if product_count >= NORMAL_ACCOUNT_MAX_PRODUCTS:
            return jsonify({"error": "Product limit reached for normal users"}), 403

    db.session.add(product)
    db.session.commit()

    return jsonify(product_schema.dump(product)), 200


@api_bp.route('/products/id/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product_schema.dump(product)), 200
    else:
        return jsonify({
            "error": "Product not found",
            "requested_product_id": product_id
        }), 404


@api_bp.route('/products/name/<string:product_name>', methods=['GET'])
@jwt_required()
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
@jwt_required()
def get_all_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200


@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    user_accounts = UserAccount.query.filter_by(is_admin=False).all()
    return jsonify(user_accounts_schema.dump(user_accounts)), 200
