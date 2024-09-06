class ProductDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_product(self, name, user_id, quantity=0, price=0.00):
        sql = """
        INSERT INTO product (name, user_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """

        return self.db_manager.execute(sql, (name, user_id, quantity, price))

    def get_all_producs(self):
        sql = 'SELECT * FROM product'
        return self.db_manager.execute(sql, fetch=True)

    def get_product_by_id(self, product_id):
        sql = 'SELECT * FROM product WHERE id = %s'
        return self.db_manager.execute(sql, (product_id,), fetch=True, one=True)

    def get_products_by_user(self, user_id):
        sql = 'SELECT * FROM product WHERE user_id = %s'
        return self.db_manager.execute(sql, (user_id,), fetch=True)

    def update_product(self, product_id, name=None, quantity=None, price=None):
        updates = []
        params = []

        if name is not None:
            updates.append('name = %s')
            params.append(name)
        if quantity is not None:
            updates.append('quantity = %s')
            params.append(quantity)
        if price is not None:
            updates.append('price = %s')
            params.append(price)

        sql = f'UPDATE product SET {', '.join(updates)} WHERE id = %s'
        params.append(product_id)

        return self.db_manager.execute(sql, params)

    def delete_product(self, product_id):
        sql = 'DELETE FROM product WHERE id = %s'
        return self.db_manager.execute(sql, (product_id,))
