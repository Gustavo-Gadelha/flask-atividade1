import psycopg2
from flask import g, current_app
from psycopg2.extras import NamedTupleCursor


def init_db():
    current_app.teardown_appcontext(teardown_connection)

    with current_app.open_resource('schema.sql') as schema:
        sql = schema.read().decode('utf8')

    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql)


def get_connection():
    if has_open_connection():
        return g.db

    try:
        g.db = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            cursor_factory=NamedTupleCursor
        )

        return g.db

    except psycopg2.Error as e:
        print(f'Error ao conectar ao banco: {e}')


def close_connection():
    if has_open_connection():
        g.db.close()

    g.pop('db', None)


def has_open_connection():
    return g.get('db') is not None and (not g.db.closed)


def teardown_connection(exception):
    try:
        close_connection()
    except psycopg2.Error as connection_error:
        raise Exception(exception, connection_error)
