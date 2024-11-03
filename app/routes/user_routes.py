from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required

from app import validation, db
from app.models import UserAccount, AccountType
from app.validation import validate_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Sessão de usuário encerrada', validation.SUCCESS_MESSAGE)
    return redirect(url_for('.login'))


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserAccount.query.filter_by(username=username).first()
        if not user:
            flash('Usuário não encontrado', validation.ERROR_MESSAGE)
            return redirect(url_for('.login'))

        if user.check_password(password):
            login_user(user)
            flash('Usuário autenticado com sucesso', validation.SUCCESS_MESSAGE)
        else:
            flash('Senha inválida. Por favor, tente novamente', validation.ERROR_MESSAGE)

        return redirect(url_for('.login'))


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        account_type = AccountType.SUPER if request.form.get('is-super') == 'on' else AccountType.NORMAL

        if validate_user(username, password, confirm_password):
            user_account = UserAccount(username, password, account_type)
            db.session.add(user_account)
            db.session.commit()

            flash('Usuário criado com sucesso, faça login para continuar', validation.SUCCESS_MESSAGE)
            return redirect(url_for('.login'))

        return redirect(url_for('.register'))
