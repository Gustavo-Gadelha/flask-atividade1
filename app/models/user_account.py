import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Enum

from app import db, bcrypt

NORMAL_ACCOUNT_MAX_PRODUCTS = 3


class AccountType(enum.Enum):
    NORMAL = 'normal'
    SUPER = 'super'


class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    account_type = db.Column(Enum(AccountType), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    products = db.relationship('Product', backref='user', lazy=True)

    def __init__(self, username, password, account_type):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.account_type = account_type

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<UserAccount(id={self.id}, username='{self.username}', account_type='{self.account_type}', is_admin={self.is_admin})>"
