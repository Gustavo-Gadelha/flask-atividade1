from flask import render_template, request, redirect, flash, url_for

from app import create_app
from app import product
from app import user_account
from config import DevelopmentConfig
from util import ERROR_MESSAGE, SUCCESS_MESSAGE, has_errors, validade_product, validate_user

app = create_app(DevelopmentConfig)


@app.route('/')
def index():
    return redirect(url_for('product_list'))


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')

        if user := user_account.get_by_login(username, password):
            user_account.create_session(user)
            return redirect(url_for('product_list'))

        else:
            flash('Usuário ou senha não encontrados', ERROR_MESSAGE)
            return render_template('user/login.html')


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        confirm_password: str = request.form.get('confirm-password')
        user_type: str = 'super' if (request.form.get('is-super') == 'on') else 'normal'

        validate_user(username, password, confirm_password)

        if has_errors():
            return render_template('user/register.html')

        user_account.create(username, password, user_type)
        flash('Usuário criado com sucesso', SUCCESS_MESSAGE)
        return redirect(url_for('user_login'))


@app.route('/user/logout', methods=['GET'])
def user_logout():
    user_account.teardown_session()
    return redirect(url_for('user_login'))


@app.route('/product/list', methods=['GET', 'POST'])
def product_list():
    if request.method == 'GET':
        return render_template('product/list.html', products=product.get_all())
    elif request.method == 'POST':
        if not user_account.has_session():
            flash('Você precisa estar autenticado para cadastrar um produto', ERROR_MESSAGE)
            return render_template('product/list.html', products=product.get_all())

        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        validade_product(product_name, quantity, price)

        if not has_errors():
            product.create(product_name, quantity, price, user_account.session_id())
            flash('Produto registrado com sucesso', SUCCESS_MESSAGE)

        return render_template('product/list.html', products=product.get_all())



if __name__ == '__main__':
    app.run(debug=True)
