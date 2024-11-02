from flask import session


def create(user):
    session['user_id'] = user.id
    session['user_name'] = user.username
    session['authenticated'] = True


def teardown():
    session.clear()


def has_user_session():
    return get_user_id() is not None and get_username() is not None and user_is_authenticated()


def get_user_id():
    return session.get('user_id')


def get_username():
    return session.get('user_name')


def user_is_authenticated():
    return session.get('authenticated')
