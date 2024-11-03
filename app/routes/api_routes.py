from flask import jsonify, request, Blueprint, render_template
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_login import login_required, current_user
from marshmallow import ValidationError

from app import db
from app.models import Product, UserAccount
from app.schemas.product import products_schema, product_schema
from app.schemas.user_account import user_accounts_schema, user_account_schema
from app.validation import validate_product_api

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
        return jsonify({'error': 'É necessário fornecer tanto o nome de usuário quanto a senha na solicitação'}), 400

    username = data.get('username')
    password = data.get('password')

    user = UserAccount.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Nome de usuário não encontrado. Por favor, verifique suas credenciais ou cadastre-se se você não tiver uma conta'}), 404

    if user.check_password(password):
        access_token = create_access_token(identity=user_account_schema.dump(user))
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Senha incorreta. Por favor, tente novamente'}), 401


@api_bp.route('/products/insert', methods=['POST'])
@jwt_required()
def insert_product():
    data = request.json
    user = UserAccount.query.get(get_jwt_identity()['id'])

    if not user:
        return jsonify({'error': 'Nome de usuário não encontrado. Por favor, verifique suas credenciais ou cadastre-se se você não tiver uma conta'}), 404

    data['user_id'] = user.id

    if errors := validate_product_api(data):
        return jsonify({'errors': errors}), 400

    try:
        product = product_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if Product.query.filter_by(name=product.name, user_id=product.user_id).first():
        return jsonify({'error': 'Um produto com este nome já existe para este usuário'}), 400

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
            'error': 'Produto não encontrado',
            'requested_product': product_id
        }), 404


@api_bp.route('/products/name/<string:product_name>', methods=['GET'])
@jwt_required()
def get_product_by_name(product_name):
    products = Product.query.filter_by(name=product_name).all()
    if products:
        return jsonify(products_schema.dump(products)), 200
    else:
        return jsonify({
            'error': 'Produto não encontrado',
            'requested_product': product_name
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
