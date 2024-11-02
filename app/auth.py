from flask_login import LoginManager

from app.models import UserAccount

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))
