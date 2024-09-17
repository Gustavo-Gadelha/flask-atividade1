from flask import flash, session

from app import user_account, product

SUCCESS_MESSAGE: str = 'success'
ERROR_MESSAGE: str = 'error'


def validate_user(username: str, password: str, confirm_password: str):
    if username != username.strip() or password != password.strip():
        flash('Não use espaços em branco no inicio ou no final do seu nome de usuário e/ou senha', ERROR_MESSAGE)
    if len(username) < 5:
        flash('O nome de usuário deve ter pelo menos 5 caracteres', ERROR_MESSAGE)
    if len(password) < 5:
        flash('A senha deve ter pelo menos 5 caracteres', ERROR_MESSAGE)
    if password != confirm_password:
        flash('As senhas não correspondem', ERROR_MESSAGE)
    if user_account.get_by_username(username):
        flash('Já existe um usuário com esse nome', ERROR_MESSAGE)


def validade_product(product_name: str, quantity: str, price: str, user_id: int):
    if product_name != product_name.strip():
        flash('Não use espaços em branco no inicio ou no final do nome do produto', ERROR_MESSAGE)
    if not quantity.isdecimal() or int(quantity) <= 0:
        flash('A quantidade do produto deve ser um numero inteiro positivo não-nulo', ERROR_MESSAGE)
    if not price.replace('.', '', 1).isdecimal() or float(price) <= 0:
        flash('O preço do produto deve ser um numero positivo não-nulo', ERROR_MESSAGE)
    if user_account.get_by_id(user_id).type == 'normal' and len(product.get_by_user_id(user_id)) >= 3:
        flash('Usuário normais não podem cadastrar mais de 3 produtos', ERROR_MESSAGE)


def has_errors():
    if (messages := session.get('_flashes')) is not None:
        error_messages = [message for category, message in messages if category == ERROR_MESSAGE]
        return error_messages is not None

    return False
