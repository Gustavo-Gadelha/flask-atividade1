import re

from flask import flash, session

from app.models import UserAccount, Product, AccountType
from app.models.user_account import NORMAL_ACCOUNT_MAX_PRODUCTS

SUCCESS_MESSAGE: str = 'success'
ERROR_MESSAGE: str = 'error'


def validate_user(username: str, password: str, confirm_password: str):
    if username != username.strip():
        flash('Não use espaços em branco no inicio ou no final do seu nome de usuário', ERROR_MESSAGE)
    if len(username) < 5 or len(username) > 255:
        flash('O nome de usuário deve ter entre 5 e 255 caracteres', ERROR_MESSAGE)
    if not re.match(r'^[a-zA-Z0-9_À-ÿ]+(?: [a-zA-Z0-9_À-ÿ]+)*$', username):
        flash('O nome de usuário só pode conter letras, números, sublinhados, e espaços entre palavras', ERROR_MESSAGE)
    if UserAccount.query.filter_by(username=username).count() > 0:
        flash('Já existe um usuário com esse nome', ERROR_MESSAGE)

    if password != password.strip():
        flash('Não use espaços em branco no inicio ou no final da sua senha', ERROR_MESSAGE)
    if len(password) < 5 or len(password) > 255:
        flash('A senha deve ter entre 5 e 255 caracteres', ERROR_MESSAGE)

    if password != confirm_password:
        flash('As senhas não coincidem', ERROR_MESSAGE)

    return not _has_errors()


def validate_product(product_name: str, quantity: str, price: str, user_id: int):
    if product_name != product_name.strip():
        flash('O nome do produto não deve conter espaços em branco no início ou no final.', ERROR_MESSAGE)
    if len(product_name) < 5 or len(product_name) > 60:
        flash('O nome do produto deve ter entre 5 e 60 caracteres.', ERROR_MESSAGE)
    if not re.match(r'^[a-zA-Z0-9_À-ÿ]+(?: [a-zA-Z0-9_À-ÿ]+)*$', product_name):
        flash(
            'O nome do produto deve conter apenas letras, números e underscores, podendo incluir espaços entre as palavras.',
            ERROR_MESSAGE)

    if not quantity.isdecimal() or int(quantity) <= 0:
        flash('A quantidade do produto deve ser um número inteiro positivo não-nulo', ERROR_MESSAGE)
    elif len(quantity) > 10:
        flash('A quantidade do produto não pode exceder 10 dígitos', ERROR_MESSAGE)

    if not re.match(r'^\d{1,10}(\.\d{1,2})?$', price) or float(price) <= 0:
        flash(
            'O preço do produto deve ser um número positivo não-nulo com até 10 dígitos antes do ponto decimal e até duas casas decimais',
            ERROR_MESSAGE)

    if UserAccount.query.get(user_id).account_type == AccountType.NORMAL:
        product_count = Product.query.filter_by(user_id=user_id).count()
        if product_count >= NORMAL_ACCOUNT_MAX_PRODUCTS:
            flash('Usuários normais não podem cadastrar mais de 3 produtos', ERROR_MESSAGE)

    if Product.query.filter_by(name=product_name, user_id=user_id).first():
        return flash('Um produto com este nome já existe para este usuário', ERROR_MESSAGE)

    return not _has_errors()


def _has_errors():
    if (messages := session.get('_flashes')) is not None:
        error_messages = [message for category, message in messages if category == ERROR_MESSAGE]
        return len(error_messages) > 0

    return False
