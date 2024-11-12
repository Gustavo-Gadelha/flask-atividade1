from marshmallow import ValidationError, validate

from app import ma
from app.models import Product


def validate_quantity(value):
    if not isinstance(value, int) or value < 1:
        raise ValidationError('A quantidade deve ser um número inteiro positivo maior ou igual a 1')
    if len(str(value)) > 10:
        raise ValidationError('A quantidade do produto não pode exceder 10 dígitos')


def validate_price(value):
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValidationError('O preço total deve ser um número inteiro positivo não-nulo')
    if len(str(int(value))) > 10:
        raise ValidationError('O preço do produto não pode exceder 10 dígitos antes do ponto decimal')


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field(required=True, validate=validate.Length(min=5, max=60))
    quantity = ma.auto_field(required=True, validate=validate_quantity)
    price = ma.auto_field(required=True, validate=validate_price)
    user_id = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
