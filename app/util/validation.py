def validate_user(username: str, password: str, confirm_password: str) -> list[str]:
    error_messages: list[str] = list()

    if username != username.strip() or password != password.strip():
        error_messages.append('Não use espaços em branco no inicio ou no final do seu nome de usuario e/ou senha')
    if len(username) < 5:
        error_messages.append('O nome de usuário deve ter pelo menos 5 caracteres')
    if len(password) < 5:
        error_messages.append('A senha deve ter pelo menos 5 caracteres')
    if password != confirm_password:
        error_messages.append('As senhas não correspondem')

    return error_messages


def validade_product(product_name: str, quantity: str, price: str) -> list[str]:
    error_messages: list[str] = list()

    if product_name != product_name.strip():
        error_messages.append('Não use espaços em branco no inicio ou no final do nome do produto')
    if not quantity.isdecimal() or int(quantity) <= 0:
        error_messages.append('A quantidade do produto deve ser um numero inteiro positivo não-nulo')
    if not price.replace('.', '', 1).isdecimal() or float(price) <= 0:
        error_messages.append('O preço do produto deve ser um numero positivo não-nulo')

    return error_messages
