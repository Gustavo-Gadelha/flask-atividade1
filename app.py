from flask import render_template, request, redirect, session, flash, url_for

from app import create_app
from app import user_account
from config import DevelopmentConfig
from util import ERROR_MESSAGE, SUCCESS_MESSAGE, has_errors, has_user_session, validade_product, validate_user

app = create_app(DevelopmentConfig)


@app.route('/')
def index():
    return redirect('/product/list')


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')

        if user_account.get_user_by_login(username, password):
            session['user']: str = username
            session['authenticated']: bool = True
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

        if not has_errors():
            user_account.create_user(username, password, user_type)
            flash('Usuário criado com sucesso', SUCCESS_MESSAGE)

        return render_template('user/register.html')


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.pop('user', None)
    session.pop('authenticated', None)
    return redirect(url_for('login_user'))


@app.route('/product/list', methods=['POST', 'GET'])
def product_list():
    if request.method == 'GET':
        return render_template('product/list.html')
    elif request.method == 'POST':
        if not has_user_session():
            flash('Você precisa estar autenticado para cadastrar um produto', ERROR_MESSAGE)
            return render_template('product/list.html')

        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        validade_product(product_name, quantity, price)

        return render_template('product/list.html')


if __name__ == '__main__':
    app.run(debug=True)
