import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Enum

from app import db, bcrypt


class AccountType(enum.Enum):
    NORMAL = 'normal'
    SUPER = 'super'


class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(Enum(AccountType), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    products = db.relationship('Product', backref='user', lazy=True)

    def __init__(self, username, password, user_type):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.user_type = user_type

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
