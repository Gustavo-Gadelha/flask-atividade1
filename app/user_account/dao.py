import bcrypt

from app.database import get_connection


def create_user(username, password, user_type):
    sql = 'INSERT INTO user_account (username, password, type) VALUES (%s, %s, %s) RETURNING *;'

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (username, hashed.decode('utf-8'), user_type))
        return cur.fetchone()


def get_all_users():
    sql = 'SELECT * FROM user_account'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_user_by_id(user_id):
    sql = 'SELECT * FROM user_account WHERE id = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchone()


def get_user_by_username(username):
    sql = 'SELECT * FROM user_account WHERE username = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (username,))
        return cur.fetchone()


def get_user_by_login(username, password):
    user = get_user_by_username(username)
    return user is not None and bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))


def update_user(user_id, username, password, user_type):
    sql = f'UPDATE user_account SET username = %s, password = %s, type = %s WHERE id = %s RETURNING *;'

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (username, hashed.decode('utf-8'), user_type, user_id))
        return cur.fetchone()


def delete_user(user_id):
    sql = 'DELETE FROM user_account WHERE id = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (user_id,))
