import os
from pathlib import Path

from flask import session


class Config(object):
    BASE_DIR = Path(__name__).parent.resolve()

    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'unsafe_secret_key')

    SESSION_COOKIE_NAME: str = os.environ.get('SESSION_COOKIE_NAME', 'session')
    SESSION_COOKIE_HTTPONLY: bool = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    REMEMBER_COOKIE_HTTPONLY: bool = os.environ.get('REMEMBER_COOKIE_HTTPONLY', 'True') == 'True'
    SESSION_COOKIE_SAMESITE: str = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')

    DB_NAME: str = os.environ.get('DB_NAME')
    DB_USER: str = os.environ.get('DB_USER')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
    DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
    DB_PORT: str = os.environ.get('DB_PORT', '5432')

    DATABASE_URI: str = os.environ.get('DATABASE_URI')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG: bool = True


class ProductionConfig(Config):
    DEBUG: bool = False


config_manager = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
