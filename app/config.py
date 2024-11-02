import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__name__).parent.resolve()

load_dotenv(BASE_DIR / '.env')


class _Config(object):
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'unsafe_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'True') == 'True'

    SESSION_COOKIE_NAME: str = os.environ.get('SESSION_COOKIE_NAME', 'session')
    SESSION_COOKIE_HTTPONLY: bool = os.environ.get('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
    REMEMBER_COOKIE_HTTPONLY: bool = os.environ.get('REMEMBER_COOKIE_HTTPONLY', 'True') == 'True'
    SESSION_COOKIE_SAMESITE: str = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')

    JWT_ISSUER: str = os.environ.get('JWT_ISSUER')
    JWT_AUTHTYPE: str = os.environ.get('JWT_AUTHTYPE')
    JWT_SECRET: str = os.environ.get('JWT_SECRET')


class DevelopmentConfig(_Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class ProductionConfig(_Config):
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
