from app import ma
from app.models import Product


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field(required=True)
    quantity = ma.auto_field(required=True)
    price = ma.auto_field(required=True)
    user_id = ma.auto_field(required=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
