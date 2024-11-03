from datetime import datetime

from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    __table_args__ = (
        db.CheckConstraint('quantity >= 0', name='check_quantity_positive'),
        db.CheckConstraint('price >= 0', name='check_price_positive'),
    )

    def __init__(self, name, quantity, price, user_id):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.user_id = user_id

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', quantity={self.quantity}, price={self.price})>"
