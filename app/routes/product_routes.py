from flask import Blueprint, redirect, request, render_template, flash, url_for

from app import validation, product, user_account

product_bp = Blueprint('product', __name__)


@product_bp.route('/list', methods=['GET', 'POST'])
def list_all():
    if request.method == 'GET':
        return render_template('product/list.html', products=product.get_all())

    elif request.method == 'POST':
        if not user_account.has_session():
            flash('Você precisa estar autenticado para cadastrar um produto', validation.ERROR_MESSAGE)
            return redirect(url_for('list'))

        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        validation.validade_product(product_name, quantity, price, user_account.session_id())

        if not validation.has_errors():
            product.create(product_name, quantity, price, user_account.session_id())

        return redirect(url_for('.list_all'))
