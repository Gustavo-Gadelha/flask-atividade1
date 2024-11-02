from flask import Blueprint, redirect, request, render_template, flash, url_for

from app import validation, session, db
from app.models import Product

product_bp = Blueprint('product', __name__)


@product_bp.route('/list', methods=['GET'])
def list_all():
    return render_template('product/list.html', products=Product.query.all())


@product_bp.route('/register', methods=['POST'])
def register():
    if not session.has_user_session():
        flash('Você precisa estar autenticado para cadastrar um produto', validation.ERROR_MESSAGE)
        return redirect(url_for('list'))

    name: str = request.form.get('product-name')
    quantity: str = request.form.get('quantity')
    price: str = request.form.get('price')

    validation.validade_product(name, quantity, price, session.get_user_id())

    if not validation.has_errors():
        product = Product(name, quantity, price, session.get_user_id())
        db.session.add(product)
        db.session.commit()

    return redirect(url_for('.list_all'))
