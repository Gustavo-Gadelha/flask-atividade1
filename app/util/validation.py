def validate_register(username: str, password: str, confirm_password: str) -> list[str]:
    error_messages: list[str] = list()

    if username != username.strip() or password != password.strip():
        error_messages.append('Não use espaços em branco no inicio ou no final do seu nome de usuario e/ou senha')
        return error_messages

    if len(username) < 5:
        error_messages.append('O nome de usuário deve ter pelo menos 5 caracteres')
    if len(password) < 5:
        error_messages.append('A senha deve ter pelo menos 5 caracteres')
    if password != confirm_password:
        error_messages.append('As senhas não correspondem')

    return error_messages
