from flask import Blueprint, render_template, request, redirect, flash, url_for

from app import validation, session, db
from app.models import UserAccount
from app.models.user_account import AccountType

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username: str | None = request.form.get('username')
        password: str | None = request.form.get('password')

        user = UserAccount.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            session.create(user)
            flash('Usuário autenticado com sucesso', validation.SUCCESS_MESSAGE)
        else:
            flash('Usuário ou senha não encontrados', validation.ERROR_MESSAGE)

        return redirect(url_for('.login'))


@user_bp.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.teardown()
        return redirect(url_for('.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username: str | None = request.form.get('username')
        password: str | None = request.form.get('password')
        confirm_password: str | None = request.form.get('confirm-password')
        user_type: AccountType = AccountType.SUPER if request.form.get('is-super') == 'on' else AccountType.NORMAL

        validation.validate_user(username, password, confirm_password)

        if not validation.has_errors():
            user_account = UserAccount(username, password, user_type)
            db.session.add(user_account)
            db.session.commit()

            flash('Usuário criado com sucesso', validation.SUCCESS_MESSAGE)
            return redirect(url_for('.login'))

        return redirect(url_for('.register'))
