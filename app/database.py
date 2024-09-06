import psycopg2
from flask import g, current_app


class DatabaseManager:
    def __init__(self, app=None):
        self.app = app

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown_db)

    def init_db(self):
        connection = self.get_connection()

        with current_app.open_resource('schema.sql') as schema:
            sql = schema.read().decode('utf8')
            self.execute(sql)

    def execute(self, query, params=None, fetch=False, one=False):
        connection = self.get_connection()

        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute(query, params)

                    if fetch and one:
                        return cur.fetchone()
                    if fetch and not one:
                        return cur.fetchall()

        except psycopg2.Error as e:
            print(f'Error ao executar query: {e}')
            connection.rollback()

    def create_connection(self):
        if self.has_connection():
            return

        try:
            g.db = psycopg2.connect(
                dbname=self.app.config['DB_NAME'],
                user=self.app.config['DB_USER'],
                password=self.app.config['DB_PASSWORD'],
                host=self.app.config['DB_HOST'],
                port=self.app.config['DB_PORT']
            )
        except psycopg2.Error as e:
            print(f'Error ao conectar ao Bacno: {e}')
            g.db = None

    def get_connection(self):
        if not self.has_connection():
            self.create_connection()

        return g.db

    def close_connection(self):
        if self.has_connection():
            g.db.close()

        g.pop('db', None)

    def has_connection(self):
        return ('db' in g) and (g.db is not None) and (not g.db.closed)

    def teardown_db(self, exception):
        try:
            self.close_connection()
        except psycopg2.Error as e:
            raise exception
