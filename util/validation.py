from flask import flash, get_flashed_messages, session

from app import user_account

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
    if user_account.get_user_by_username(username):
        flash('Já existe um usuário com esse nome', ERROR_MESSAGE)


def validade_product(product_name: str, quantity: str, price: str):
    if product_name != product_name.strip():
        flash('Não use espaços em branco no inicio ou no final do nome do produto', ERROR_MESSAGE)
    if not quantity.isdecimal() or int(quantity) <= 0:
        flash('A quantidade do produto deve ser um numero inteiro positivo não-nulo', ERROR_MESSAGE)
    if not price.replace('.', '', 1).isdecimal() or float(price) <= 0:
        flash('O preço do produto deve ser um numero positivo não-nulo', ERROR_MESSAGE)


def has_errors():
    return get_flashed_messages(category_filter=['error'])


def has_user_session():
    return ('user' in session) and (session['user']) and ('authenticated' in session) and (session['authenticated'])
