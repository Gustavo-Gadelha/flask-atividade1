from flask import render_template, request, redirect, session, flash

from app import create_app
from app import user_account
from config import DevelopmentConfig
from util.validation import validate_user, validade_product

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

        if user_account.verify_login(username, password):
            session['user']: str = username
            session['authenticated']: bool = True
            return redirect('/product/list')

        else:
            error_messages: list[str] = ['Usuário ou senha não encontrados']
            return render_template('user/login.html', error_messages=error_messages)


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        confirm_password: str = request.form.get('confirm-password')
        user_type: str = 'super' if (request.form.get('is-super') == 'on') else 'normal'

        error_messages: list[str] = validate_user(username, password, confirm_password)

        if error_messages:
            return render_template('user/register.html', error_messages=error_messages)

        else:
            user_account.create_user(username, password, user_type)
            success_messages = ['Usuário criado com sucesso']
            return render_template('user/login.html', success_messages=success_messages)


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.clear()
    return redirect('/')


@app.route('/product/list', methods=['POST', 'GET'])
def product_list():
    if request.method == 'GET':
        return render_template('product/list.html')

    elif request.method == 'POST':
        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        if 'user' not in session or 'authenticated' not in session:
            error_messages: list[str] = ['Você precisa estar autenticado para cadastrar um produto']
            return render_template('product/list.html', error_messages=error_messages)

        error_messages: list[str] = validade_product(product_name, quantity, price)

        if error_messages:
            return render_template('product/list.html', error_messages=error_messages)

        return render_template('product/list.html')


if __name__ == '__main__':
    app.run(debug=True)
