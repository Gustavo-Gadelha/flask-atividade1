from flask import Blueprint, redirect, request, render_template, url_for, jsonify
from flask_login import login_required, current_user

from app import db
from app.models import Product
from app.validation import validate_product

product_bp = Blueprint('product', __name__)


@product_bp.route('/list', methods=['GET'])
def list_all():
    return render_template('product/list.html', products=Product.query.all())


@product_bp.route('/register', methods=['POST'])
@login_required
def register():
    name = request.form.get('product-name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    if validate_product(name, quantity, price, current_user.id):
        product = Product(name, quantity, price, current_user.id)
        db.session.add(product)
        db.session.commit()

    return redirect(url_for('.list_all'))


@product_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete(product_id):
    product = Product.query.get(product_id)

    if not product:
        return redirect(url_for('.list_all'))

    if current_user.is_admin:
        db.session.delete(product)
        db.session.commit()
    else:
        return jsonify({'error': 'Você não tem permissão para deletar este produto'}), 403

    return redirect(url_for('.list_all'))
