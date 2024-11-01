from app.database import get_connection


def create(name, quantity, price, user_id):
    sql = 'INSERT INTO product (name, quantity, price, user_id) VALUES (%s, %s, %s, %s) RETURNING id;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (name, quantity, price, user_id))
        return cur.fetchone()


def get_all():
    sql = 'SELECT * FROM product;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_by_id(product_id):
    sql = 'SELECT * FROM product WHERE id = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (product_id,))
        return cur.fetchone()

def get_by_name(product_name):
    sql = 'SELECT * FROM product WHERE name = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (product_name,))
        return cur.fetchone()


def get_by_user_id(user_id):
    sql = 'SELECT p.* FROM product p JOIN user_account u ON p.user_id = u.id WHERE u.id = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchall()


def update(product_id, name, quantity, price, user_id):
    sql = f'UPDATE product SET name = %s, quantity = %s, price = %s, user_id = %s WHERE id = %s RETURNING *;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (name, quantity, price, user_id, product_id))
        return cur.fetchone()


def delete(product_id):
    sql = 'DELETE FROM product WHERE id = %s;'

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (product_id,))
