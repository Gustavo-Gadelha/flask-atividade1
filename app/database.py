import psycopg2
from flask import g, current_app
from psycopg2.extras import NamedTupleCursor


def init_app(app):
    app.teardown_appcontext(teardown_connection)

    with app.app_context():
        init_db()


def init_db():
    connection = get_connection()

    with current_app.open_resource('schema.sql') as schema:
        sql = schema.read().decode('utf8')

    with connection, connection.cursor() as cur:
        cur.execute(sql)


def get_connection():
    if has_open_connetion():
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
    if has_open_connetion():
        g.db.close()

    g.pop('db', None)


def has_open_connetion():
    return ('db' in g) and (g.db is not None) and (not g.db.closed)


def teardown_connection(exception):
    try:
        close_connection()
    except psycopg2.Error as e:
        raise exception
