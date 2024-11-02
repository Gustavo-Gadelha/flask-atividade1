from flask import Blueprint, redirect, request, render_template, url_for
from flask_login import login_required, current_user

from app import validation, db
from app.models import Product

product_bp = Blueprint('product', __name__)


@product_bp.route('/list', methods=['GET'])
def list_all():
    return render_template('product/list.html', products=Product.query.all())


@product_bp.route('/register', methods=['POST'])
@login_required
def register():
    name: str = request.form.get('product-name')
    quantity: str = request.form.get('quantity')
    price: str = request.form.get('price')

    validation.validade_product(name, quantity, price, current_user.id)

    if not validation.has_errors():
        product = Product(name, quantity, price, current_user.id)
        db.session.add(product)
        db.session.commit()

    return redirect(url_for('.list_all'))
