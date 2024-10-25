from flask import render_template, request, redirect, flash

from app import create_app, validation
from app import product
from app import user_account

app = create_app()


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

        if user := user_account.get_by_login(username, password):
            user_account.create_session(user)
            flash('Usuário autenticado com sucesso', validation.SUCCESS_MESSAGE)

        else:
            flash('Usuário ou senha não encontrados', validation.ERROR_MESSAGE)

        return redirect('/user/login')


@app.route('/user/logout', methods=['GET'])
def user_logout():
    if request.method == 'GET':
        user_account.teardown_session()
        return redirect('/user/login')


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        confirm_password: str = request.form.get('confirm-password')
        user_type: str = 'super' if request.form.get('is-super') == 'on' else 'normal'

        validation.validate_user(username, password, confirm_password)

        if not validation.has_errors():
            user_account.create(username, password, user_type)
            flash('Usuário criado com sucesso', validation.SUCCESS_MESSAGE)

        return redirect('/user/register')


@app.route('/product/list', methods=['GET', 'POST'])
def product_list():
    if request.method == 'GET':
        return render_template('product/list.html', products=product.get_all())

    elif request.method == 'POST':
        if not user_account.has_session():
            flash('Você precisa estar autenticado para cadastrar um produto', validation.ERROR_MESSAGE)
            return redirect('/product/list')

        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        validation.validade_product(product_name, quantity, price, user_account.session_id())

        if not validation.has_errors():
            product.create(product_name, quantity, price, user_account.session_id())

        return redirect('/product/list')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
