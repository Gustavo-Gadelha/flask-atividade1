from flask import Blueprint, render_template, request, redirect, flash, url_for

from app import user_account, validation

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username: str | None = request.form.get('username')
        password: str | None = request.form.get('password')

        if user := user_account.get_by_login(username, password):
            user_account.create_session(user)
            flash('Usuário autenticado com sucesso', validation.SUCCESS_MESSAGE)
        else:
            flash('Usuário ou senha não encontrados', validation.ERROR_MESSAGE)

        return redirect(url_for('.login'))


@user_bp.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        user_account.teardown_session()
        return redirect(url_for('.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str | None = request.form.get('username')
        password: str | None = request.form.get('password')
        confirm_password: str | None = request.form.get('confirm-password')
        user_type: str = 'super' if request.form.get('is-super') == 'on' else 'normal'

        validation.validate_user(username, password, confirm_password)

        if not validation.has_errors():
            user_account.create(username, password, user_type)
            flash('Usuário criado com sucesso', validation.SUCCESS_MESSAGE)

        return redirect(url_for('.login'))
