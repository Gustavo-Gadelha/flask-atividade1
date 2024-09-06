class UserAccountDAO:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def create_user(self, username, password, user_type):
        sql = """
        INSERT INTO user_account (username, password, type)
        VALUES (%s, %s, %s)
        RETURNING id;
        """

        return self.db_manager.execute(sql, (username, password, user_type))

    def get_all_users(self, user_id):
        sql = 'SELECT * FROM user_account'
        return self.db_manager.execute(sql, fetch=True)

    def get_user_by_id(self, user_id):
        sql = 'SELECT * FROM user_account WHERE id = %s'
        return self.db_manager.execute(sql, (user_id,), fetch=True, one=True)

    def get_user_by_username(self, username):
        sql = 'SELECT * FROM user_account WHERE username = %s'
        return self.db_manager.execute(sql, (username,), fetch=True, one=True)

    def update_user(self, user_id, username=None, password=None, user_type=None):
        updates = []
        params = []

        if username is not None:
            updates.append('username = %s')
            params.append(username)
        if password is not None:
            updates.append('password = %s')
            params.append(password)
        if user_type is not None:
            updates.append('type = %s')
            params.append(user_type)

        sql = f'UPDATE user_account SET {', '.join(updates)}  WHERE id = %s'
        params.append(user_id)

        return self.db_manager.execute(sql, params)

    def delete_user(self, user_id):
        sql = 'DELETE FROM user_account WHERE id = %s'
        return self.db_manager.execute(sql, (user_id,))
