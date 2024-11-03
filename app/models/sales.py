from datetime import date

from sqlalchemy import CheckConstraint

from app import db


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today(), nullable=False)

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )

    def __repr__(self):
        return f"<Sales(id={self.id}, product='{self.product_name}', quantity={self.quantity}, total_price={self.total_price}, date={self.date})>"
