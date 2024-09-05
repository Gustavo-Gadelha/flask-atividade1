from pathlib import Path

from dotenv import load_dotenv
from flask import render_template, request, redirect

from app import create_app
from app.util.validation import validate_register

env_path: Path = Path(__file__).parent / '.env'

if env_path.exists():
    load_dotenv(env_path)

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

        return redirect('/')


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
        confirm_password: str = request.form.get('confirmPassword')

        error_messages: list[str] = validate_register(username, password, confirm_password)

        if error_messages:
            return render_template('user/register.html', error_messages=error_messages)

        return redirect('/')


if __name__ == '__main__':
    app.run()
