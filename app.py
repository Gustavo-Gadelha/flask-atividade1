from flask import render_template, request, redirect, session

from app import create_app
from app.util.validation import validate_user, validade_product

app = create_app('development')


@app.route('/')
def index():
    return redirect('/product/list')


@app.route('/product/list')
def product_list():
    return render_template('product/list.html')


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')

        error_messages: list[str] = list()

        if error_messages:
            return render_template('user/login.html', error_messages=error_messages)

        session['user'] = username
        session['authenticated'] = True
        return redirect('/product/list')


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        confirm_password: str = request.form.get('confirm-password')

        error_messages: list[str] = validate_user(username, password, confirm_password)

        if error_messages:
            return render_template('user/register.html', error_messages=error_messages)

        return redirect('/user/login')


@app.route('/product/register', methods=['POST'])
def product_register():
    if request.method == 'POST':
        product_name: str = request.form.get('product-name')
        quantity: str = request.form.get('quantity')
        price: str = request.form.get('price')

        error_messages: list[str] = validade_product(product_name, quantity, price)

        if error_messages:
            return render_template('user/login.html', error_messages=error_messages)

        return redirect('/product/list')


@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run()
