from flask import session


def create_session(user):
    session['user_id'] = user.id
    session['user_name'] = user.username
    session['authenticated'] = True


def teardown_session():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('authenticated', None)


def has_session():
    return session.get('user_id') is not None and session.get('user_name') and session.get('authenticated')
