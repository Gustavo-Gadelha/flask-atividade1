import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__name__).parent.resolve()

load_dotenv(BASE_DIR / '.env')


class Config(object):
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'unsafe_secret_key')

    SESSION_COOKIE_NAME: str = os.environ.get('SESSION_COOKIE_NAME', 'session')
    SESSION_COOKIE_HTTPONLY: bool = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    REMEMBER_COOKIE_HTTPONLY: bool = os.environ.get('REMEMBER_COOKIE_HTTPONLY', 'True') == 'True'
    SESSION_COOKIE_SAMESITE: str = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')


class DevelopmentConfig(Config):
    DEBUG: bool = True

    DATABASE_NAME: str = os.environ.get('DEV_DATABASE_NAME')
    DATABASE_USER: str = os.environ.get('DEV_DATABASE_USER')
    DATABASE_PASSWORD: str = os.environ.get('DEV_DATABASE_PASSWORD')
    DATABASE_HOST: str = os.environ.get('DEV_DATABASE_HOST')
    DATABASE_PORT: str = os.environ.get('DEV_DATABASE_PORT')
    DATABASE_URI: str = os.environ.get('DEV_DATABASE_URI')


class ProductionConfig(Config):
    DEBUG: bool = False

    DATABASE_NAME: str = os.environ.get('DATABASE_NAME')
    DATABASE_USER: str = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD: str = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST: str = os.environ.get('DATABASE_HOST')
    DATABASE_PORT: str = os.environ.get('DATABASE_PORT')
    DATABASE_URI: str = os.environ.get('DATABASE_URI')
