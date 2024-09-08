import bcrypt

from app.user_account import get_user_by_username


def verify_login(username, password):
    user = get_user_by_username(username)

    if user is None:
        return False

    return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
