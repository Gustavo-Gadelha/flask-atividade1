from marshmallow.fields import Enum

from app import ma
from app.models import UserAccount
from app.models.user_account import AccountType


class UserAccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserAccount
        load_instance = True

    id = ma.auto_field()
    username = ma.auto_field(required=True)
    account_type = Enum(AccountType, by_value=True, required=True)

    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


user_account_schema = UserAccountSchema()
user_accounts_schema = UserAccountSchema(many=True)
