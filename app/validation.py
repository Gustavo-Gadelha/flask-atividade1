import re

from flask import flash, session

from app.models import UserAccount, Product
from app.models.user_account import NORMAL_ACCOUNT_MAX_PRODUCTS

SUCCESS_MESSAGE: str = 'success'
ERROR_MESSAGE: str = 'error'


def validate_user(username: str, password: str, confirm_password: str):
    if username != username.strip():
        flash('Não use espaços em branco no inicio ou no final do seu nome de usuário', ERROR_MESSAGE)
    if len(username) < 5 or len(username) > 255:
        flash('O nome de usuário deve ter entre 5 e 255 caracteres', ERROR_MESSAGE)
    if not re.match(r"^[a-zA-Z0-9_À-ÿ]+(?: [a-zA-Z0-9_À-ÿ]+)*$", username):
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
        flash('Não use espaços em branco no início ou no final do nome do produto', ERROR_MESSAGE)

    if not quantity.isdecimal() or int(quantity) <= 0:
        flash('A quantidade do produto deve ser um número inteiro positivo não-nulo', ERROR_MESSAGE)
    elif int(quantity) < 1:
        flash('A quantidade do produto deve ser ser maior ou igual a 1', ERROR_MESSAGE)

    if not re.match(r'^\d+(\.\d{1,2})?$', price) or float(price) <= 0:
        flash('O preço do produto deve ser um número positivo não-nulo com até duas casas decimais', ERROR_MESSAGE)
    elif float(price) < 1:
        flash('O preço do produto deve ser maior ou igual a R$ 1,00', ERROR_MESSAGE)

    if UserAccount.query.get(user_id).account_type == 'normal':
        product_count = Product.query.filter_by(user_id=user_id).count()
        if product_count >= NORMAL_ACCOUNT_MAX_PRODUCTS:
            flash('Usuários normais não podem cadastrar mais de 3 produtos', ERROR_MESSAGE)
    if Product.query.filter_by(name=product_name, user_id=user_id).first():
        return flash('Um produto com este nome já existe para este usuário', ERROR_MESSAGE)

    return not _has_errors()


def validate_product_api(data):
    errors = {}

    required_fields = ['name', 'quantity', 'price']
    for field in required_fields:
        if field not in data:
            errors[field] = f'O campo {field} é obrigatório'

    if 'quantity' in data:
        if not isinstance(data['quantity'], int) or data['quantity'] < 1:
            errors['quantity'] = 'A quantidade deve ser um número inteiro positivo maior ou igual a 1'

    if 'price' in data:
        if not isinstance(data['price'], (int, float)) or data['price'] < 1:
            errors['quantity'] = 'O preço total deve ser maior ou igual a R$ 1,00'

    return errors


def _has_errors():
    if (messages := session.get('_flashes')) is not None:
        error_messages = [message for category, message in messages if category == ERROR_MESSAGE]
        return len(error_messages) > 0

    return False
